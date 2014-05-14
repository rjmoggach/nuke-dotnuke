import re
import nuke

__menus__ = {}


KNOBS_TO_IGNORE = [
  'display',
  'selectable',
  'import_chan',
  'export_chan',
  'xform_order',
  'rot_order',
  'projection_mode'
]

KNOBS_3D = [
  'translate',
  'rotate',
  'scaling',
  'skew',
  'pivot',
  'near'
]

KNOBS_UV = [
  'win_translate',
  'rotate',
  'scaling',
  'skew',
  'pivot',
  'near'
]

ROTATE_CHANS = (
  'rotate.x',
  'rotate.y',
  'rotate.z'
)

DATA_FORMAT_OPTIONS = "mm cm inch"

CAMERA_KNOBS = [
  'haperture',
  'vaperture',
  'focal'
]

NODE_TYPE_OPTIONS = 'Camera Axis'


def getKnobChannels(node):
  '''
  function that searches a node for knobs that have
  data for import or export and returns a list
  '''
  knobData = nuke.toNode(node).writeKnobs(1)
  knobIndex = nuke.toNode(node).writeKnobs(0)
  knobList = knobIndex.split(' ')
  knobs = []
  for knob in knobList:
    if knob in KNOBS_TO_IGNORE:
      continue
    if knob in KNOBS_3D:
      knob3dRegex = re.compile('%s \{[0-9]* [0-9]* [0-9]*\}' % knob)
      knob3dRegexMatch = knob3dRegex.search(knobData)
      if knob3dRegexMatch != None:
        knobs.append(knob+'.x')
        knobs.append(knob+'.y')
        knobs.append(knob+'.z')
        continue
    if knob in KNOBS_UV:
      knobUVregex = re.compile('%s \{[0-9]* [0-9]*\}' % knob)
      knobUVregexMatch = knobUVregex.search(knobData)
      if knobUVregexMatch != None:
        knobs.append(knob+'.u')
        knobs.append(knob+'.v')
        continue
    knobs.append(knob)
  return knobs

def getDataConversions(dataTypes):
  '''
  creates panel to choose data conversions
  and returns corresponding conversion
  '''
  print str(dataTypes)
  p = nuke.Panel("Import Data Type:")
  conversions = []
  # check if lists INTERSECT
  if not list(set(ROTATE_CHANS) & set(dataTypes)) == []:
    conversions.append('rotation')
    p.addEnumerationPulldown('rotation', 'degrees radians')
  for knobType in CAMERA_KNOBS:
    try:
      #Look for the data type
      dataTypes.index(knobType)
      #if found add to to the returnLookUp List
      conversions.append(knobType)
      #Add pulldown option to the panel
      p.addEnumerationPulldown(knobType, DATA_FORMAT_OPTIONS)
    except:
      pass
  p.addButton("Cancel") # returns 0
  p.addButton("Ok") # returns 1
  p.setWidth(250)
  if conversions != []:
    try: result = p.show()
    except: result = False
  else: result = True
  if result:
    if 'rotation' in conversions:
      if p.value('rotation') == 'radians': rotateConversion = 57.2957795
      else: rotateConversion = 1
    else: rotateConversion = 1

    if 'focal' in conversions:
      if p.value('focal') == 'inch': focalConversion = 25.4
      elif p.value('focal') == 'cm': focalConversion = 100
      else: focalConversion = 1
    else: focalConversion = 1

    if 'haperture' in conversions:
      if p.value('haperture') == 'inch': hapertureConversion = 25.4
      elif p.value('haperture') == 'cm': hapertureConversion = 100
      else: hapertureConversion = 1
    else: hapertureConversion = 1

    if 'vaperture' in conversions:
      if p.value('vaperture') == 'inch': vapertureConversion = 25.4
      elif p.value('vaperture') == 'cm': vapertureConversion = 100
      else: vapertureConversion = 1
    else: vapertureConversion = 1

    print 'rotateConversion: %s' % str(rotateConversion)
    print 'focalConversion: %s' % str(focalConversion)
    print 'hapertureConversion: %s' % str(hapertureConversion)
    print 'vapertureConversion: %s' % str(vapertureConversion)

    return rotateConversion, focalConversion, hapertureConversion, vapertureConversion
  else:
    return False

