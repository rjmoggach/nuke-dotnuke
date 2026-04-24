# nuke-dotnuke 🎬

Personal startup environment for Nuke — GUI / authoring enhancements only, zero impact on rendering.

## Installation

Clone this repo in place of your `.nuke` folder:

```bash
git clone git@github.com:rjmoggach/nuke-dotnuke.git ~/.nuke
```

## Structure

```
.nuke/
  init.py                 # Non-GUI initialization
  menu.py                 # GUI initialization, loads mynk + tools
  mynk/                   # Core library
    config.py             # Config management (ConfigObj)
    constants.py          # Path constants
    gui.py                # Menu / toolbar builder
    tools.py              # Tool discovery and loading
    gizmos.py             # Gizmo path manager and menu builder
    formats.py            # Format management
    knobs.py              # Knob defaults from config
    logger.py             # Logging with optional colorlog
    listUtils.py          # Natural sort / priority sort utilities
    data/defaults.cfg     # Default configuration
  tools/
    python/               # Python tools (auto-discovered → menus)
      color/              # Colorspace helpers
        set_colorspace.py       # Batch-set colorspace on Reads/Writes (OCIO aware)
      file/                     # File operations
        togglePath.py           # Two-prefix path toggle NoOp
        animVersUpdate.py, archive.py, revealInFolder.py, ...
      edit/                     # Edit operations
        pasteToSelected.py      # Paste into pipe on selected nodes
        setLabel.py             # Quick label editor
        setStartAt.py           # Set start frame
        classDisable.py         # Toggle disable by node class
        togglePanel.py          # Toggle effect panels
        nodes/
          align/
            alignNodes.py       # Center-align H/V
            mirrorNodes.py      # Mirror around topmost selected node
          create/
            createDots.py       # Perpendicular-routing dot inserter
            createLinks.py, createReadFromWrite.py,
            createWrite.py, createWriteDirs.py, ...
          kiss.py               # Auto-connect nearby nodes
      camera/, channel/, time/, transform/, other/
      W/                        # Wouter Gilsing tools
        W_hotbox.py (v2.0), W_hotboxManager.py (v2.0),
        W_smartAlign.py, W_scaleTree.py (v2.2),
        W_backdropper.py (v1.2), W_moveMenu.py
      _builtins.py              # Built-in menu entries + Reload MyNk
    gizmos/                     # Custom gizmos (auto-discovered)
```

## Menu Structure

Tools are auto-discovered from `tools/python/` and added to the **MyNk** menu:

- **File** — File operations, path toggle, write descriptor updates
- **Edit** — Paste to selected, labels, node align / create / kiss
  - `Nodes/Align/Horizontal/{Left, Middle, Right, Mirror}`
  - `Nodes/Align/Vertical/{Top, Middle, Bottom, Mirror}`
  - `Nodes/Kiss`, `Toggle Class Disable`, `Toggle Effects Panel`
- **Create** — Dots, Links, Read/Write creation helpers
- **Color** — `Set Colorspace`
- **Camera, Channel, Time, Transform** — naturally sorted
- **Other** — miscellaneous
- _(separator)_
- **Reload MyNk** — rebuild the entire mynk environment

### Sort order

Menu ordering applies head / tail priority plus natural (case-insensitive, numeric-aware) sort to **every** segment of a `/`-separated path — not just the top-level. Pinned heads: `File, Edit, Create`. Pinned tails: `Other, Reload MyNk`. Underscore-prefixed modules sort to the end.

Individual entries can opt out with two optional fields in their `__menus__` dict:

- `order: <int>` — pin a leaf below its sorted siblings (used to keep `Flood Red / Green / Blue / Alpha` in logical order).
- `separator_before: True` — emit a horizontal rule before this entry (used ahead of `Reload MyNk`).

Hotkeys render in the menubar only; the node toolbar mirrors the same commands without the shortcut label so Nuke's last-wins binding stays pinned to the menubar.

## Authoring a Tool

Drop a `.py` anywhere under `tools/python/` and declare a `__menus__` dict:

```python
__menus__ = {
    "Create/My Tool": {
        "cmd": "my_func()",
        "hotkey": "#+m",
        "icon": "",
        "order": 10,                # optional
        "separator_before": False,  # optional
    },
}

def my_func():
    ...
```

The key is the full menu path; the command is bound relative to the module's dotted path unless it starts with `nuke`. Sub-directories become sub-menus automatically. Nested modules just work.

## Notable Tools ⚡

- **`createDots`** (`#.`) — inserts / repositions dots upstream of selected nodes with L-shaped perpendicular routing. Multi-branch forks consolidate onto one shared dot below the source; per-branch routing dots only appear when a column offset demands them. Existing dots whose sole dependent is the selected node are repositioned in place, so the tool is idempotent on re-run. Respects the global Dot-size preference. Write-class nodes always get a dot above (never beside).
- **`mirrorNodes`** (`Shift+X`, `Shift+Y`) — reflects the selection around the **topmost** selected node in the input chain, so the head of the branch stays put while the downstream graph flips.
- **`set_colorspace`** — OCIO-aware batch colorspace setter with cascading enum dropdown, including a `Raw Data` checkbox that applies `raw=True` to Reads (Writes are skipped with a note). Undo-wrapped.
- **`togglePath`** — spawns a portable NoOp with two prefix fields and a single `Toggle Paths` button. Stored inside `.nk` files (no gizmo dep), direction auto-detects per click.

## Logging 🪵

`mynk` initialises a dedicated `MyNk` logger with format:

```
LEVEL [MyNk] filename.ext message
```

If `colorlog` is installed, the level is coloured; otherwise the plain `logging` formatter is used. The logger has `propagate=False` so Nuke's root logger doesn't re-emit records in its default `INFO:MyNk:` format.

## Design Principles

- Empower users to define their workflow, don't prescribe it
- Enhancements should be transparent and just work
- Fail gracefully when custom dependencies break
- Keep convenience functions separate from mission-critical logic
- Changes to expected behaviour are opt-in
- Keep the original UI intact

## Requirements

- Nuke 14+ (Python 3)
- PySide2 (Nuke < 16) or PySide6 (Nuke 16+)
- Optional: `colorlog` for coloured log output

## Configuration

User config is managed via `mynk.cfg` (gitignored) which overrides `mynk/data/defaults.cfg`. Settings include custom formats, knob defaults, and tool paths.
