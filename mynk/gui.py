# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/gui.py -- provides functions for building mynk toolbar and menu: init_gui, add_toolbar, add_menu
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#

import os
import shutil

import nuke

from . import constants as _c
from . import LOG
from . import config
from .internal import coerce_unicode


class MyNkGui(object):
  def __init__(self):
    nuke.pluginAddPath(coerce_unicode(os.path.join(_c.MYNK_PATH, 'icons'), _c.MYNK_CHARSET), addToSysPath=False)

  def create_menu(self):
    nuke_menu = nuke.menu('Nuke')
    self.menu = nuke_menu.addMenu('&MyNk', icon='mynk.png')
  
  def create_toolbar(self):
    nuke_toolbar = nuke.menu("Nodes")
    self.toolbar = nuke.toolbar('MyNk')
    self.toolbar_menu = self.toolbar.addMenu('MyNk', icon="mynk.png")

  def init_gui(self):
    self.create_menu()
    self.create_toolbar()
    self.menu.addCommand("Restore Clean Layout", "nuke.restoreWindowLayout(7)", "F5", icon="desktop_alt_2.png")

  def add_entry_to_toolbar(self, entry):
    pass

  def add_entry_to_menu(self, entry):
    pass

  def add_entry_list(self, entry_list):
   for entry in entry_list:
     pass
 
  def setFavorites(self):
    # SHORT CUT SYNTAX
    # 'Ctrl-s'    "^s"
    # 'Ctrl-Shift-s'  "^+s"
    # 'Alt-Shift-s'   "#+s"
    # 'Shift+F4'    "+F4"
    nuke.removeFavoriteDir('Nuke')
    nuke.addFavoriteDir('DotNuke', os.path.expanduser('~/.nuke'), 0)
    nuke.addFavoriteDir('Jobs', '/', 0)
    nuke.addFavoriteDir('Fonts', '/', nuke.FONT)
  
  def restoreWindowLayout(self, layout=1):
    nuke.restoreWindowLayout(layout)
