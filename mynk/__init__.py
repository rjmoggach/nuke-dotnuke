# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/__init__.py -- wraps mynk in a bow
#


# logger relies on: constants
import logging
from logger import MyNkLogger
LOG = MyNkLogger().LOG

# constants relies on: exceptions, LOG, internal
import constants

# const relies on: constants, exceptions, internal
from const import const, set_const

# config relies on: constants
from config import MyNkConfig
config = MyNkConfig().config

# gui relies on: constants, config
from gui import MyNkGui
gui = MyNkGui()

# formats relies on: constants, config
import formats

# tools relies on: constants, config
from tools import MyNkTools
tools = MyNkTools()

# knobs relies on: constants, config
import knobs


__all__ = [ 'constants', 'const', 'set_const', 'LOG', 'config', 'gui', 'formats', 'tools', 'knobs', ]

__name__ = 'mynk'