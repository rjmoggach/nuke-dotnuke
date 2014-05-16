# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/internal.py -- non-public methods for internal module consumption
#

import os
import inspect
import sys

_MODULE_PATH = os.path.dirname(inspect.getfile(sys._getframe(0)))