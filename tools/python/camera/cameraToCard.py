import nuke

__menus__ = {
  'Camera -> Card':  {
    'command': 'cameraToCard()',
    'hotkey': '',
    'icon': ''
  },
  'Card -> Camera':  {
    'command': 'cardToCamera()'
    'hotkey': '',
    'icon': ''
  }
}

def cameraToCard():
	transGeoNode=nuke.createNode('TransformGeo', 'inputs {2} name {cameraToCard} translate {0 0 "-this.distance"} scaling {this.hapt this.vapt} uniform_scale {this.distance} addUserKnob {20 Distance} addUserKnob {7 hapt} hapt {{"1/([value input1.focal]/[value input1.haperture])" }} addUserKnob {7 vapt} vapt {{"1/([value input1.focal]/[value input1.haperture])"}} addUserKnob {7 distance R 0 1000} distance 1')
	transGeoNodeTranslate = "%s.translate" % transGeoNode.name()
	transGeoNodeDistance = "%s.distance" % transGeoNode.name()
	axisNode = nuke.createNode('Axis')
	cameraNode = nuke.createNode('Camera2', 'translate {0 0 %s} pivot {%s %s %s}'  (transGeoNodeDistance, transGeoNodeTranslate, transGeoNodeTranslate, transGeoNodeTranslate))
	transGeoNode.setInput(1, cameraNode)
	cameraNode.setInput(1, axisNode)

def cardToCamera():
	transformGeoNode=nuke.createNode('TransformGeo', 'name {cardToCamera} translate {0 0 "-this.distance"} scaling {this.hapt this.vapt} uniform_scale {this.distance} addUserKnob {20 Distance} addUserKnob {7 hapt} hapt {{"1/([value input1.focal]/[value input1.haperture])" }} addUserKnob {7 vapt} vapt {{"1/([value input1.focal]/[value input1.haperture])" }} addUserKnob {7 distance R 0 1000} distance 1')
	cameraNode=nuke.createNode('Camera2')
	transformGeoNode.setInput(1, cameraNode)
