def unique(a):
    """
    return the list with duplicate elements removed
    """
    return list(set(a))


def intersect(a, b):
    """
    return the intersection of two lists
    """
    return list(set(a) & set(b))


def union(a, b):
    """
    return the union of two lists
    """
    return list(set(a) | set(b))


def difference(a, b):
    """
    show whats in list b which isnt in list a
    """
    return list(set(b).difference(set(a)))


import re

_NATURAL_SPLIT_RE = re.compile(r'(\d+)')


def natural_sort_key(s):
    """Sort key for natural (human-friendly) ordering.
    Case-insensitive, numerically-aware: 'Node2' before 'Node10'.
    """
    parts = _NATURAL_SPLIT_RE.split(str(s).lower())
    return [int(part) if part.isdigit() else part for part in parts]


def priority_sort_key(head=None, tail=None):
    """Return a sort key that pins head items first and tail items last,
    with everything else natural-sorted in between.

    Usage: sorted(items, key=priority_sort_key(head=["file","edit"], tail=["other"]))
    """
    head = head or []
    tail = tail or []
    head_map = {item.lower(): i for i, item in enumerate(head)}
    tail_map = {item.lower(): i for i, item in enumerate(tail)}

    def _key(s):
        s_lower = str(s).lower()
        if s_lower in head_map:
            return (0, head_map[s_lower], [])
        if s_lower in tail_map:
            return (2, tail_map[s_lower], [])
        return (1, 0, natural_sort_key(s))

    return _key
