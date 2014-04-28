import sys
import os
import re
import types
import imp
import nuke
from mynk.log import LOG


class PythonLoader(object):
  def __init__(self, settings=None, path=None, verbose=False):
    self.settings = settings
    self.verbose = verbose
    self.studio = self.settings.STUDIO
    if path is None:
      self.tools_path = self.settings.TOOLS_PATH
    else:
      self.tools_path = path
    self.tools = types.ModuleType('plugins')
    for tool_path in self.tools_path:
        self.load_plugins_from_path(tool_path)
    if self.verbose:
      self.list_plugins()


  def load_plugins_from_path(self, path):
    '''
    Iterate through the given folder and load all modules and
    packages found in it. Also add the folder to sys.path.
    '''
    if self.verbose:
      LOG.info("  ---> Looking for plugins in " + path)
    if os.path.isdir(path):
      sys.path.append(path)
      test = re.compile(".*\.py$", re.IGNORECASE)
      files = os.listdir(path)
      files.sort()
      for f in files:
        p = os.path.join( path, f )
        if not f.startswith("."):
          if test.search(f):
            module_name = os.path.splitext(f)[0]
            LOG.info( "   - Loading module " + module_name )
            try:
              module = imp.load_source(module_name, p)
              setattr(self.tools, module_name, module)
            except Exception, detail:
              exception( "   ---> %s could not be loaded: %s" % (p, str(detail)))
          elif os.path.isdir(p):
            p = os.path.join(p, "__init__.py" )
            if os.path.exists(p):
              package_name = os.path.splitext(f)[0]
              if self.verbose:
                LOG.info("  --->    - Loading package %s" % p)
              try:
                module = __import__(package_name)
                setattr(self.tools, package_name, module);
              except Exception, detail:
                LOG.warning( "   ---> Plugin %s could not be loaded: %s" % (p, str(detail)))


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

