import nuke

__menus__ = {
  'Tools/Nodes/Create Dots': {
    'cmd': 'createDots(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}



def createDots(nodes):
  '''
  Creates more organized trees using intermediary dots
  '''
  for node in nodes:
    nodeXpos = node.xpos()
    nodeYpos = node.ypos()
    nodeWidth = node.screenWidth()
    nodeHeight = node.screenHeight()
    try:
      A = node.input(0)
      AXpos = A.xpos()
      AXpos = A.ypos()
      AWidth = A.screenWidth()
      AHeight = A.screenHeight()
      B = node.input(1)
      dot = nuke.nodes.Dot()
      if B:
        BXpos = B.xpos()
        BYpos = B.ypos()
        BWidth = B.screenWidth()
        BHeight = B.screenHeight()
        dot.setInput(0,B)
        node.setInput(1,dot)
        dot.setXYpos(BXpos+BWidth/2-6,nodeYpos+4)
        if A.Class()== "Dot":
          node.knob("xpos").setValue(AXpos-nodeWidth/2+6)
        else:
          node.knob("xpos").setValue(AXpos)
      else:
        dot.setInput(0,A)
        node.setInput(0,dot)
        dot.setXYpos(nodeXpos+nodeWidth/2-6,AXpos+AHeight/2-6)
    except:
      pass
