import math
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Nodes/Kiss/Kiss Up':  {
    'cmd': 'kiss_up()',
    'hotkey': 'F1',
    'icon': ''
  },
  'Tools/Nodes/Kiss/Kiss Down':  {
    'cmd': 'kiss_down()',
    'hotkey': 'F2',
    'icon': ''
  }
}



def check_proximity(sel_xywh, nearby_xywh, direction, proximity=[50,80]):
  """
  newer method to check if a node is below another node
  Note: nuke coordinates are measured from top left corner for node and screen
  """
  horiz = nearby_xywh[0] - proximity[0] <= sel_xywh[0] + sel_xywh[2]/2 <= nearby_xywh[0] + nearby_xywh[2] + proximity[0]
  if direction == 'up':
    vert = nearby_xywh[1] + nearby_xywh[3] <= sel_xywh[1] <= nearby_xywh[1] + nearby_xywh[3] + proximity[1]
  else:
    vert = nearby_xywh[1] - proximity[1] <= sel_xywh[1] + sel_xywh[3] <= nearby_xywh[1]
  if horiz and vert: return True
  else: return False


def kiss_up(proximity=100):
  try:
    sel = nuke.selectedNode()
    sel_xywh = [sel.xpos(), sel.ypos(), sel.screenWidth(), sel.screenHeight()]
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
      node_xywh = [node.xpos(), node.ypos(), node.screenWidth(), node.screenHeight()]
      if check_proximity(sel_xywh, node_xywh, 'up'):
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


def kiss_down(proximity=100):
  try:
    sel = nuke.selectedNode()
    sel_xywh = [sel.xpos(), sel.ypos(), sel.screenWidth(), sel.screenHeight()]
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
      node_xywh = [node.xpos(), node.ypos(), node.screenWidth(), node.screenHeight()]
      if check_proximity(sel_xywh, node_xywh, 'down'):
        max_inputs = node.maxInputs()
        for m in range(max_inputs):
          if node.input(m) is sel:
            return
          if node.canSetInput(m, sel):
            if node.input(m) is None:
              node.setInput(m, sel)
              return
        return
