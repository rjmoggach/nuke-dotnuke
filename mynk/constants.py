# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/constants.py -- a place for constants.  per MyNk specification,
#   constants take their value from the calling program environment
#   (if available), and default to the the expected values.
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#

import os
import inspect
import sys
import errno

from . import MyNkEnvError
from . import LOG
from .internal import coerce_unicode
from .internal import _MODULE_PATH

try:
  # Set the default unicode charset to be utf8
  MYNK_CHARSET = os.environ.get("MYNK_CHARSET", u'utf8')
  MYNK_CHARSET = coerce_unicode(MYNK_CHARSET, MYNK_CHARSET)
  
  # Set the mynk delimiter to be an underscore
  MYNK_DELIMITER = coerce_unicode(os.environ.get("MYNK_DELIMITER", u'_'), MYNK_CHARSET)
  
  # Set the module's path attribute
  MYNK_PATH = coerce_unicode(os.environ.get("MYNK_PATH", _MODULE_PATH), MYNK_CHARSET)
  
  # For convenience set the dotnuke folder location
  DOTNUKE_PATH = coerce_unicode(os.path.expanduser('~/.nuke'), MYNK_CHARSET)
  
  # If we want more debugging set the MYNK_DEVEL environment variable
  MYNK_DEVEL = True if coerce_unicode(os.environ.get("MYNK_DEVEL", False), MYNK_CHARSET) in ['1', 'true', 'True'] else False
  LOG.debug(u'MYNK_DEVEL attribute is {0}'.format(MYNK_DEVEL) )

except ValueError, e:
  raise MyNkEnvError(errno.EINVAL, e.message)

