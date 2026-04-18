import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
  'Edit/Paste To Selected': {
    'cmd': 'pasteToSelected()',
    'hotkey': '#+v',
    'icon': ''
  }
}


def pasteToSelected():
    if not nuke.selectedNodes():
        try:
            nuke.nodePaste('%clipboard%')
        except RuntimeError:
            nuke.message('Nothing to paste or clipboard does not contain valid node data.')
        return

    selection = nuke.selectedNodes()

    for node in selection:
        # find all downstream connections to this node
        dependents = {}
        for dep in node.dependent():
            for i in range(dep.inputs()):
                if dep.input(i) == node:
                    dependents.setdefault(dep, []).append(i)

        # deselect everything, select only this node, then paste
        for n in nuke.allNodes():
            n['selected'].setValue(False)
        node['selected'].setValue(True)

        try:
            nuke.nodePaste('%clipboard%')
        except RuntimeError:
            nuke.message('Nothing to paste or clipboard does not contain valid node data.')
            break

        # find the pasted nodes (they are now selected)
        pasted = [n for n in nuke.selectedNodes() if n != node]
        if not pasted:
            continue

        # connect pasted node(s) input to the original node
        # find the bottom-most pasted node (lowest in the tree)
        bottom = max(pasted, key=lambda n: n.ypos())
        # find the top-most pasted node
        top = min(pasted, key=lambda n: n.ypos())

        # connect top of pasted tree to the selected node
        top.setInput(0, node)

        # reconnect downstream nodes to the bottom of pasted tree
        for dep, inputs in dependents.items():
            for i in inputs:
                dep.setInput(i, bottom)

    # restore original selection
    for n in nuke.allNodes():
        n['selected'].setValue(False)
    for node in selection:
        node['selected'].setValue(True)
