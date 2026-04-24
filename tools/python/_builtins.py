# there are a number of tools that I want to be part of the tools menu
# so this is a quick way of getting them in there without extra work
#
# I add a __menus__ dict and it gets picked up by mynk.tools and mynk.gui
#
# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"
import importlib
import mynk


def reload_mynk():
    importlib.reload(mynk)
    mynk.gui.init_gui()
    mynk.tools.add_python_tools_from_path_list()
    mynk.gui.add_toolmunch_to_menu("mynk.tools.python")


__menus__ = {
    "Channel/Keep": {
        "cmd": "nuke.createNode('Remove', 'operation keep channels rgba')",
        "hotkey": "",
        "icon": "Keep.png",
        "order": 10,
    },
    "Channel/Flood Red": {
        "cmd": "nuke.createNode('Shuffle', 'green red blue red alpha red name Flood_Red tile_color 0x7e0b0bff')",
        "hotkey": "",
        "icon": "FloodRed.png",
        "order": 20,
    },
    "Channel/Flood Green": {
        "cmd": "nuke.createNode('Shuffle', 'red green blue green alpha green name Flood_Green tile_color 0x356b00ff')",
        "hotkey": "",
        "icon": "FloodGreen.png",
        "order": 21,
    },
    "Channel/Flood Blue": {
        "cmd": "nuke.createNode('Shuffle', 'red blue green blue alpha blue name Flood_Blue tile_color 0x171789ff')",
        "hotkey": "",
        "icon": "FloodBlue.png",
        "order": 22,
    },
    "Channel/Flood Alpha": {
        "cmd": "nuke.createNode('Shuffle', 'red alpha green alpha blue alpha name Flood_Alpha tile_color 0xffffffff')",
        "hotkey": "",
        "icon": "FloodAlpha.png",
        "order": 23,
    },
    "Channel/Shuffle From": {
        "cmd": "nuke.createNode('Shuffle', 'in2 rgba red red2 green green2 blue blue2 label \[knob\ this.in2\]')",
        "hotkey": "",
        "icon": "Shuffle.png",
        "order": 30,
    },
    "Reload MyNk": {
        "cmd": "reload_mynk()",
        "hotkey": "",
        "icon": "Recycle.png",
        "separator_before": True,
    },
}
