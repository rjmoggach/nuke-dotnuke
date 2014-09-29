# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/gui.py -- provides functions for building mynk toolbar and menu: init_gui, add_toolbar, add_menu
#
# SHORT CUT SYNTAX
# 'Ctrl-s'    "^s"
# 'Ctrl-Shift-s'  "^+s"
# 'Alt-Shift-s'   "#+s"
# 'Shift+F4'    "+F4"
#
# convert camel case to titles re.sub("([a-z])([A-Z])","\g<1> \g<2>", key).title()

import re
import os
import shutil
from types import ModuleType
import inspect

import nuke

from . import constants as _c
from . import LOG
from . import config

import mynk

class MyNkGui(object):
  def __init__(self):
    nuke.pluginAddPath(os.path.join(_c.MYNK_PATH, 'icons'), addToSysPath=False)
    LOG.info(' [MyNk] initializing custom user menus etc.')

  def add_tool_menus(self, tool_str):
    try:
      tool = eval(tool_str)
      menus = getattr(tool, '__menus__' ,None)
    except AttributeError:
      LOG.warning(' [MyNk] tool has no __menus__ attribute: {0}'.format(tool_str))
    else:
      if menus is None:
        return
      else:
        for key,val in menus.iteritems():
          title = key
          if val:
            cmd = val['cmd'] if val['cmd'].startswith('nuke') else '{0}.{1}'.format(tool_str, val['cmd'])
            hotkey = val['hotkey']
            icon = val['icon']
            for menu in [self.menu,self.nuke_toolbar]:
              menu.addCommand(title,cmd,hotkey,icon)
          else:
            menu.addMenu(title)
            
  def add_toolbunch_to_menu(self, toolbunch_str):
    for key,val in eval(toolbunch_str).toDict().iteritems():
      dottedpath = '{0}.{1}'.format(toolbunch_str,key)
      if inspect.ismodule(val):
        self.add_tool_menus(dottedpath)
      else:
        self.add_toolbunch_to_menu(dottedpath)

  def init_gui(self):
    nuke_menu = nuke.menu('Nuke')
    self.menu = nuke_menu.addMenu('MyNk', icon='mynk.png')
    nuke_toolbar = nuke.menu("Nodes")
    self.nuke_toolbar = nuke_toolbar.addMenu("MyNk", "mynkx.png")

  def add_entry_to_toolbar(self, entry):
    pass

  def add_entry_to_menu(self, entry):
    pass

  def add_entry_list(self, entry_list):
   for entry in entry_list:
     pass
 
  def setFavorites(self):
    nuke.removeFavoriteDir('Nuke')
    nuke.addFavoriteDir('DotNuke', os.path.expanduser('~/.nuke'), 0)
    nuke.addFavoriteDir('Jobs', '/', 0)
    nuke.addFavoriteDir('Fonts', '/', nuke.FONT)
  
  def restoreWindowLayout(self, layout=1):
    nuke.restoreWindowLayout(layout)

