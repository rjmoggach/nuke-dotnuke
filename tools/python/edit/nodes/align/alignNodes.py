import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
    "Edit/Nodes/Align/Horizontal/Middle": {
        "cmd": "alignNodes(nuke.selectedNodes())",
        "hotkey": "#x",
        "icon": "",
    },
    "Edit/Nodes/Align/Vertical/Middle": {
        "cmd": 'alignNodes(nuke.selectedNodes(), "y")',
        "hotkey": "#y",
        "icon": "",
    },
}


def alignNodes(nodes, direction="x"):
    """
    Align nodes either horizontally or vertically.
    Aligns by node center to handle varying node sizes (e.g. Dot nodes).
    """
    if len(nodes) < 2:
        return
    if direction.lower() not in ("x", "y"):
        raise ValueError("direction argument must be x or y")

    if direction == "x":
        centers = [float(n.xpos() + n.screenWidth() / 2) for n in nodes]
        avgCenter = sum(centers) / len(centers)
        for n in nodes:
            n.setXpos(int(avgCenter - n.screenWidth() / 2))
    else:
        centers = [float(n.ypos() + n.screenHeight() / 2) for n in nodes]
        avgCenter = sum(centers) / len(centers)
        for n in nodes:
            n.setYpos(int(avgCenter - n.screenHeight() / 2))

    return avgCenter
