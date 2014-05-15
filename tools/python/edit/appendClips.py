import nuke

__menus__ = {
  'Tools/Edit/Append Clips':  {
    'cmd': 'appendClips()',
    'hotkey': '',
    'icon': ''
  }
}

def appendClips():
  sw = nuke.nodes.AppendClip()
  an = [n for n in nuke.allNodes() if n.Class() == "Read"] 
  s=len(an)
  print s
  x=0
  while x != s:
    sw.setInput(x,an[x])
    x=x+1
 
