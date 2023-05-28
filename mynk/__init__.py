# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/__init__.py -- wraps mynk in a bow
#


# logger relies on: constants
import logging
from mynk.logger import MyNkLogger
LOG = MyNkLogger().LOG

# constants relies on: exceptions, LOG, internal
from mynk import constants

# const relies on: constants, exceptions, internal
from mynk.const import const, set_const

# config relies on: constants
from mynk.config import MyNkConfig
config = MyNkConfig().config

# gui relies on: constants, config
from mynk.gui import MyNkGui
gui = MyNkGui()

# formats relies on: constants, config
from mynk import formats

# tools relies on: constants, config
from mynk.tools import MyNkTools
tools = MyNkTools()

# knobs relies on: constants, config
import mynk.knobs


__all__ = [ 'constants', 'const', 'set_const', 'LOG', 'config', 'gui', 'formats', 'tools', 'knobs', ]

__name__ = 'mynk'
