from __future__ import with_statement
import nuke
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Other/Delete Viewers': {
    'cmd': 'deleteViewers()',
    'hotkey': '+D',
    'icon': ''
  }
}

def deleteViewers():
  counter = 0
  with nuke.root():
    for i in nuke.allNodes(recurseGroups=True):
      if i.Class() == "Viewer":
        nuke.delete(i)
        counter+=1
    print "DeleteViewers: {0} viewers deleted.".format(counter)