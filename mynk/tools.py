# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# fsq/tools.py -- provides functions for easily adding tools into the module
#                  namespace: add_tools_path
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#

import os
import shutil
import sys
import types
import imp
import re

import nuke

from . import constants as _c
from . import LOG
from .internal import coerce_unicode

# checkout https://github.com/dsc/bunch
from .bunch import Bunch

MYNK_TOOLS_PATH = coerce_unicode(os.path.join(_c.DOTNUKE_PATH, 'tools', 'python'), _c.MYNK_CHARSET)


class MyNkTools(object):
  def __init__(self, path_list=[]):
    self.path_list = path_list
    self.tools_dict = {}
    self.python=Bunch()
    LOG.info(' [MyNk] initializing custom user tools')
  
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

  def add_python_tools_from_path(self, path, prefix_list=[]):
    '''Recursively add python modules and packages at path
       to dotted python path at prefix'''
    # expand any tilde home directory shortcuts
    path = os.path.expanduser(path)
    # if no prefix list defined use the default internal python bunch
    if not prefix_list:
      prefix_list = ['self','python']
    # we want a filesystem path so check for that first
    if os.path.isdir(path):
      LOG.debug(u'Loading tools from path: {0}'.format(path))
      # add path to system path
      sys.path.append(path)
      search_re = re.compile(".*\.py$", re.IGNORECASE)
      files = os.listdir(path)
      files.sort()
      for file_name in files:
        # ignore hidden files
        if not file_name.startswith('.'):
          file_path = os.path.join(path, file_name)
          # if file matches regex (is python file)
          if search_re.search(file_name):
            module_name = os.path.splitext( file_name )[0]
            try:
              module = imp.load_source(module_name, file_path)
              setattr(eval('.'.join(prefix_list)), module_name, module)
              debug_msg = u'Loaded Module [{0}] from path: {1}'.format(module_name, file_path)
              self.tools_dict
              LOG.debug(debug_msg)
            except Exception, detail:
              error_msg = u'Module [{0}] could not be loaded from path: {1}\n{2}'.format(module_name, file_path, detail)
              LOG.warning(error_msg)
          # if file is directory (org or package)
          elif os.path.isdir(file_path):
            path_check = os.path.join(file_path, "__init__.py" )
            if os.path.exists(path_check):
              package_name = os.path.splitext(file_name)[0]
              try:
                package = __import__(package_name)
                setattr(eval('.'.join(prefix_list)), package_name, package)
                debug_msg = u'Loaded Package [{0}] from path: {1}'.format(package_name, file_path)
                LOG.debug(debug_msg)
              except Exception, detail:
                error_msg = u'Package [{0}] could not be loaded from path: {1}\n{2}'.format(package_name, file_path, detail)
                LOG.warning(error_msg)
            else:
              dir_name = os.path.splitext(file_name)[0]
              self.tools_dict[dir_name] = {}
              setattr(eval('.'.join(prefix_list)), dir_name, Bunch())
              prefix_list.append(dir_name)
              new_prefix = '.'.join(prefix_list)
              new_path = os.path.join(path, suffix)
              self.add_python_tools_from_path(new_path, prefix_list=prefix_list)

  def add_tools_to_menu(self, menu=[], submenu=None):
    pass
  
  def list_plugins(self):
    '''
    A debugging function to print out details of the loaded plugins
    '''
    for i,j in self.tools.__dict__.iteritems():
      if isinstance( j, types.ModuleType ):
        if hasattr( j, "version" ):
          LOG.info( "  ---> Plugin: %s %s %s" % (str(i), str(j), str(j.version) ) )
        else:
          LOG.info( "  ---> Unversioned Plugin: %s %s " % (str(i), str(j)) )

