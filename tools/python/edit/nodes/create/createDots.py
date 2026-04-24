from collections import OrderedDict

import nuke

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"

__menus__ = {
    "Create/Create Dots": {
        "cmd": "createDots(nuke.selectedNodes())",
        "hotkey": "#.",
        "icon": "",
    }
}


def createDots(nodes):
    """Insert / reposition dots upstream of each selected node with
    perpendicular L-shaped routing.

    Multi-selection forking: when two or more selected nodes share the
    same effective upstream (two Grades feeding from one Read, say), the
    tool consolidates the fork onto ONE shared dot directly below the
    upstream. Any existing per-branch dots that become redundant are
    deleted. Each branch whose column is far from the shared dot then
    gets its own routing dot so the side pipe is perpendicular; branches
    already near the shared-dot column connect directly (a short
    near-vertical pipe isn't worth inserting a dot on).

    Single-branch routing chooses one of three placements:

      * Column-aligned upstream and downstream (horizontal offset smaller
        than either node's width): midpoint dot on the downstream's
        column, halfway between the two — either L-shape would plant the
        dot inside a node's body.
      * Source-type upstream (no connected inputs): dot directly below
        the source on its own column, at the downstream's row.
      * Mid-graph upstream: dot directly above the downstream on its
        column, at the upstream's row.

    Reuse: a Dot whose only dependent is the selected node is repositioned
    in place rather than stacked under another dot. Re-running the tool
    on an already-routed graph is idempotent.

    Write-class nodes always take the main-input path even when a
    mask/AOV input is connected. Mask-input routing is a separate B-side
    dot at the mask source's column, at the downstream's row.

    All offsets use live screenWidth/screenHeight so placement respects
    the Dot-size preference.
    """
    main_nodes = []
    mask_nodes = []
    for node in nodes:
        A = node.input(0)
        if A is None:
            continue
        B = None if node.Class().startswith("Write") else node.input(1)
        if B:
            mask_nodes.append(node)
        else:
            main_nodes.append(node)

    # Group main-input nodes by effective upstream so multiple selected
    # nodes feeding from the same source share a single dot.
    groups = OrderedDict()
    for node in main_nodes:
        upstream = _effective_upstream_of_main_input(node)
        if upstream is None:
            continue
        entry = groups.setdefault(id(upstream), (upstream, []))
        entry[1].append(node)

    for upstream, members in groups.values():
        if len(members) > 1:
            _route_shared_main(upstream, members)
        else:
            _route_single_main(members[0])

    for node in mask_nodes:
        _route_mask(node)


def _effective_upstream_of_main_input(node):
    """Return the upstream for grouping purposes, unwrapping a reusable
    per-branch Dot so that two nodes each with their own per-branch dot
    still group together when those dots share a grandparent."""
    A = node.input(0)
    if A is None:
        return None
    if A.Class() == "Dot" and _only_dependent(A, node):
        up = A.input(0)
        if up is not None:
            return up
    return A


def _route_single_main(node):
    A = node.input(0)
    if A is None:
        return
    # Skip nodes that are already column-aligned with their effective
    # upstream — a new dot on a near-vertical pipe would only land in
    # midpoint mode and serve no routing purpose.
    effective_upstream = _effective_upstream_of_main_input(node)
    if effective_upstream is not None and _pipe_already_perpendicular(
        effective_upstream, node
    ):
        return
    dot, upstream = _get_or_make_dot(A, node, input_index=0)
    if upstream is None:
        return
    _place_single_main_dot(dot, upstream, node)


