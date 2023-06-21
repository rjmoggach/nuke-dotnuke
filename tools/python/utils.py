import sys
import os
import threading
import time
import re
import importlib


import nuke

__menus__ = {}


def getScene():
    root_name = nuke.toNode("root").name()
    return root_name


def getRenderOpts():
    # returns a Nuke "format" object
    oRenderOpts = nuke.toNode("root").knob("format").value()
    return oRenderOpts


def getSelected():
    sel = nuke.selectedNode().knob("name").value()
    return sel


def getResX():
    oFormat = getRenderOpts()
    ResX = nuke.Format.width(oFormat)
    # note there is also nuke.Format.setWidth(oFormat)
    return ResX


def getResY():
    oFormat = getRenderOpts()
    ResY = nuke.Format.height(oFormat)
    # note there is also nuke.Format.setHeight(oFormat)
    return ResY


def getExtension():
    ext = getSceneFullPath()[getSceneFullPath().find(".") :]
    return ".nk"


def getPixelRatio():
    oFormat = getRenderOpts()
    pixRatio = nuke.Format.pixelAspect(oFormat)
    return pixRatio


def getDeviceAspectRatio():
    # resX/resY?
    return 1


def getStartFrame():
    StartFrame = nuke.toNode("root").knob("first_frame").value()
    return StartFrame


def getEndFrame():
    EndFrame = nuke.toNode("root").knob("last_frame").value()
    return EndFrame


def getStepBy():
    StepBy = 1
    return StepBy


def getScenePath():
    return os.path.split(getSceneFullPath())[0]


def getSceneFullPath():
    return nuke.toNode("root").knob("name").value()


def getSceneName():
    return os.path.split(getSceneFullPath())[1]


def getSceneCleanName():
    return getSceneName().split(".")[0]


def getTimeSliderRange():
    return (getStartFrame(), getEndFrame())


def hasChanged():
    return nuke.Root().modified()


def saveAs(*args):
    args = cleanArgs(args)
    outputFileName = args[0]
    nuke.scriptSaveAs(outputFileName)


def setRenderPaths(*args):
    args = cleanArgs(args)
    outPath = args[0]
    selWrites = nuke.selectedNodes("Write")

    selWrites.reverse()
    for eachNode in selWrites:
        eachNode.setSelected(False)

    for eachNode in selWrites:
        ext = "exr"
        if eachNode.knob("file").value():
            match = re.search(".*\.(\w+)", eachNode.knob("file").value())
            if match:
                ext = match.groups(1)[0]
                print(ext)

        eachNode.knob("file").setValue(outPath + r".%04d." + ext)
        eachNode.knob("label").setValue(os.path.basename(os.path.dirname(outPath)))

    for eachNode in selWrites:
        eachNode.setSelected(True)

    return


def createReadNode(*args):
    args = cleanArgs(args)
    infoDict = args[0]
    readNode = nuke.nodes.Read()
    readNode.knob("file").setValue(infoDict["file"])
    readNode.knob("on_error").setValue(1)  # black on missing frames
    readNode.knob("first").setValue(int(infoDict["first"]))
    readNode.knob("last").setValue(int(infoDict["last"]))

    return readNode


def getWritePath(*args):
    args = cleanArgs(args)
    eachPass = args[0]
    numsearch = re.search(".*[\.|_](\d+)\.", eachPass["importFrame"])
    frameNum = "0101"
    if numsearch:
        frameNum = numsearch.group(1)
    return (
        eachPass["importFrame"]
        .replace(frameNum, "%04d")
        .replace(
            ("/" + eachPass["version"] + "/"),
            ("/" + eachPass["version"] + eachPass["imageTag"] + "/"),
        )
    )


def getNukeFrameNumbers(digits):
    """
    return the size of nuke 'frame number variable'

    input:
      %04
      ###
    """
    if "#" in digits:
        return digits.count("#")
    else:
        return int("".join(i for i in digits if i.isdigit()))


def refreshNode(*args):
    args = cleanArgs(args)
    strNode = args[0]
    n = nuke.toNode(strNode)
    x = int(n.knob("tile_color").getValue())
    n.knob("tile_color").setValue(0)
    n.knob("tile_color").setValue(x)
    n.knob("file").setFlag(nuke.INVISIBLE)
    n.knob("file").clearFlag(nuke.INVISIBLE)


def nodePaste(*args):
    args = cleanArgs(args)
    file = args[0]
    nuke.nodePaste(file)


def cleanArgs(args):
    if type(args[0]) == list and len(args) == 1:
        return args[0]
    else:
        return args


def paddingSplit(file_name):
    """
    This will break up a sting that describes
    a frame range into component pieces.

    input: <string>
    output: <tuple>; (int,string,string)

    Example:
    print paddingSplit("colorbars.%04d.sgi")
    (4,"colorbars.",".sgi")
    """
    file_name = file_name.strip()

    padding = 0
    prefix = file_name
    suffix = None

    m1 = re.search("^(.+)%(\d+)d(.+)$", file_name)
    m2 = re.search("^(.+)(#+)(,+)$", file_name)
    if m1:
        prefix = m1.group(1)
        padding = int(m1.group(2))
        suffix = m1.group(3)
    elif m2:
        prefix = m2.group(1)
        padding = m2.group(2).count("#")
        suffix = m2.group(3)
    return (padding, prefix, suffix)


def reload_lib(mylib):
    importlib.reload(mylib)
