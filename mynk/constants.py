# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/constants.py -- a place for constants.  per MyNk specification,
#   constants take their value from the calling program environment
#   (if available), and default to the the expected values.
#

import os
import inspect
import sys
import errno

from . import LOG
from .internal import _MODULE_PATH

try:
  # Set the default unicode charset to be utf8
  MYNK_CHARSET = os.environ.get("MYNK_CHARSET", u'utf8')
  
  # Set the mynk delimiter to be an underscore
  MYNK_DELIMITER = os.environ.get("MYNK_DELIMITER", u'_')
  
  # Set the module's path attribute
  MYNK_PATH = os.environ.get("MYNK_PATH", _MODULE_PATH)
  
  # For convenience set the dotnuke folder location
  DOTNUKE_PATH = os.path.expanduser('~/.nuke')
  
  # If we want more debugging set the MYNK_DEVEL environment variable
  MYNK_DEVEL = True if os.environ.get("MYNK_DEVEL", False) in ['1', 'true', 'True'] else False
  LOG.debug(u'MYNK_DEVEL attribute is {0}'.format(MYNK_DEVEL) )

except ValueError as e:
  LOG.error(errno.EINVAL, e.message)

