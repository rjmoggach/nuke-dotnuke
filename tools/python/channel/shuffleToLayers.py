import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Channel/Shuffle Layers': {
    'cmd': 'shuffleToLayers(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}


def shuffleToLayers(nodes, margins=[50,30], dots=True):
  '''
  Shuffles a multi-layer EXR to multiple shuffle nodes
  '''
  node_xywh=[]
  dot_xywh=[]
  shuf_xywh=[]
  for node in nodes:
    channels = nuke.channels(node)
    if not node_xywh:
      node_xywh = [node.xpos(),node.ypos(), node.screenWidth(), node.screenHeight()]
    else:
      node.setXYpos(shuf_xywh[0] + (shuf_xywh[2] + dot_xywh[2])/2 + margins[0], dot_xywh[1] - margins[1] - node_xywh[3])
    layers = []
    validChannels = ['red', 'green', 'blue', 'alpha', 'black', 'white']
    dot_xywh = []

    for each in channels:
      layerName = each.split('.')[0]
      tmp = []
      for channel in channels:
        if channel.startswith(layerName):
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

      dot = nuke.nodes.Dot()
      shuffle = nuke.createNode('Shuffle', prefs)
      shuffle.knob('label').setValue('[value in]')
      shuffle.setInput(0, dot)

      if not dot_xywh:
        dot.setInput(0, node)
        dot_xywh = [dot.xpos(), dot.ypos(), dot.screenWidth(), dot.screenHeight()]
        if not shuf_xywh:
          dot.setXYpos( node_xywh[0] + (node_xywh[2]-dot_xywh[2])/2, node_xywh[1] + node_xywh[3] + margins[1])
        else:
          dot.setXYpos( shuf_xywh[0] + margins[0] + shuf_xywh[2], shuf_xywh[1] - margins[1] - dot_xywh[3])
      else:
        dot.setInput(0, nuke.toNode(dotName))
        dot.setXYpos(dot_xywh[0] + shuffle.screenWidth() + margins[0], dot_xywh[1])        

      dotName = dot.name()
      dot_xywh = [dot.xpos(), dot.ypos(), dot.screenWidth(), dot.screenHeight()]
      shuffle.setXYpos(dot_xywh[0]-(shuffle.screenWidth()-dot_xywh[2])/2, dot_xywh[1] + dot_xywh[3] + margins[1])
      shuf_xywh = [shuffle.xpos(), shuffle.ypos(), shuffle.screenWidth(), shuffle.screenHeight()]

