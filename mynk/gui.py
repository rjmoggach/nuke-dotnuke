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

import inspect
import os

import nuke

from . import LOG
from . import constants as _c
from .listUtils import natural_sort_key
from .tools import MYNK_MENU_INDEX, MYNK_MENU_TAIL

import mynk  # noqa: F401  (used by eval() of dotted paths in _collect_commands)


class MyNkGui(object):
    def __init__(self):
        nuke.pluginAddPath(os.path.join(_c.MYNK_PATH, "icons"), addToSysPath=False)
        LOG.info(" [MyNk] initializing custom user menus etc.")

    def _collect_commands(self, toolmunch_str):
        """Walk the toolmunch tree and return a flat list of
        (menu_path, cmd, hotkey, icon, separator_before, order) tuples from
        every module's __menus__. `order` is an optional int that pins the
        leaf item ahead of naturally-sorted siblings (lower = earlier)."""
        items = []
        tool_dict = eval(toolmunch_str).toDict()
        for key in tool_dict.keys():
            dotted_path = "{0}.{1}".format(toolmunch_str, key)
            val = tool_dict[key]
            if inspect.ismodule(val):
                menus = getattr(val, "__menus__", None)
                if not menus:
                    continue
                for path, entry in menus.items():
                    if not entry:
                        continue
                    cmd = entry["cmd"]
                    if not cmd.startswith("nuke"):
                        cmd = "{0}.{1}".format(dotted_path, cmd)
                    items.append(
                        (
                            path,
                            cmd,
                            entry.get("hotkey", ""),
                            entry.get("icon", ""),
                            bool(entry.get("separator_before", False)),
                            entry.get("order", None),
                        )
                    )
            else:
                items.extend(self._collect_commands(dotted_path))
        return items

    def _menu_path_sort_key(self, path, order=None):
        """Sort key that applies head/tail priority and natural sort to every
        segment of a '/'-separated menu path. When `order` is supplied, the
        leaf segment uses it instead of natural sort so callers can pin
        logical orderings (e.g. R/G/B/A) that aren't alphabetical."""
        head_map = {item.lower(): i for i, item in enumerate(MYNK_MENU_INDEX)}
        tail_map = {item.lower(): i for i, item in enumerate(MYNK_MENU_TAIL)}
        segs = path.split("/")

        def seg_key(seg, is_leaf):
            s = str(seg).lower()
            if s in head_map:
                return (0, head_map[s], (1,))
            if s in tail_map:
                return (2, tail_map[s], (1,))
            if s.startswith("_"):
                return (2, len(tail_map), (1, natural_sort_key(seg)))
            if is_leaf and order is not None:
                return (1, 0, (0, order))
            return (1, 0, (1, natural_sort_key(seg)))

        last = len(segs) - 1
        return tuple(seg_key(seg, i == last) for i, seg in enumerate(segs))

    def add_toolmunch_to_menu(self, toolmunch_str):
        items = self._collect_commands(toolmunch_str)
        items.sort(key=lambda item: self._menu_path_sort_key(item[0], item[5]))
        for path, cmd, hotkey, icon, sep_before, _order in items:
            if sep_before:
                self.menu.addSeparator()
                self.nuke_toolbar.addSeparator()
            # Hotkey is only registered on the menubar so it shows there;
            # Nuke binds the shortcut to whichever entry was added last, and
            # registering on both would shift the displayed key to the
            # toolbar menu.
            self.menu.addCommand(path, cmd, hotkey, icon)
            self.nuke_toolbar.addCommand(path, cmd, "", icon)

    def init_gui(self):
        nuke_menu = nuke.menu("Nuke")
        self.menu = nuke_menu.addMenu("MyNk", icon="mynk_classic.png")
        nuke_toolbar = nuke.menu("Nodes")
        self.nuke_toolbar = nuke_toolbar.addMenu("MyNk", icon="mynk_classic.png")

    def add_entry_to_toolbar(self, entry):
        pass

    def add_entry_to_menu(self, entry):
        pass

    def add_entry_list(self, entry_list):
        for entry in entry_list:
            pass

    def setFavorites(self):
        nuke.removeFavoriteDir("Nuke")
        nuke.addFavoriteDir("DotNuke", os.path.expanduser("~/.nuke"), 0)
        nuke.addFavoriteDir("Jobs", "/studio/jobs", 0)
        nuke.addFavoriteDir("Fonts", "/", nuke.FONT)

    def restoreWindowLayout(self, layout=1):
        nuke.restoreWindowLayout(layout)
