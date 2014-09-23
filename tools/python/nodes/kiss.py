import math
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Nodes/Align/Kiss':  {
    'cmd': 'toggle_node()',
    'hotkey': 'F1',
    'icon': ''
  },
  'Tools/Nodes/Align/Kiss Down':  {
    'cmd': 'toggle_node_down()',
    'hotkey': 'F2',
    'icon': ''
  }
}


# m.addCommand('ToggelNode...', ToggelNode, 'F1')
# m.addCommand('ToggelDownNode...', Toggel_DownNode, 'F2')

def check_proximity(node_xy, node_wh, sel_xy):
  horiz = math.fabs(node_xy[0] - sel_xy[0]) <= node_wh[0]
  vert = math.fabs(node_xy[0] - sel_xy[0]) <= node_wh[1]
  if horiz and vert: return True
  else: return False

def toggle_node():
  try:
    sel = nuke.selectedNode()
    sel_xy = [sel.xpos(), sel.ypos()]
  except:
    return
  all_nodes = nuke.allNodes()
  input_count = sel.maxInputs()
  connected = []
  disconnected = []
  related = False
  for i in range(input_count):
    if not sel.input(i) is None:
      connected.append(i)
    else:
      disconnected.append(i)
  if len(disconnected) == 0:
    return
  for node in all_nodes:
    if not node is sel:
      node_xy = [node.xpos(), node.ypos()]
      node_wh = [node.screenWidth(), node.screenHeight()]
      if check_proximity(node_xy, node_wh, sel_xy):
        for input_num in connected:
          if sel.input(input_num).name() == node.name():
            related = True
            break
        if not related:
          if sel.Class() == 'ScanlineRender' and node.Class() == 'Scene':
            sel.setInput(1, node)
          else:
            sel.setInput(disconnected[0], node)
          return


def toggle_node_down():
  try:
    sel = nuke.selectedNode()
    sel_xy = [sel.xpos(), sel.ypos()]
  except:
    return
  all_nodes = nuke.allNodes()
  input_count = sel.maxInputs()
  connected = []
  disconnected = []
  related = False
  all_nodes = nuke.allNodes()
  for node in all_nodes:
    if not node is sel:
      node_xy = [node.xpos(), node.ypos()]
      node_wh = [node.screenWidth(), node.screenHeight()]
      if check_proximity(node_xy, node_wh, sel_xy):
        max_inputs = node.maxInputs()
        for m in range(max_inputs):
          if node.input(m) is sel:
            return
          if node.canSetInput(m, sel):
            if node.input(m) is None:
              node.setInput(m, sel)
              return
        return
