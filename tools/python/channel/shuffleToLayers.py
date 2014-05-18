import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Channel/Shuffle Layers': {
    'cmd': 'shuffleToLayers(nuke.selectedNodes())',
    'hotkey': '#s',
    'icon': ''
  }
}


def shuffleToLayers(nodes):
  '''
  Shuffles a multi-layer EXR to multiple shuffle nodes
  '''
  for node in nodes:
    channels = nuke.channels(node)
    posX = node['xpos'].value()
    posY = node['ypos'].value()
    layers = []
    validChannels = ['red', 'green', 'blue', 'alpha', 'black', 'white']

    for each in channels:
      layerName = each.split('.')[0]
      tmp = []
      for channel in channels:
        if channel.startswith(layerName) == True:
          tmp.append(channel)
      if len(tmp) < 4:
        for i in range(4-len(tmp)):
          tmp.append("%s.white" % layerName)
      if tmp not in layers:
        layers.append(tmp)

    for each in layers:
      layer = each[0].split('.')[0]
      channel1 = each[0].split('.')[1]
      channel2 = each[1].split('.')[1]
      channel3 = each[2].split('.')[1]
      channel4 = each[3].split('.')[1]

      if channel1 not in validChannels:
        channel1 = "red red"
      else:
        channel1 = "%s %s" % (channel1, channel1)

      if channel2 not in validChannels:
        channel2 = "green green"
      else:
        channel2 = "%s %s" % (channel2, channel2)

      if channel3 not in validChannels:
        channel3 = "blue blue"
      else:
        channel3 = "%s %s" % (channel3, channel3)

      if channel4 not in validChannels:
        channel4 = "alpha alpha"
      else:
        channel4 = "%s %s" % (channel4, channel4)

      prefs = "in %s %s %s %s %s" % (layer, channel1, channel2, channel3, channel4)
      shuffle = nuke.createNode('Shuffle', prefs)
      shuffle.knob('label').setValue('[value in]')
      shuffle.setInput(0, node)



