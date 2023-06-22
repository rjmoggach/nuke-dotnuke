# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# fsq/tools.py -- provides functions for easily adding tools into the module
#                  namespace: add_tools_path
#

import os
import shutil
import sys
import types
import imp
import re
import inspect

import nuke

from . import constants as _c
from . import LOG

# checkout https://github.com/Infinidat/munch
from .munch import Munch

MYNK_TOOLS_PATH = os.path.join(_c.DOTNUKE_PATH, "tools", "python")

MYNK_MENU_INDEX = [
    "file",
    "edit",
]


class MyNkTools(object):
    @property
    def __name__(self):
        return "mynk.tools"

    def __init__(self, path_list=[]):
        self.path_list = path_list
        self.tools_dict = {}
        self.python = Munch()
        self.prefix = inspect.getmodule(self).__name__
        LOG.info(" [MyNk] initializing custom user tools")

    def add_default_path(self):
        if not self.path_list:
            self.path_list.append(MYNK_TOOLS_PATH)

    def add_path(self, path):
        if os.path.isdir(path):
            if not path in self.path_list:
                self.path_list.append(path)

    def add_python_tools_from_path_list(self):
        if self.path_list:
            for path in self.path_list:
                self.add_python_tools_from_path(path)
        else:
            self.add_default_path()
            self.add_python_tools_from_path_list()

    def add_python_tools_from_path(self, path, dest=None):
        """Recursively add python modules and packages at path
        to dotted python path at prefix"""
        # expand any tilde home directory shortcuts
        path = os.path.expanduser(path)
        # if no prefix list defined use the default internal python munch
        if dest is None:
            dest = self.python
        # we want a filesystem path so check for that first
        if os.path.isdir(path):
            # ignore pycache
            if not (os.path.basename(path) == "__pycache__"):
                LOG.debug("Loading tools from path: {0}".format(path))
                # add path to system path
                sys.path.append(path)
                search_re = re.compile(".*\.py$", re.IGNORECASE)
                files = os.listdir(path)
                files.sort()
                for file_name in files:
                    # ignore hidden files
                    if not file_name.startswith("."):
                        file_path = os.path.join(path, file_name)
                        # if file matches regex (is python file)
                        if search_re.search(file_name):
                            module_name = os.path.splitext(file_name)[0]
                            try:
                                module = imp.load_source(module_name, file_path)
                                setattr(dest, module_name, module)
                                LOG.debug(
                                    "Loaded Module [{0}]: {1}".format(
                                        module_name, file_path
                                    )
                                )
                            except Exception as detail:
                                LOG.warning(
                                    "Module [{0}] could not be loaded: {1}\n{2}".format(
                                        module_name, file_path, detail
                                    )
                                )
                        # if file is directory (org or package)
                        elif os.path.isdir(file_path):
                            path_check = os.path.join(file_path, "__init__.py")
                            if os.path.exists(path_check):
                                package_name = os.path.splitext(file_name)[0]
                                try:
                                    package = __import__(package_name)
                                    setattr(dest, package_name, package)
                                    LOG.debug(
                                        debug_msg="Loaded Package [{0}]: {1}".format(
                                            package_name, file_path
                                        )
                                    )
                                except Exception as detail:
                                    LOG.warning(
                                        "Package [{0}] could not be loaded from path: {1}\n{2}".format(
                                            package_name, file_path, detail
                                        )
                                    )
                            else:
                                dir_name = os.path.splitext(file_name)[0]
                                setattr(dest, dir_name, Munch())
                                new_path = os.path.join(path, dir_name)
                                self.add_python_tools_from_path(
                                    new_path, eval("dest.{0}".format(dir_name))
                                )
                        else:
                            pass

    def list_plugins(self):
        """
        A debugging function to print out details of the loaded plugins
        """
        for i, j in self.tools.__dict__.iteritems():
            if isinstance(j, types.ModuleType):
                if hasattr(j, "version"):
                    LOG.info(
                        "  ---> Plugin: %s %s %s" % (str(i), str(j), str(j.version))
                    )
                else:
                    LOG.info("  ---> Unversioned Plugin: %s %s " % (str(i), str(j)))
