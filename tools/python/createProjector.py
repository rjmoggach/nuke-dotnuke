import nuke
import nukescripts

def createProjector(cameraNode):
	if not cameraNode.Class() == "Camera2" or not cameraNode.Class() == "Camera":
		nuke.message("Please select a camera")
	else:
		frame = nuke.getInput("Frame to project")
		try:
			int(frame)
		except ValueError:
			nuke.message("You must enter a frame number!")
			return 0

		nukescripts.node_copypaste()
		cameraNode = nuke.selectedNode()
		cameraNode.addKnob(nuke.Int_Knob('referenceFrame', 'Reference Frame'))
		cameraNode['referenceFrame'].setValue(int(frame))
		cameraNode['label'].setValue("Projection at frame: [value referenceFrame]")
		cameraNode['tile_color'].setValue(123863)
		cameraNode['gl_color'].setValue(123863)

		for knob in cameraNode.knobs().values():
			if knob.hasExpression():
				if knob.arraySize() ==1:
					nuke.animation("%s.%s" % (cameraNode.name(), knob.name()), "generate", ("%s" % (nuke.root().firstFrame()), "%s" % (nuke.root().lastFrame()), "1", "y", "%s" % (knob.name())))
				else:
					i = knob.arraySize() -1
					while i > -1:
						nuke.animation("%s.%s.%s" % (cameraNode.name(), knob.name(), i), "generate", ("%s" % (nuke.root().firstFrame()), "%s" % (nuke.root().lastFrame()), "1", "y", "%s" % (knob.name())))
						i = i-1


		for knob in cameraNode.knobs().values():
		   if knob.isAnimated():
			   knob.setExpression('curve(referenceFrame)')


