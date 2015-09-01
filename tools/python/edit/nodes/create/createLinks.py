import os, platform
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Edit/Nodes/Create/Symbolic Links': {
    'cmd': 'createLinks(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}
def createLinks(nodes=[]):
  '''
  function that creates symbolic links to
  the selected read or write node image folders
  at a given location
  '''
  # if no nodes are specified then look for selected nodes
  if not nodes:
    nodes = nuke.selectedNodes()

  # if nodes is still empty no nodes are selected
  if not nodes:
    nuke.message('ERROR: No node(s) selected.')
    return

  EXISTING = []

  p = nuke.Panel( 'Choose Path' )
  p.setTitle( 'Choose a path' )
  p.setWidth( 500 )
  p.addFilenameSearch('Directory', os.getcwd())
  result = p.show()

  if result:
    dest = p.value('Directory')
  else:
    return

  for entry in nodes:
    _class = entry.Class()
    if _class == "Write":
      path = nuke.filename(entry)
      if path is None:
        continue
      root_path = os.path.dirname(path)
      IGNORE = ['Left', 'left', 'L', 'l', 'Right', 'right', 'R', 'r', '2k_flat', '2k_scope', 'hd', 'jpg', 'exr', 'tif', 'dpx']
      while os.path.split(root_path)[1] in IGNORE:
        root_path=os.path.split(root_path)[0]
      try:
        os.symlink(root_path, os.path.join(dest, os.path.basename(root_path)) )
      except:
        continue

