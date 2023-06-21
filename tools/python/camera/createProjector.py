import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"


__menus__ = {
    "Camera/Create Projector from Camera": {
        "cmd": "createProjector(nuke.selectedNodes())",
        "hotkey": "",
        "icon": "",
    }
}


def clipboard():
    return "%clipboard%"


def copy_paste():
    nuke.nodeCopy(clipboard())
    for node in nuke.allNodes():
        node.knob("selected").setValue(False)
    nuke.nodePaste(clipboard())


def createProjector():
    selectedNodes = nuke.selectedNodes()
    for cameraNode in nuke.selectedNodes():
        if cameraNode.Class() in ["Camera2", "Camera"]:
            cameraNodeName = cameraNode.name()
            frame = nuke.getInput("Frame to Project for {0}?".format(cameraNode.name()))
            try:
                int(frame)
            except ValueError:
                nuke.message("You must enter a frame number!")
                return 0
            copy_paste()
            selectedCamera = nuke.selectedNode()
            selectedCamera.addKnob(nuke.Int_Knob("referenceFrame", "Reference Frame"))
            selectedCamera["referenceFrame"].setValue(int(frame))
            selectedCamera["label"].setValue(
                "Projection at frame: [value referenceFrame]"
            )
            selectedCamera["tile_color"].setValue(123863)
            selectedCamera["gl_color"].setValue(123863)

            for knob in selectedCamera.knobs().values():
                if knob.hasExpression():
                    if knob.arraySize() == 1:
                        nuke.animation(
                            "{0}.{1}".format(selectedCamera.name(), knob.name()),
                            "generate",
                            (
                                "{0}".format(nuke.root().firstFrame()),
                                "{0}".format(nuke.root().lastFrame()),
                                "1",
                                "y",
                                "{0}".format(knob.name()),
                            ),
                        )
                    else:
                        i = knob.arraySize() - 1
                        while i > -1:
                            nuke.animation(
                                "{0}.{1}.{2}".format(
                                    selectedCamera.name(), knob.name(), i
                                ),
                                "generate",
                                (
                                    "{0}".format(nuke.root().firstFrame()),
                                    "{0}".format(nuke.root().lastFrame()),
                                    "1",
                                    "y",
                                    "{0}".format(knob.name()),
                                ),
                            )
                            i = i - 1

            for knob in selectedCamera.knobs().values():
                if knob.isAnimated():
                    knob.setExpression("curve(referenceFrame)")
