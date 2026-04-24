"""Simple Path Toggle: ad-hoc two-prefix path swap for Nuke.

Portable NoOp node with a single Toggle Paths button and two user-entered
prefixes. Direction is auto-detected per click: whichever side the majority
of matching paths are on, the click flips to the other. Useful for bringing
a script between home and work, a shared drive and a local copy, or any
one-off prefix pair.

Public API:
    create()        build a new Simple Path Toggle NoOp in the graph
    toggle(node)    swap paths on the given Simple Path Toggle node

Built as a NoOp rather than a .gizmo for portability: a gizmo-backed node
stored in a .nk can't open on a box without the gizmo dir on NUKE_PATH.
A NoOp with user knobs serialises fully into the .nk.
"""

from __future__ import print_function

import sys

import nuke

# Register in __main__ so the Toggle Paths PyScript_Knob on spawned NoOps can
# resolve `togglePath` by bare name — mynk loads this file via imp.load_source
# as module `togglePath`, but PyScript_Knob callbacks eval in __main__.
import __main__
__main__.__dict__["togglePath"] = sys.modules[__name__]

__menus__ = {
    "File/Simple Path Toggle": {
        "cmd": "create()",
        "hotkey": "",
        "icon": "",
    },
}


def create():
    """Build and return a new Simple Path Toggle NoOp, registered in the graph."""
    node = nuke.createNode("NoOp", inpanel=False)
    node["name"].setValue("SimplePathToggle1")
    node["label"].setValue("Simple\nPath Toggle")
    node["tile_color"].setValue(0x339966FF)

    node.addKnob(nuke.Tab_Knob("tab_main", "Path Toggle"))
    node.addKnob(
        _button(
            "toggle",
            "Toggle Paths",
            "togglePath.toggle(nuke.thisNode())",
        )
    )
    status = nuke.Text_Knob("status", " ")
    status.setValue("Fill in both prefixes and click Toggle Paths.")
    node.addKnob(status)
    node.addKnob(
        nuke.Text_Knob(
            "hdr",
            "",
            "Two prefixes. Click toggles paths from whichever side is current.",
        )
    )
    node.addKnob(nuke.String_Knob("path_a", "Path A"))
    node.addKnob(nuke.String_Knob("path_b", "Path B"))
    return node


def toggle(node):
    """Swap file-knob paths between Path A and Path B.

    Target-set rule:
        - any nodes selected (other than this panel) -> rewrite those only
        - nothing selected                           -> rewrite every node

    Direction = away from the current majority. If most matching paths are
    on Path A, we convert to Path B, and vice versa.
    """
    a = node["path_a"].value().strip()
    b = node["path_b"].value().strip()
    if not a or not b:
        nuke.message("Simple Path Toggle: fill in both Path A and Path B first.")
        return

    pairs = [(a, b)]
    a_count, b_count = _count_state(node, pairs)
    if a_count == 0 and b_count == 0:
        _set_status(node, "No paths matching either prefix found.")
        if nuke.GUI:
            nuke.message(
                "Simple Path Toggle: no paths starting with Path A or Path B."
            )
        return

    direction = "a2b" if a_count >= b_count else "b2a"
    _swap(node, pairs, direction)
    _refresh_status(node)


# -- Internals ----------------------------------------------------------------
def _button(name, label, python_code):
    btn = nuke.PyScript_Knob(name, label, python_code)
    btn.setFlag(nuke.STARTLINE)
    return btn


def _swap(node, pairs, direction):
    targets, scope = _target_nodes(node)
    changed = 0
    unchanged = 0
    with nuke.Undo():
        nuke.Undo().name("Simple Path Toggle {0}".format(direction))
        for target in targets:
            if target is node:
                continue
            for knob in _iter_file_knobs(target):
                old = knob.value() or ""
                new = _rewrite_one(old, pairs, direction)
                if new is None:
                    continue
                if new == old:
                    unchanged += 1
                    continue
                knob.setValue(new)
                changed += 1

    msg = "Simple Path Toggle ({0}, {1} nodes): rewrote {2} path(s); {3} already-correct.".format(
        direction,
        scope,
        changed,
        unchanged,
    )
    print(msg)
    if nuke.GUI:
        nuke.message(msg)


def _refresh_status(node):
    a = node["path_a"].value().strip()
    b = node["path_b"].value().strip()
    if not a or not b:
        _set_status(node, "Fill in both prefixes.")
        return
    a_count, b_count = _count_state(node, [(a, b)])
    if a_count == 0 and b_count == 0:
        _set_status(node, "No paths match either prefix.")
    elif a_count >= b_count:
        _set_status(
            node,
            "Paths are on Path A ({0}A / {1}B). Click to convert to Path B.".format(
                a_count, b_count
            ),
        )
    else:
        _set_status(
            node,
            "Paths are on Path B ({0}A / {1}B). Click to convert to Path A.".format(
                a_count, b_count
            ),
        )


def _set_status(node, text):
    knob = node.knobs().get("status")
    if knob is not None:
        knob.setValue(text)


def _count_state(node, pairs):
    """Return (a_count, b_count) match counts across the target set."""
    a_total = 0
    b_total = 0
    targets, _ = _target_nodes(node)
    for target in targets:
        if target is node:
            continue
        for knob in _iter_file_knobs(target):
            value = (knob.value() or "").replace("\\", "/")
            if not value:
                continue
            for a_pfx, b_pfx in pairs:
                a_n = _normalise_prefix(a_pfx)
                b_n = _normalise_prefix(b_pfx)
                if value.startswith(a_n):
                    a_total += 1
                    break
                if value.startswith(b_n):
                    b_total += 1
                    break
    return a_total, b_total


def _target_nodes(panel_node):
    sel = [n for n in nuke.selectedNodes() if n is not panel_node]
    if sel:
        return sel, "selected"
    return nuke.allNodes(recurseGroups=True), "all"


def _iter_file_knobs(node):
    for name in node.knobs():
        knob = node[name]
        if isinstance(knob, nuke.File_Knob):
            yield knob


def _normalise_prefix(p):
    """Canonical form: forward slashes, exactly one trailing slash.

    Prevents false-matches like ``/home/user/proj`` matching
    ``/home/user/project_archive/...``.
    """
    return p.replace("\\", "/").rstrip("/") + "/"


def _rewrite_one(value, pairs, direction):
    """Return rewritten value, or None if no prefix matched.

    Always emits forward slashes — Nuke .nk files are TCL-serialised and
    backslashes are escape characters there, so saving a path like
    ``Z:\proj\foo`` breaks on reload.
    """
    if not value:
        return None
    norm = value.replace("\\", "/")
    for a, b in pairs:
        src = _normalise_prefix(a if direction == "a2b" else b)
        dst = _normalise_prefix(b if direction == "a2b" else a)
        if norm.startswith(src):
            tail = norm[len(src) :]
            return dst + tail
    return None
