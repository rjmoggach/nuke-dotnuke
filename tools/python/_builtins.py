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

__menus__ = {
  'Tools/Channel/Keep': {
    'cmd': "nuke.createNode('Remove', 'operation keep channels rgba')",
    'hotkey': '',
    'icon': 'Keep.png'
  },
  'Tools/Channel/Flood Red': {
    'cmd': "nuke.createNode('Shuffle', 'green red blue red alpha red name Flood_Red tile_color 0x7e0b0bff')",
    'hotkey': '',
    'icon': 'FloodRed.png'
  },
  'Tools/Channel/Flood Green': {
    'cmd': "nuke.createNode('Shuffle', 'red green blue green alpha green name Flood_Green tile_color 0x356b00ff')",
    'hotkey': '',
    'icon': 'FloodGreen.png'
  },
  'Tools/Channel/Flood Blue': {
    'cmd': "nuke.createNode('Shuffle', 'red blue green blue alpha blue name Flood_Blue tile_color 0x171789ff')",
    'hotkey': '',
    'icon': 'FloodBlue.png'
  },
  'Tools/Channel/Flood Alpha': {
    'cmd': "nuke.createNode('Shuffle', 'red alpha green alpha blue alpha name Flood_Alpha tile_color 0xffffffff')",
    'hotkey': '',
    'icon': 'FloodAlpha.png'
  },
  'Tools/Channel/Shuffle From': {
    'cmd': "nuke.createNode('Shuffle', 'in2 rgba red red2 green green2 blue blue2 label \[knob\ this.in2\]')",
    'hotkey': '',
    'icon': 'Shuffle.png'
  },
}

