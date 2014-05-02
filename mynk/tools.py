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
    self.python = None
    if not self.path_list:
      self.path_list.append(MYNK_TOOLS_PATH)

  def add_tools_from_path(self, path, prefix=None):
    if not prefix:
      prefix = 'self.python'
    if os.path.isdir(path):
      LOG.info(path)
      sys.path.append(path)
      test = re.compile(".*\.py$", re.IGNORECASE)
      files = os.listdir(path)
      files.sort()
      for f in files:
        p = os.path.join(path, f)
        if not f.startswith('.'):
          if test.search(f):
            module_name = os.path.splitext(f)[0]
            LOG.info("Loading module: %s" % module_name)
            try:
              module = imp.load_source(module_name, p)
              setattr(eval(prefix), module_name, module)
            except:
              LOG.warning("Plugin %s could not be loaded: %s" % (p, str(detail)) )
          elif os.path.isdir(p):
            path_check = os.path.join(p, "__init__.py" )
            if os.path.exists(path_check):
              package_name = os.path.splitext(f)[0]
              try:
                module = __import__(package_name)
                setattr(eval(prefix), package_name, module)
                LOG.info("Loading package: %s" % package_name)
              except Exception, detail:
                LOG.warning( "Plugin %s could not be loaded: %s" % (package_name, str(detail)))
            else:
              suffix = os.path.splitext(f)[0]
              new_prefix = '.'.join([prefix, suffix])
              new_path = os.path.join(path, suffix)
              self.add_tools_from_path(new_path, new_prefix)


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

