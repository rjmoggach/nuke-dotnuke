# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/internal.py -- non-public methods for internal module consumption
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#
import os
import inspect
import sys
import errno
import numbers

from . import MyNkCoerceError

# additional types to coerce to unicode, beyond decodable types
_COERCE_THESE_TOO = (numbers.Real,)


def coerce_unicode(s, charset):
  if isinstance(s, unicode):
    return s
  try:
    return unicode(s, encoding=charset)
  except (UnicodeEncodeError, UnicodeDecodeError, ), e:
    raise MyNkCoerceError(errno.EINVAL, u'cannot decode: {0} (charset: {1})'.format(e.reason, charset))
  except TypeError, e:
      if isinstance(s, _COERCE_THESE_TOO):
          try:
              return unicode(s)
          except Exception, e:
              raise MyNkCoerceError(errno.EINVAL, e.message)
      raise MyNkCoerceError(errno.EINVAL, e.message)


_MODULE_PATH = os.path.dirname(inspect.getfile(sys._getframe(0)))