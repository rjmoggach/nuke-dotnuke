"""set_colorspace: batch-set the colorspace knob on selected Read/Write nodes.

Public API:
    set_colorspace(value=None)
        If value is None, prompts the artist with a hierarchical dropdown
        built from the active OCIO config (families become submenus).
        Pass a specific colorspace name (e.g. "ACEScg") to apply directly,
        or pass the string "Raw Data" to toggle the raw knob on instead.

UI:
    - Uses a PythonPanel + CascadingEnumeration_Knob so '/'-separated options
      render as native submenus, matching Nuke's own colorspace knob dropdown.
    - Options are built from PyOpenColorIO's current config when available
      so the menu reflects the OCIO family hierarchy. Falls back to the
      first target's knob.values() (with " - " -> "/" normalisation) when
      PyOCIO isn't importable.
    - A separate "Raw Data" checkbox sits above the pulldown; ticking it
      greys out the pulldown and applies raw=True to Read-type nodes on
      submit (Write nodes have no raw knob — they're skipped with a note).

Scope:
    - Touches nodes whose selected knob is named ``colorspace`` (Read, ReadGeo,
      Camera) or ``output_colorspace`` (Write, DeepWrite).
    - Non-matching selected nodes are skipped silently; reported at the end.
    - Wrapped in nuke.Undo() so Ctrl+Z reverts the whole batch.
"""

from __future__ import print_function

import nuke
import nukescripts

__menus__ = {
    "Color/Set Colorspace": {
        "cmd": "set_colorspace()",
        "hotkey": "",
        "icon": "",
    },
}

_TARGET_KNOBS = ("colorspace", "output_colorspace")
_RAW_SENTINEL = "Raw Data"


def _eligible_knobs(node):
    for name in _TARGET_KNOBS:
        if name in node.knobs():
            yield node[name]


def _collect_targets():
    targets = []
    for node in nuke.selectedNodes():
        for knob in _eligible_knobs(node):
            targets.append((node, knob))
    return targets


def _ocio_options():
    """Build hierarchical 'Family/Colorspace' display strings from the active OCIO config.

    Returns (display_options, display_to_value) or (None, None) if PyOpenColorIO
    is unavailable or the config can't be loaded.
    """
    try:
        import PyOpenColorIO as ocio
    except ImportError:
        return None, None
    try:
        config = ocio.GetCurrentConfig()
    except Exception:  # noqa: BLE001
        return None, None

    mapping = {}
    displays = []
    for cs in config.getColorSpaces():
        name = cs.getName()
        family = (cs.getFamily() or "").strip().strip("/")
        display = "{0}/{1}".format(family, name) if family else name
        mapping[display] = name
        displays.append(display)
    displays.sort(key=str.lower)
    return displays, mapping


def _knob_options(knob):
    """Fallback: options from the knob itself. Returns (displays, mapping)."""
    values = list(knob.values())
    mapping = {}
    displays = []
    for v in values:
        # ACES configs surface " - " as the family separator; Enumeration_Knob
        # submenu splitting is on "/", so rewrite and keep a back-map for setValue.
        display = v.replace(" - ", "/")
        mapping[display] = v
        displays.append(display)
    return displays, mapping


class _Picker(nukescripts.PythonPanel):
    def __init__(self, options, n_targets):
        nukescripts.PythonPanel.__init__(self, "Set Colorspace")
        self.raw = nuke.Boolean_Knob("raw", "Raw Data")
        self.raw.setFlag(nuke.STARTLINE)
        self.cs = nuke.CascadingEnumeration_Knob("cs", "Colorspace", options)
        self.info = nuke.Text_Knob("info", "", "Apply to {0} node(s)".format(n_targets))
        self.addKnob(self.info)
        self.addKnob(self.cs)
        self.addKnob(self.raw)

    def knobChanged(self, knob):
        # Ticking Raw Data greys out the colorspace pulldown so the UI
        # matches the semantics: either pick a colorspace OR enable raw.
        if knob is self.raw:
            self.cs.setEnabled(not self.raw.value())


def _prompt(first_knob, n_targets):
    displays, mapping = _ocio_options()
    if not displays:
        displays, mapping = _knob_options(first_knob)
    if not displays:
        nuke.message("Set Colorspace: no colorspace options available.")
        return None

    panel = _Picker(displays, n_targets)
    if not panel.showModalDialog():
        return None
    if panel.raw.value():
        return _RAW_SENTINEL
    picked = panel.cs.value()
    return mapping.get(picked, picked)


def set_colorspace(value=None):
    """Apply a colorspace (or enable Raw Data) on selected Read/Write nodes."""
    targets = _collect_targets()
    if not targets:
        msg = "Set Colorspace: no selected nodes have a colorspace / output_colorspace knob."
        print(msg)
        if nuke.GUI:
            nuke.message(msg)
        return

    if value is None:
        _, first_knob = targets[0]
        value = _prompt(first_knob, len(targets))
        if value is None:
            return  # cancelled

    is_raw = value == _RAW_SENTINEL
    changed = 0
    skipped = []
    with nuke.Undo():
        label = "Raw Data" if is_raw else value
        nuke.Undo().name("Set Colorspace: {0}".format(label))
        for node, knob in targets:
            try:
                if is_raw:
                    if "raw" in node.knobs():
                        node["raw"].setValue(True)
                        changed += 1
                    else:
                        skipped.append(
                            "{0} ({1}): no 'raw' knob — Write-type nodes don't support Raw Data".format(
                                node.name(), node.Class()
                            )
                        )
                else:
                    # Clear raw when applying a real colorspace, otherwise the
                    # conversion is silently bypassed on a node that had raw=True.
                    if "raw" in node.knobs():
                        node["raw"].setValue(False)
                    knob.setValue(value)
                    changed += 1
            except (ValueError, TypeError) as exc:  # noqa: BLE001
                skipped.append("{0} ({1}): {2}".format(node.name(), knob.name(), exc))

    display_val = "Raw Data" if is_raw else repr(value)
    msg_lines = [
        "Set Colorspace: set {0} node(s) to {1}.".format(changed, display_val)
    ]
    if skipped:
        msg_lines.append("Skipped:")
        msg_lines.extend("  " + s for s in skipped)
    msg = "\n".join(msg_lines)
    print(msg)
    if nuke.GUI:
        nuke.message(msg)