def _pipe_already_perpendicular(upstream, node):
    """True when a dot between `upstream` and `node` would fall back to
    midpoint placement — i.e. both L-shapes would overlap a node body.
    In that case the pipe is effectively vertical and inserting a dot
    serves no routing purpose."""
    dx = abs(
        (upstream.xpos() + upstream.screenWidth() // 2)
        - (node.xpos() + node.screenWidth() // 2)
    )
    # Nuke's default Dot is 12 wide; we haven't made one yet so use the
    # default as the reference. This mirrors the overlap math inside
    # _place_single_main_dot.
    dot_w = 12
    source_overlaps = dx < (node.screenWidth() + dot_w) // 2
    midgraph_overlaps = dx < (upstream.screenWidth() + dot_w) // 2
    return source_overlaps and midgraph_overlaps


def _place_single_main_dot(dot, upstream, node):
    nodeXpos = node.xpos()
    nodeYpos = node.ypos()
    nodeWidth = node.screenWidth()
    nodeHeight = node.screenHeight()
    uXpos = upstream.xpos()
    uYpos = upstream.ypos()
    uWidth = upstream.screenWidth()
    uHeight = upstream.screenHeight()
    dotW = dot.screenWidth()
    dotHalfW = dotW // 2
    dotHalfH = dot.screenHeight() // 2

    dx = abs((uXpos + uWidth // 2) - (nodeXpos + nodeWidth // 2))
    # Source mode puts the dot at upstream's column — it would plant the dot
    # inside the downstream body when the X extents overlap.
    source_overlaps = dx < (nodeWidth + dotW) // 2
    # Mid-graph puts the dot at downstream's column — similarly overlaps
    # the upstream body when their X extents overlap.
    midgraph_overlaps = dx < (uWidth + dotW) // 2

    prefer_source = upstream.inputs() == 0

    if prefer_source and not source_overlaps:
        dot.setXYpos(
            uXpos + uWidth // 2 - dotHalfW,
            nodeYpos + nodeHeight // 2 - dotHalfH,
        )
    elif not midgraph_overlaps:
        dot.setXYpos(
            nodeXpos + nodeWidth // 2 - dotHalfW,
            uYpos + uHeight // 2 - dotHalfH,
        )
    elif not source_overlaps:
        # Mid-graph would overlap upstream but source doesn't overlap the
        # downstream — use source mode as a fallback even when upstream
        # isn't strictly a source-type node.
        dot.setXYpos(
            uXpos + uWidth // 2 - dotHalfW,
            nodeYpos + nodeHeight // 2 - dotHalfH,
        )
    else:
        # Both L-modes would overlap a node body: midpoint fallback.
        dot.setXYpos(
            nodeXpos + nodeWidth // 2 - dotHalfW,
            (uYpos + uHeight + nodeYpos) // 2 - dotHalfH,
        )


def _route_shared_main(upstream, members):
    """Consolidate `members` onto a single shared dot below `upstream`,
    then add per-branch routing dots for each member whose column isn't
    already near the shared dot.
    """
    if upstream.Class() == "Dot":
        # Upstream is itself the shared fork already — just reposition.
        up_of_dot = upstream.input(0)
        if up_of_dot is None:
            return
        shared_dot = upstream
        _place_shared_main_dot(shared_dot, up_of_dot, members)
    else:
        shared_dot, orphan_candidates = _consolidate_shared_main_dot(
            upstream, members
        )
        _place_shared_main_dot(shared_dot, upstream, members)
        for d in orphan_candidates:
            if not d.dependent(nuke.INPUTS, forceEvaluate=False):
                nuke.delete(d)

    # Branch-side routing: for each member whose column is far enough from
    # the shared dot that a direct pipe would be obviously diagonal, call
    # the single-node logic to add a per-branch routing dot. Members that
    # are already column-aligned with the shared dot connect directly.
    for node in members:
        if not _column_aligned(shared_dot, node):
            _route_single_main(node)


def _consolidate_shared_main_dot(upstream, members):
    """Find/create the shared dot between `upstream` and `members`; rewire
    each member's main input through it. Returns (shared_dot, list_of_
    previous_per_branch_dots_that_may_now_be_orphaned)."""
    members_set = set(members)
    existing = upstream.dependent(nuke.INPUTS, forceEvaluate=False)
    # A Dot child of `upstream` is safe to promote to the shared-fork role
    # only when its own dependents are a subset of our selected members —
    # promoting one that also feeds an unrelated branch would silently
    # change that branch's routing.
    candidates = [
        d for d in existing
        if d.Class() == "Dot"
        and set(d.dependent(nuke.INPUTS, forceEvaluate=False)).issubset(members_set)
    ]

    if candidates:
        shared_dot = candidates[0]
        orphan_candidates = list(candidates[1:])
    else:
        shared_dot = nuke.nodes.Dot()
        shared_dot.setInput(0, upstream)
        orphan_candidates = []

    for node in members:
        current = node.input(0)
        if current is shared_dot:
            continue
        node.setInput(0, shared_dot)
        if (current is not None
                and current.Class() == "Dot"
                and current is not shared_dot
                and current not in orphan_candidates):
            orphan_candidates.append(current)

    return shared_dot, orphan_candidates


def _place_shared_main_dot(dot, upstream, members):
    uXpos = upstream.xpos()
    uYpos = upstream.ypos()
    uWidth = upstream.screenWidth()
    uHeight = upstream.screenHeight()
    dotHalfW = dot.screenWidth() // 2
    dotHalfH = dot.screenHeight() // 2
    topmost_y = min(n.ypos() for n in members)
    dot.setXYpos(
        uXpos + uWidth // 2 - dotHalfW,
        (uYpos + uHeight + topmost_y) // 2 - dotHalfH,
    )


def _route_mask(node):
    A = node.input(0)
    B = node.input(1)
    if B is None:
        return
    nodeXpos = node.xpos()
    nodeYpos = node.ypos()
    nodeWidth = node.screenWidth()
    nodeHeight = node.screenHeight()
    dot, upstream = _get_or_make_dot(B, node, input_index=1)
    if upstream is None:
        return
    dotHalfW = dot.screenWidth() // 2
    dotHalfH = dot.screenHeight() // 2
    dot.setXYpos(
        upstream.xpos() + upstream.screenWidth() // 2 - dotHalfW,
        nodeYpos + nodeHeight // 2 - dotHalfH,
    )
    if A is not None and A.Class() == "Dot":
        node.knob("xpos").setValue(
            A.xpos() + A.screenWidth() // 2 - nodeWidth // 2
        )
    elif A is not None:
        node.knob("xpos").setValue(A.xpos())


def _column_aligned(upstream, node):
    """True when a branch dot for `node` would visually stack on `upstream`.
    Only then is it safe to skip the per-branch routing dot; anywhere
    outside the upstream's own X footprint there's room for the branch
    dot to sit cleanly at node's column."""
    dx = abs(
        (upstream.xpos() + upstream.screenWidth() // 2)
        - (node.xpos() + node.screenWidth() // 2)
    )
    return dx < upstream.screenWidth()


def _get_or_make_dot(candidate, downstream, input_index):
    """Return (dot, effective_upstream). If `candidate` is already a Dot
    whose only dependent is `downstream`, reuse it in place (effective
    upstream is the dot's own input(0); caller should skip if None).
    Otherwise create a new Dot wired between `candidate` and `downstream`.
    """
    if candidate.Class() == "Dot" and _only_dependent(candidate, downstream):
        return candidate, candidate.input(0)
    dot = nuke.nodes.Dot()
    dot.setInput(0, candidate)
    downstream.setInput(input_index, dot)
    return dot, candidate


def _only_dependent(candidate, downstream):
    """True iff `downstream` is the single node depending on `candidate`."""
    deps = candidate.dependent(nuke.INPUTS, forceEvaluate=False)
    return len(deps) == 1 and deps[0] is downstream
