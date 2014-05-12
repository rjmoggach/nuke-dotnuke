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
# logging levels for reference:
# DEBUG	Detailed information, typically of interest only when diagnosing problems.
# INFO	Confirmation that things are working as expected.
# WARNING	An indication that something unexpected happened, or indicative of some problem in the near future
# (e.g. 'disk space low'). The software is still working as expected.
# ERROR	Due to a more serious problem, the software has not been able to perform some function.
# CRITICAL A serious error, indicating that the program itself may be unable to continue running.

import os
import sys
import logging
import types



class MyNkLogger(object):
  def __init__(self):
    self.level = logging.DEBUG \
                 if os.environ.get("MYNK_DEVEL", False) in ['1', 'true', 'True'] \
                 else logging.INFO
    exc_format = '%(asctime)s %(levelname)s: %(message)s'
    format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    self.exc_formatter = logging.Formatter(exc_format, date_format)
    self.formatter = logging.Formatter(format, date_format)
    self.init_logger()

  def init_handler(self):
    self.stream_handler = logging.StreamHandler()
    self.stream_handler.setFormatter(self.formatter)
    self.stream_handler.setLevel(self.level)
    
  def init_logger(self):
    self.init_handler()
    self.LOG = logging.getLogger('MyNk')
    self.LOG.addHandler(self.stream_handler)
    sys.excepthook = self.exception_handler
    self.LOG.flush = types.MethodType(self.__flush_log, self.LOG)
    self.LOG.remove_stream_handler = types.MethodType(self.__remove_stream_handler, self.LOG)
    self.LOG.setLevel(self.level)

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

