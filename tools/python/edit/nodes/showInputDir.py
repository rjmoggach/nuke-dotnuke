import nuke
import os
import subprocess
import platform

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

NAUTILUS_CMD = "/usr/bin/nautilus"
KONQUEROR_CMD = "/usr/bin/konqueror"
MACOSX_CMD = "open"
WINDOWS_CMD = "explorer"
MAX_NODES = 4

if platform.system() == "Linux":
    if os.path.exists(NAUTILUS_CMD):
        BROWSER = "Nautilus"
        BROWSER_CMD = NAUTILUS_CMD
    elif os.path.exists(KONQUEROR_CMD):
        BROWSER = "Konqueror"
        BROWSER_CMD = KONQUEROR_CMD
    else:
        BROWSER = "Browser"
        BROWSER_CMD = "xdg-open"
elif platform.system() == "Darwin":
    BROWSER = "Finder"
    BROWSER_CMD = MACOSX_CMD
else:
    BROWSER = "Explorer"
    BROWSER_CMD = WINDOWS_CMD


__menus__ = {
    "Edit/Nodes/Show in {0}".format(BROWSER): {
        "cmd": "showInputDir(nuke.selectedNodes())",
        "hotkey": "#r",
        "icon": "",
    }
}


def showInputDir(nodes=[]):
    print("TEST")
    """
  function that shows a file browser window
  for the directory in a read or write node
  """
    # if no nodes are specified then look for selected nodes
    if not nodes:
        nodes = nuke.selectedNodes("Read") + nuke.selectedNodes("Write")

    # if nodes is still empty no nodes are selected
    if not nodes:
        nuke.message("ERROR: No node(s) selected.")
        return

    if len(nodes) > MAX_NODES:
        confirm = nuke.ask(
            "Are you sure you want to open {0} {1} windows?".format(len(nodes), BROWSER)
        )
        if not confirm:
            return

    for node in nodes:
        _class = node.Class()
        if not _class == "Write" or not _class == "Read":
            continue
        else:
            path = nuke.filename(node)
            if path is None:
                continue
            if path[-1:] == "/":
                path = path[:-1]
            root_path = os.path.dirname(os.path.dirname(path))
        node["selected"].setValue(False)

        try:
            path = i["file"].evaluate().split("/")[:-1]
            root_path = "/".join(getPath)
            if platform.system() == "Windows":
                root_path = root_path.replace("/", "\\")
                print('{0} "{1}"'.format(BROWSER_CMD, root_path))
                subprocess.Popen('{0} "{1}"'.format(BROWSER_CMD, root_path))
            else:
                subprocess.Popen([BROWSER_CMD, root_path])
        except:
            continue

    return
