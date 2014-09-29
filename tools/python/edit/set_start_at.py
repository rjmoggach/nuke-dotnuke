import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Nodes/Set Start At': {
    'cmd': 'set_start_at(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}

def set_start_at(nodes):
    
    '''Quick change a read node to start at a frame'''
    if not nodes:
      return
    else:
      p = nuke.Panel('Edit Start At')
      p.setTitle('Edit Start At')
      p.setWidth(200)
      p.addNotepad('StartAt', '1')
      result = p.show()
      if result:
        start_at = p.value('StartAt')
        for node in nodes:
          if node.Class() in [ "Read", "Read2"]:
            node['frame_mode'].setValue('start at')
            node['frame'].setValue(start_at)
            node_name = node.name()