def createChannelOrderPanel(dataTypesCount, dataTypes=''):
  '''
  opens a nuke panel for setting chan data types
  '''
  if dataTypes == '':
    dataTypes = [
      'none',
      'frame',
      'translate.x',
      'translate.y',
      'translate.z',
      'rotate.x',
      'rotate.y',
      'rotate.z',
      'scaling.x',
      'scaling.y',
      'scaling.z',
      'focal',
      'haperture',
      'vaperture'
    ]
  else:
    dataTypes = ['none', 'frame'] + dataTypes
  p = nuke.Panel("Import Chan Data:")
  #Create the number of pulldowns based on the numberOfNameTypes
  for chanNumber in range(dataTypesCount):
    p.addEnumerationPulldown(str(chanNumber), string.join(dataTypes))
  #add buttons and window size
  p.addButton("Cancel") # returns 0
  p.addButton("Ok") # returns 1

  try: result = p.show()
  except: result = False
  if result:
    returnData = []
    for chanNumber in range(dataTypesCount):
      returnData.append(p.value(str(chanNumber)))
    return returnData
  else:
    return False


def createNodePanel():
  '''
  function to create camera or axis node
  '''
  p = nuke.Panel("Create Node:")
  p.addEnumerationPulldown("Type:", NODE_TYPE_OPTIONS)
  p.addButton("Cancel") # returns 0
  p.addButton("Ok") # returns 1
  try:
    result = p.show()
  except:
    result = False
  #Crashes if value() is called and the panel was canceled
  if result:
    selectedNode = nuke.createNode("Camera")
    return selectedNode
  else:
    return None


def setKey(node, knob, frame, value):
  '''
  work around function to set values at key frames
  '''
  TCL = 'setkey %s.%s %s %s' % (node, knob, str(frame), str(value))
  try: nuke.tcl(TCL)
  except: return 0
  return 1


def getDataSetCount(file):
  '''
  inspects a chan file and returns the data set count
  from the first line of the file
  '''
  fileData = open(file, 'r')
  firstLine = fileData.readline()
  fileData.close()
  dataSetCount = len(firstLine.split(' '))
  return dataSetCount


def importChan(chanFile = ''):
  '''
  import chan data from a file to selected node knobs
  '''

  if chanFile == '':
    rawInput = nuke.getClipname('Select Chan File', '*.chan', chanFile)
    if rawInput == None:
      print "CANCEL"
      return
    else:
      chanFile = rawInput
  chanFileName = os.path.basename(chanFile)

  # get data set count
  dataSetCount = getDataSetCount(chanFile)
  # Create Empty Node
  selectedNode = createNodePanel()
  nodeName = selectedNode.name()

  #get a list of posible knobs
  nodeKnobList = getKnobChannels(nodeName)

  #Get list of data types in chan order
  knobLookups = createChannelOrderPanel(dataSetCount, nodeKnobList)

  #Set units of the data being imported
  rotateConversion, focalConversion, hapertureConversion, vapertureConversion = getDataConversions(knobLookups)

  fileData = open(chanFile, 'r')
  frame = 0

  #try to to find the location of the frame number data
  try: frameDataLocation = knobLookups.index('frame')
  except: frameDataLocation = -1

  #Make list of lines of data
  fileLines = fileData.readlines()

  #Read each line of data from chan file
  for line in fileLines:

    #split the data up into a list
    lineData = line.split(' ')

    if frameDataLocation == -1:
      #incr frame number
      frame += 1
    else:
      frame = lineData[frameDataLocation]

    #for dataIndex in the number of elements in the list
    for lineNumber in range(len(lineData)):

      #get value from lineData
      value = lineData[lineNumber]

      #Look up the knob type
      knob = knobLookups[lineNumber]


      #set knob value if not set to none
      if knob in ['none', 'frame']:
        print "PASS(%s,%s) %s %s" % (str(frame), str(lineNumber), knob, str(value))
      else:
        print "(%s,%s) %s %s" % (str(frame), str(lineNumber), knob, str(value))
        if knob == "haperture":
          setKey(nodeName, knob, frame, float(value) * hapertureConversion)
        else:
          setKey(nodeName, knob, frame, value)
  print 'Chan Import Complete.'
  fileData.close()
  selectedNode.knob('label').setValue(chanFileName)
  return


def exportChan(node=''):
  '''
  export node knobs channel data to chan file
  '''
  pass




