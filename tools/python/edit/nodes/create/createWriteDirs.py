import os, platform, stat
import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
    "Create/Create Write Dirs": {
        "cmd": "createWriteDirs(nuke.selectedNodes())",
        "hotkey": "#+w",
        "icon": "",
    }
}


def createWriteDirs(nodes=[]):
    """
    Makes directories for selected write nodes
    """
    # if no nodes are specified then look for selected nodes
    if not nodes:
        nodes = nuke.selectedNodes()

    # if nodes is still empty no nodes are selected
    if not nodes:
        nuke.message("ERROR: No node(s) selected.")
        return

    EXISTING = []

    for node in nodes:
        _class = node.Class()
        if _class == "Write":
            path = nuke.filename(node)

            if path is None:
                nuke.tprint("No path attribute.")
                continue
            root_path = os.path.dirname(path)

            if os.path.exists(root_path) == True:
                nuke.tprint("Path Exists: {}".format(root_path))
            try:
                os.mkdir(root_path)
                os.chmod(root_path, 0o0755)
                nuke.tprint("Path created: {}".format(root_path))
            except:
                if nuke.ask("Create Path?\n {}".format(root_path)):
                    os.makedirs(root_path)
                    os.chmod(root_path, 0o0775)
                    nuke.tprint("Path created: {}".format(root_path))
                else:
                    nuke.tprint("Path creation cancelled for: {}".format(root_path))
    return
