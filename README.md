# nuke-dotnuke

Personal startup environment for Nuke (GUI enhancements only, no impact on rendering).

## Installation

Clone this repo to replace your `.nuke` folder in your home directory:

```bash
git clone git@github.com:rjmoggach/nuke-dotnuke.git ~/.nuke
```

## Structure

```
.nuke/
  init.py              # Non-GUI initialization
  menu.py              # GUI initialization, loads mynk and tools
  mynk/                # Core library
    config.py           # Config management (ConfigObj)
    constants.py        # Path constants
    gui.py              # Menu and toolbar builder
    tools.py            # Tool discovery and loading
    gizmos.py           # Gizmo path manager and menu builder
    formats.py          # Format management
    knobs.py            # Knob defaults from config
    listUtils.py        # Natural sort and priority sort utilities
    data/defaults.cfg   # Default configuration
  tools/
    python/             # Python tools (auto-discovered, mapped to menus)
      file/             # File operations
      edit/             # Edit operations
        pasteToSelected.py    # Paste into pipe on selected nodes
        setLabel.py           # Quick label editor
        setStartAt.py         # Set start frame
        nodes/
          align/              # Node alignment tools
            alignNodes.py       # Center-align (horizontal/vertical middle)
            mirrorNodes.py      # Mirror nodes
          create/             # Node creation tools
            createDots.py       # Create dot nodes
            createLinks.py      # Create symbolic links
            createReadFromWrite.py
            createWrite.py      # Write from Read with format options
            createWriteDirs.py  # Create output directories
          kiss.py             # Auto-connect nearby nodes
          classDisable.py     # Toggle disable by node class
          togglePanel.py      # Panel to toggle effect types
          revealInFolder.py   # Open file browser to node path
      camera/           # Camera tools
      channel/          # Channel operations
      time/             # Time/animation tools
      transform/        # Transform tools
      other/            # Miscellaneous
      W/                # Wouter Gilsing tools
        W_hotbox.py (v2.0)        # Hotbox popup menu
        W_hotboxManager.py (v2.0) # Hotbox manager
        W_smartAlign.py           # Smart align to connected nodes
        W_scaleTree.py (v2.2)     # Scale node tree
        W_backdropper.py (v1.2)   # Auto-colorize backdrops
        W_moveMenu.py             # Menu manipulation utilities
      _builtins.py      # Built-in menu entries and Reload MyNk
    gizmos/             # Custom gizmos (auto-discovered)
```

## Menu Structure

Tools are auto-discovered from `tools/python/` and added to the **MyNk** menu:

- **File** - File operations, write descriptor updates
- **Edit** - Paste to selected, labels, node alignment, creation tools
  - Nodes/Align/Horizontal/{Left, Middle, Right, Mirror}
  - Nodes/Align/Vertical/{Top, Middle, Bottom, Mirror}
  - Nodes/Kiss, Toggle Class Disable, Toggle Effects Panel
- **Camera, Channel, Time, Transform** - Sorted naturally
- **Other** - Miscellaneous tools
- **Reload MyNk** - Reload the entire mynk environment

Menu ordering uses natural sort (case-insensitive, numeric-aware) with pinned items at the top (File, Edit) and bottom (Other, Reload MyNk).

## Design Principles

- Empower users to define their workflow, don't prescribe it
- Enhancements should be transparent and just work
- Fail gracefully when custom dependencies break
- Keep convenience functions separate from mission-critical logic
- Changes to expected behavior are opt-in
- Keep the original UI intact

## Requirements

- Nuke 14+ (Python 3)
- PySide2 (Nuke < 16) or PySide6 (Nuke 16+)

## Configuration

User configuration is managed via `mynk.cfg` (gitignored) which overrides `mynk/data/defaults.cfg`. Settings include custom formats, knob defaults, and tool paths.
