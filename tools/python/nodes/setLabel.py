import nuke

__menus__ = {
  'Tools/Nodes/Set Label': {
    'cmd': 'setLabel(nuke.selectedNodes())',
    'hotkey': '',
    'icon': ''
  }
}

def setLabel(nodes):
	'''Quickly edit the label for the selected node'''
	for node in nodes:
	 node_label = node['label'].value()
	 node_name = node.name()
	 title = 'Edit Label for {0}'.format(node_name)
	 p = nuke.Panel(title)
	 p.setTitle(title)
	 p.setWidth(400)
	 p.addNotepad('Label', node_label)
	 result = p.show()
	 if result:
	   label = p.value('label')
	   try:
	     node['label'].setValue(label)
	   except:
	     return
