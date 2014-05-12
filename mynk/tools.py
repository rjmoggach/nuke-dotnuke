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


MYNK_TOOLS_PATH = coerce_unicode(os.path.join(_c.DOTNUKE_PATH, 'tools', 'python'), _c.MYNK_CHARSET)


class MyNkTools(object):
  def __init__(self, path_list=[]):
    self.path_list = path_list
    self.python = self.Tools()
    LOG.info(' [MyNk] initializing custom user tools')
  
  class Tools(object):
    '''convenience container class for organizing
    arbitrary python tools in a hierarchy'''
    def __init__(self, **kw):
      self.__dict__.update(kw)

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

  def add_tools_from_path(self, path, prefix=None):
    if not prefix:
      prefix = 'self.python'
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
                module = __import__(package_name)
                setattr(eval(prefix), package_name, module)
                debug_msg = u'Loaded Package [{0}] from path: {1}'.format(package_name, file_path)
                LOG.debug(debug_msg)
              except Exception, detail:
                error_msg = u'Package [{0}] could not be loaded from path: {1}\n{2}'.format(package_name, file_path, detail)
                LOG.warning(error_msg)
            else:
              suffix = os.path.splitext(file_name)[0]
              new_prefix = '.'.join([prefix, suffix])
              eval_sub_str= u'setattr({0},"{1}",self.Tools())'.format(prefix, suffix)
              eval(eval_sub_str)
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

