# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/exceptions.py -- provides exceptions for mynk, exceptions in their own module
#                      avoids circular imports
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#

class MyNkError(OSError):
  '''root for MyNkErrors, only used to except any MyNk error, never raised'''
  pass
  
class MyNkEnvError(MyNkError):
  '''An error occurred while evaluating the mynk environment'''
  pass

class MyNkKnobsError(MyNkError):
  '''An error occurred while using the mynk knobs tools'''
  pass

class MyNkConfigError(MyNkError):
  '''An error occurred while using the mynk config tools'''
  pass

class MyNkConfigMalformedError(MyNkConfigError):
  '''A provided config file does not evaluate correctly'''
  pass

class MyNkConfigDoesNotExistError(MyNkConfigError):
  '''A provided config file does not exist'''
  pass

class MyNkConfigUnreadableError(MyNkConfigError):
  '''A provided config file is not readable'''
  pass

class MyNkFormatsError(MyNkError):
  '''An error occurred while using the mynk formats tools'''
  pass

class MyNkMalformedFormatError(MyNkFormatsError):
  '''An error occurred while parsing a provided format string'''
  pass

class MyNkCoerceError(MyNkError):
  '''Everything is coerced to unicode'''
  pass
