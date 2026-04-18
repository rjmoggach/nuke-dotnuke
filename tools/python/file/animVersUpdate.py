import os
import nuke

__menus__ = {
    "File/Update Write Descriptors": {
        "cmd": "anim_vers_update()",
        "hotkey": "",
        "icon": "",
    }
}


def anim_vers_update():
    """Update Descriptor knobs on all Write nodes based on the selected node's filename.

    Extracts the version/name portion from the selected node's file path
    (underscore-separated elements from position 3 onwards) and applies it
    to the Descriptor knob on all Write nodes.
    """
    try:
        sel = nuke.selectedNode()
    except ValueError:
        nuke.message("Please select a node with a file knob.")
        return

    filepath = nuke.filename(sel)
    if not filepath:
        nuke.message("Selected node has no file path.")
        return

    # Extract name portion: split filename by underscore, take elements from index 3 onwards
    basename = os.path.splitext(os.path.splitext(os.path.basename(filepath))[0])[0]
    parts = basename.split("_")
    if len(parts) > 3:
        name = "_".join(parts[3:])
    else:
        name = basename

    for node in nuke.allNodes("Write"):
        descriptor = node.knob("Descriptor")
        if descriptor is None:
            continue
        val = descriptor.value()
        if not val:
            continue
        desc_parts = val.split("_")
        if len(desc_parts) > 1:
            desc_parts[1:] = [name]
        else:
            desc_parts[0:] = [name]
        descriptor.setValue("_".join(desc_parts))
