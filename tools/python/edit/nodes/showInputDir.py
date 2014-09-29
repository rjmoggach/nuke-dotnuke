import os, platform
import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

if platform.system() == 'Linux':
  if os.path.exists('/usr/bin/nautilus'):
    _browser = 'Nautilus'
  if os.path.exists('/usr/bin/konqueror'):
    _browser = 'Konqueror'
elif platform.system() == 'Darwin':
    _browser = 'Finder'
else:
  _browser = 'Explorer'


__menus__ = {
  'Tools/Edit/Nodes/Show in {0}'.format(_browser): {
    'cmd': 'showInputDir(nuke.selectedNodes())',
    'hotkey': '#r',
    'icon': ''
  }
}


def showInputDir(nodes=[]):
  '''
  function that shows a file browser window
  for the directory in a read or write node
  '''
  # if no nodes are specified then look for selected nodes
  if not nodes:
    nodes = nuke.selectedNodes()

  # if nodes is still empty no nodes are selected
  if not nodes:
    nuke.message('ERROR: No node(s) selected.')
    return

  for entry in nodes:
    _class = entry.Class()
    if _class == "Write" or _class == "Read":
      path = nuke.filename(entry)
      if path is None:
        continue
      if path[-1:] is '/':
        path = path[:-1]
      root_path = os.path.dirname(os.path.dirname(path))
      for n in nuke.selectedNodes():
        n['selected'].setValue(False)
      if platform.system() == 'Linux':
        if os.path.exists('/usr/bin/nautilus'):
          os.popen2('/usr/bin/nautilus %s' % root_path)
        if os.path.exists('/usr/bin/konqueror'):
          os.popen2('/usr/bin/konqueror %s' % root_path)
      elif platform.system() == 'Darwin':
        os.popen2('open %s' % root_path)
      else:
        u=os.path.split(path)[0]
        u = os.path.normpath(u)
        cmd = 'explorer "%s"' % (u)
        os.popen2(cmd)
        #os.system(cmd)
  return
