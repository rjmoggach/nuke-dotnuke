import os
import sys
import logging
import types

from mynk.settings import LOG_PATH


# Define our LOG class for convenience
LOG = logging.getLogger('MyNk')
LOG_FILE = os.path.join(LOG_PATH,'mynk.log')
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s','%Y-%m-%d %H:%M:%S')
EXCEPTION_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s: %(message)s','%Y-%m-%d %H:%M:%S')
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)
LOG.addHandler(STREAM_HANDLER)


if ('DEVEL' in os.environ.keys()) and (str(os.environ['DEVEL']).lower() in ['1','yes','true']):
  LOG.setLevel( logging.DEBUG )
else:
  LOG.setLevel( logging.INFO )


def __flush_log(log=None):
  if log is None:
    log = LOG
  for handler in log.handlers:
    if hasattr(handler,'flush'):
      handler.flush()


def __remove_stream_handler(log=None):
  if log is None:
    log = LOG
  handlers_to_remove = []
  for i,handler in enumerate(log.handlers):
    if handler == STREAM_HANDLER:
      handlers_to_remove.append(i)
  for x in reversed(handlers_to_remove):
    del log.handlers[x]


def exception_handler(exception_type, exception_value, traceback):
  """
  Creates an exception handler to replace the standard except hook
  """
  STREAM_HANDLER.setFormatter(EXCEPTION_FORMATTER)
  LOG.critical("Uncaught exception", exc_info=(exception_type, exception_value, traceback))
  STREAM_HANDLER.setFormatter(FORMATTER)


sys.excepthook = exception_handler
LOG.flush = types.MethodType(__flush_log, LOG)
LOG.remove_stream_handler = types.MethodType(__remove_stream_handler, LOG)

