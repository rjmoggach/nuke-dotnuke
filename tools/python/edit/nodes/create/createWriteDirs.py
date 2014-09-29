import os, platform
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Nodes/Create/Create Write Dirs': {
    'cmd': 'createWriteDirs(nuke.selectedNodes())',
    'hotkey': '#+w',
    'icon': ''
  }
}
def createWriteDirs(nodes=[]):
  '''
  Makes directories for selected write nodes
  '''
  # if no nodes are specified then look for selected nodes
  if not nodes:
    nodes = nuke.selectedNodes()

  # if nodes is still empty no nodes are selected
  if not nodes:
    nuke.message('ERROR: No node(s) selected.')
    return

  EXISTING = []

  for entry in nodes:
    _class = entry.Class()
    if _class == "Write":
      path = nuke.filename(entry)
      if path is None: continue
      root_path = os.path.dirname(path)

      if os.path.exists(root_path) == True:
        nuke.tprint('Path Exists: '+ root_path )
        return
      try:
        os.mkdir(root_path)
        os.chmod(root_path,0775)
      except:
        if nuke.ask('Create Path: '+ root_path):
          os.makedirs(root_path)
          os.chmod(root_path,0775)
        else:
          return
  return
