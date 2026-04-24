import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
    "Edit/Nodes/Align/Horizontal/Mirror": {
        "cmd": "mirrorNodes(nuke.selectedNodes())",
        "hotkey": "#+x",
        "icon": "",
    },
    "Edit/Nodes/Align/Vertical/Mirror": {
        "cmd": 'mirrorNodes(nuke.selectedNodes(), "y")',
        "hotkey": "#+y",
        "icon": "",
    },
}


def mirrorNodes(nodes, direction="x"):
    """Mirror selected nodes across an axis set by the topmost node.

    The pivot is the upstream-most selected node — the one with no
    ancestors (via the input chain, at any depth) among the selection.
    Its X center (for `direction="x"`) or Y center (for `direction="y"`)
    becomes the mirror axis, so the head of the branch stays put while
    everything downstream of it flips.
    """
    if len(nodes) < 2:
        return
    direction = direction.lower()
    if direction not in ("x", "y"):
        raise ValueError("direction argument must be x or y")

    pivot = _find_topmost_node(nodes)
    if direction == "x":
        axis = pivot.xpos() + pivot.screenWidth() / 2.0
    else:
        axis = pivot.ypos() + pivot.screenHeight() / 2.0

    for n in nodes:
        if direction == "x":
            center = n.xpos() + n.screenWidth() / 2.0
            n.setXpos(int(n.xpos() - 2 * (center - axis)))
        else:
            center = n.ypos() + n.screenHeight() / 2.0
            n.setYpos(int(n.ypos() - 2 * (center - axis)))


def _find_topmost_node(nodes):
    """Return the first node in `nodes` that has no other selected node as
    an ancestor via the input chain."""
    node_set = set(nodes)
    for n in nodes:
        if not _has_selected_ancestor(n, node_set):
            return n
    return nodes[0]


def _has_selected_ancestor(node, node_set):
    """Walk up `node`'s input chain — returns True if any ancestor (any
    depth) is a member of `node_set` besides `node` itself."""
    seen = set()
    stack = []
    for i in range(node.inputs()):
        parent = node.input(i)
        if parent is not None:
            stack.append(parent)
    while stack:
        cur = stack.pop()
        name = cur.fullName()
        if name in seen:
            continue
        seen.add(name)
        if cur in node_set and cur is not node:
            return True
        for i in range(cur.inputs()):
            parent = cur.input(i)
            if parent is not None:
                stack.append(parent)
    return False
