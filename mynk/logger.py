# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/logger.py -- wraps python logging to ease loggggging
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#

import os
import sys
import logging
import types

class MyNkLogger(object):
  def __init__(self):
    self.exc_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s','%Y-%m-%d %H:%M:%S')
    self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s','%Y-%m-%d %H:%M:%S')
    self.init_logger()

  def init_handler(self):
    self.stream_handler = logging.StreamHandler()
    self.stream_handler.setFormatter(self.formatter)
    self.stream_handler.setLevel(logging.INFO)
    
  def init_logger(self):
    self.init_handler()
    self.LOG = logging.getLogger('MyNk')
    self.LOG.addHandler(self.stream_handler)
    sys.excepthook = self.exception_handler
    self.LOG.flush = types.MethodType(self.__flush_log, self.LOG)
    self.LOG.remove_stream_handler = types.MethodType(self.__remove_stream_handler, self.LOG)
    self.LOG.setLevel(logging.INFO)

  def __flush_log(self, log):
    '''Flush a log'''
    for handler in log.handlers:
      if hasattr(handler,'flush'):
        handler.flush()
  
  def __remove_stream_handler(self, log):
    '''remove stream handler from a given log object'''
    handlers_to_remove = []
    for i,handler in enumerate(log.handlers):
      if handler == self.stream_handler:
        handlers_to_remove.append(i)
    for x in reversed(handlers_to_remove):
      del log.handlers[x]

  def exception_handler(self, exception_type, exception_value, traceback):
    '''Creates an exception handler to replace the standard except hook'''
    self.stream_handler.setFormatter(self.exc_formatter)
    self.LOG.critical("Uncaught exception", exc_info=(exception_type, exception_value, traceback))
    self.stream_handler.setFormatter(self.formatter)

