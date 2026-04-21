import nuke

__menus__ = {
    "Edit/Toggle Class Disable": {
        "cmd": "class_disable()",
        "hotkey": "",
        "icon": "",
    }
}


def class_disable():
    """Toggle the disable knob on all nodes matching the selected node's class."""
    try:
        sel = nuke.selectedNode()
    except ValueError:
        return
    node_class = sel.Class()
    for node in nuke.allNodes():
        if node.Class() == node_class:
            node["disable"].setValue(not node["disable"].value())
