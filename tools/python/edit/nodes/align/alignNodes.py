import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Tools/Edit/Nodes/Align/Align Nodes X':  {
    'cmd': 'alignNodes(nuke.selectedNodes())',
    'hotkey': '#x',
    'icon': ''
  },
  'Tools/Edit/Nodes/Align/Align Nodes Y':  {
    'cmd': 'alignNodes(nuke.selectedNodes(), "y")',
    'hotkey': '#y',
    'icon': ''
  }
}


def alignNodes( nodes, direction = 'x' ):
  '''
  Align nodes either horizontally or vertically.
  '''
  if len( nodes ) < 2:
    return
  if direction.lower() not in ('x', 'y'):
    raise ValueError, 'direction argument must be x or y'

  positions = [ float( n[ direction.lower()+'pos' ].value() ) for n in nodes]
  avgPosition = sum( positions ) / len( positions )
  for n in nodes:
    if direction == 'x':
      for n in nodes:
        if not n.Class() == "Dot":
          n.setXpos( int(avgPosition) )
        else:
          n.setXpos( int(avgPosition) + 40)
    else:
      for n in nodes:
          n.setYpos( int(avgPosition) )

  return avgPosition


