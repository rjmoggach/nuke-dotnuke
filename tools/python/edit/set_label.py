import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Edit/Nodes/Set Label': {
    'cmd': 'set_label()',
    'hotkey': 'F9',
    'icon': ''
  }
}

def set_label():
    
    '''Quick edit the label for the selected node'''
    
    try:
        sn = nuke.selectedNodes()[-1]
        snLabel = sn['label'].value()
        snName = sn.name()
    except:
        sn = None
        return
    
    p = nuke.Panel( 'Edit Label' )
    p.setTitle( 'Edit label for %s' % snName )
    p.setWidth( 350 )
    p.addNotepad('Label', snLabel)
    result = p.show()
    
    if result:
        label = p.value('Label')
        try:
            sn['label'].setValue(label)
        except:
            return
            
            
