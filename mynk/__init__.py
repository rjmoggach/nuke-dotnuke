# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/__init__.py -- wraps mynk in a bow
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#


# ORDER MATTERS HERE -- SOME MODULES ARE DEPENDANT ON OTHERS
from exceptions import MyNkError, MyNkEnvError, MyNkKnobsError, \
                       MyNkConfigError, MyNkConfigMalformedError, \
                       MyNkCoerceError, MyNkConfigDoesNotExistError, \
                       MyNkConfigUnreadableError, \
                       MyNkFormatsError, MyNkMalformedFormatError

# logger relies on: constants
from logger import MyNkLogger
LOG = MyNkLogger().LOG

# constants relies on: exceptions, LOG, internal
import constants

# const relies on: constants, exceptions, internal
from const import const, set_const

# config relies on: constants
from config import MyNkConfig
config = MyNkConfig().config

# formats relies on: constants, config
import formats

# tools relies on: constants, config
from tools import MyNkTools
tools = MyNkTools().python

# knobs relies on: constants, config
import knobs


__all__ = [ 'MyNkError', 'MyNkEnvError', 'MyNkKnobsError', 'MyNkConfigError', 'MyNkCoerceError',
            'MyNkConfigMalformedError', 'MyNkConfigDoesNotExistError', 'MyNkConfigUnreadableError',
            'MyNkFormatsError', 'MyNkMalformedFormatError',
            'constants', 'const', 'set_const', 'LOG', 'config', 'formats', 'tools', 'knobs', ]
