import __builtin__
import glob
import imp
import inspect
import logging
import os
import re
import shutil
import sys
import types

import nuke
from configobj import ConfigObj


MYNK_PATH = os.path.dirname(inspect.getfile(sys._getframe(0)))
__builtin__.MYNK_PATH = MYNK_PATH


class MyNk(object):
  """MyNk Workspace Customization Class

  This class implements a number of workspace customizations that are
  in general terms meant for the GUI only and serve to enhance the user
  experience and are not mission critical features.
  
  It provides the following:
   * a reasonably accessible configuration toolset that uses .ini syntax
   * ability to set image format defaults to more sane values
   * ability to set default values on node knobs
   * recursive loading of extra python tools without additional menu.py files
   * local gizmo sandbox area for testing without additional menu.py files
   * custom menu generation
  """
  def __init__(self, cfg_path=None):
    self.init_cfg(cfg_path)
    self.init_logging()
    self.tools = types.ModuleType('tools')


  def init_cfg(self, user_cfg_path=None):
    """
    Initializes the default configuration file
    in the user dotnuke workspace area and creates
    the builtin in config object using that file as it's data source
    """
    default_cfg_path = MYNK_PATH
    default_cfg_file_path = os.path.join(default_cfg_path, 'defaults.cfg')
    if user_cfg_path is None:
      user_cfg_path = DOTNUKE_PATH
    else:
      user_cfg_path = user_cfg_path
    user_cfg_file_path = os.path.join(user_cfg_path, 'mynk.cfg')
    if not os.path.isdir(user_cfg_path):
      try:
        os.makedirs(user_cfg_path)
        self.LOG.info("Created user configuration: %s" % user_cfg_file_path)
      except:
        if not os.path.isdir(user_cfg_path):
          raise
    if not os.path.exists(user_cfg_file_path):
      shutil.copy(default_cfg_file_path, user_cfg_file_path)
    self.config = ConfigObj(user_cfg_file_path, indent_type='  ')
  

  def set_knob_defaults(self, knob_defaults):
    """
    Takes a dictionary from the config object and sets knob defaults
    for the given nodes
    """
    for node, defaults in knob_defaults.iteritems():
      for knob, default in defaults.iteritems():
        nuke.knobDefault('%s.%s' % (node, knob) , '%s' % default)
        msg = 'Added knob default: %s.%s = %s' % (node, knob, default)
        self.LOG.info(msg)


  def set_format_defaults(self, format_defaults):
    """
    Initializes the built in formats and
    takes a dictionary from a config object and sets the image formats
    """
    for format_name, format in format_defaults.iteritems():
      if format.get('active') in ['1', 'true', 'True']:
        if not format.get('W') is None:
          W = format.get('W')
          if not format.get('H') is None:
            H = format.get('H')
            x = format.get('x',0)
            y = format.get('y',0)
            r = format.get('r', format.get('W'))
            t = format.get('t', format.get('H'))
            pa = format.get('pa', 1)
            format_str = "%s %s %s %s %s %s %s %s" % (W, H, x, y, r, t, pa, format_name)
            nuke.addFormat(format_str)
            msg = 'Added format: %s' % format_name
            self.LOG.info(msg)


  def load_python_tools(self, path):
    """
    Iterate through the given folder and load all modules and
    packages found in it. Also add the folder to sys.path.
    """
    self.LOG.info("Looking for tools in: %s" % path)
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
            msg = "Loading module: %s" % module_name
            self.LOG.info(msg)
            try:
              module = imp.load_source(module_name, p)
              setattr(self.tools, module_name, module)
            except Exception, detail:
              msg = "%s could not be loaded: %s" % (p, str(detail))
              self.LOG.warning(msg)
              exception(msg)
          elif os.path.isdir(p):
            p = os.path.join(p, "__init__.py" )
            if os.path.exists(p):
              package_name = os.path.splitext(f)[0]
              msg="Loading package: %s" % p
              self.LOG.info(msg)
              try:
                module = __import__(package_name)
                setattr(self.tools, package_name, module);
              except Exception, detail:
                msg = "Tool %s could not be loaded: %s" % (p, str(detail))
                self.LOG.warning(msg)
                exception(msg)


  def list_tools(self):
    """
    A debugging function to print out details of the loaded tools
    """
    for i,j in self.tools.__dict__.iteritems():
      if isinstance(j, types.ModuleType):
        if hasattr(j, "version" ):
          msg = "Tool: %s %s %s" % (str(i), str(j), str(j.version) )
          self.LOG.debug(msg)
        else:
          msg = "Unversioned Tool: %s %s " % (str(i), str(j))
          self.LOG.debug(msg)
  

  def init_logging(self):
    self.LOG = logging.getLogger('MyNk')
    self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s','%Y-%m-%d %H:%M:%S')
    self.exceptionFormatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s','%Y-%m-%d %H:%M:%S')
    self.streamHandler = logging.StreamHandler()
    self.streamHandler.setFormatter(self.formatter)
    self.LOG.addHandler(self.streamHandler)
    sys.excepthook = self.exception_handler
    self.LOG.flush = types.MethodType(self.__flush_log, self.LOG)
    self.LOG.remove_stream_handler = types.MethodType(self.__remove_stream_handler, self.LOG)
    self.set_devel_log_level()
    self.LOG.info('Initialized MyNk logging')


  def set_devel_log_level(self):
    if ('DEVEL' in os.environ.keys()) and (str(os.environ['DEVEL']).lower() in ['1','yes','true']):
      self.LOG.setLevel( logging.DEBUG )
    else:
      self.LOG.setLevel( logging.INFO )
    

  def __flush_log(self):
    for handler in self.LOG.handlers:
      if hassattr(handler, 'flush'):
        handler.flush()


  def __remove_stream_handler(log=None):
    handlersToRemove = []
    for i,handler in enumerate(self.LOG.handlers):
      if handler == self.streamHandler:
        handlersToRemove.append(i)
    for x in reversed(handlersToRemove):
      del self.LOG.handlers[x]


  def exception_handler(self, exception_type, exception_value, traceback):
    """
    Creates an exception handler to replace the standard except hook
    """
    self.streamHandler.setFormatter(self.exceptionFormatter)
    self.LOG.critical("Uncaught exception", exc_info=(exception_type, exception_value, traceback))
    self.streamHandler.setFormatter(self.formatter)




