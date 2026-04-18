import nuke

__menus__ = {
    "Edit/Nodes/Toggle Effects Panel": {
        "cmd": "toggle_panel()",
        "hotkey": "",
        "icon": "",
    }
}

TOGGLE_CLASSES = {
    "Vector Blur": ["VectorBlur"],
    "Grain": ["Grain", "Grain2"],
    "Distort": ["IDistort"],
    "Blur": ["Blur"],
    "Defocus": ["Defocus"],
    "GridWarp": ["GridWarp"],
    "DirBlur": ["DirBlurWrapper"],
}


def _toggle_class(class_names):
    """Toggle disable on all nodes matching any of the given class names."""
    for node in nuke.allNodes():
        if node.Class() in class_names:
            node["disable"].setValue(not node["disable"].value())


def toggle_panel():
    """Show a panel to toggle disable on common effect node types."""
    p = nuke.Panel("Toggle Effects")
    for label in TOGGLE_CLASSES:
        p.addBooleanCheckBox(label, False)
    if not p.show():
        return
    for label, classes in TOGGLE_CLASSES.items():
        if p.value(label):
            _toggle_class(classes)
