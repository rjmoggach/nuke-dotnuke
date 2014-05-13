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


class ToolMeta(type):
  def __init__(cls, name, bases, dct):
    if not hasattr(cls, 'registry'):
      # base class - create empty registry
      cls.registry = {}
    else:
      # derived class - add cls to registry
      tool_id = name.lower()
      cls.registry[tool_id] = cls
    super(ToolMeta, cls).__init__(name, bases, dct)

class Tool(object):
  __metaclass__ = ToolMeta


class Container(object):
  def __getattr__(self, name):
    self.__dict__[name] = Container()
    return self.__dict__[name]

  def __repr__(self):
    return_dict = {}
    for key,val in self.__dict__.items():
      return_dict[key] = val
    return repr(return_dict)
      

class MyNkTools(object):
  def __init__(self, path_list=[]):
    self.path_list = path_list
    self.python = Bunch()
    LOG.info(' [MyNk] initializing custom user tools')
  
  def add_default_path(self):
    if not self.path_list:
      self.path_list.append(MYNK_TOOLS_PATH)

  def add_path(self, path):
    if os.path.isdir(path):
      if not path in self.path_list:
        self.path_list.append(path)

  def add_tools_from_path_list(self):
    if self.path_list:
      for path in self.path_list:
        self.add_tools_from_path(path)
    else:
      self.add_default_path()
      self.add_tools_from_path_list()

  def add_tools_from_path(self, path, prefix='self.python'):
#    if not prefix[:5] == 'self.':
#      prefix = 'self.{prefix}'.format(prefix=prefix)
#    prefix_exec = '{0} = Bunch()'.format(prefix)
#    LOG.info(prefix_exec)
#    exec(prefix)
    path = os.path.expanduser(path)
    if os.path.isdir(path):
      path_msg = u'Loading tools from path: {0}'.format(path)
      LOG.debug(path_msg)
      sys.path.append(path)
      search_re = re.compile(".*\.py$", re.IGNORECASE)
      files = os.listdir(path)
      files.sort()
      for file_name in files:
        file_path = os.path.join(path, file_name)
        if not file_name.startswith('.'):
          if search_re.search(file_name):
            module_name = os.path.splitext( file_name )[0]
            try:
              module = imp.load_source(module_name, file_path)
              setattr(eval(prefix), module_name, module)
              debug_msg = u'Loaded Module [{0}] from path: {1}'.format(module_name, file_path)
              LOG.debug(debug_msg)
            except Exception, detail:
              error_msg = u'Module [{0}] could not be loaded from path: {1}\n{2}'.format(module_name, file_path, detail)
              LOG.warning(error_msg)
          elif os.path.isdir(file_path):
            path_check = os.path.join(file_path, "__init__.py" )
            if os.path.exists(path_check):
              package_name = os.path.splitext(file_name)[0]
              try:
                package = __import__(package_name)
                setattr(eval(prefix), package_name, package)
                debug_msg = u'Loaded Package [{0}] from path: {1}'.format(package_name, file_path)
                LOG.debug(debug_msg)
              except Exception, detail:
                error_msg = u'Package [{0}] could not be loaded from path: {1}\n{2}'.format(package_name, file_path, detail)
                LOG.warning(error_msg)
            else:
              suffix = os.path.splitext(file_name)[0]
              new_prefix = '.'.join([prefix, suffix])
              setattr(eval(prefix), suffix, Bunch())
              new_path = os.path.join(path, suffix)
              self.add_tools_from_path(new_path, prefix=new_prefix)

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

