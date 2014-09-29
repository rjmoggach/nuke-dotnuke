import nuke


__menus__ = {
  'Tools/Time/Frame Hold Now':  {
    'cmd': 'frame_hold_set(nuke.selectedNode())',
    'hotkey': '',
    'icon': ''
  }
}


SET_CMD="""
node = nuke.thisNode()
node['first_frame'].setValue(nuke.frame())
"""

def frame_hold_set(node):
  if not node:
    return
  elif not node.Class() == 'FrameHold':
    return
  else:
    node['first_frame'].setValue(nuke.frame())
    tab_knob = nuke.Tab_Knob("SetThisFrame", "SetThisFrame")
    node.addKnob(tab_knob)
    script_btn = nuke.PyScript_Knob("SetThisFrame", "SetThisFrame")
    node.addKnob(script_btn)
    node.knob("SetThisFrame").setCommand(SET_CMD)
