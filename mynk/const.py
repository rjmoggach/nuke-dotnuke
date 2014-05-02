# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/const.py -- provides constants convenience functions: const, set_const
#
# mynk is all unicode internally, if you pass in strings,
# they will be explicitly coerced to unicode.
#

import errno
import numbers

from . import constants as _c, MyNkEnvError
from .internal import coerce_unicode


def const(const):
  '''Convenience wrapper to yield the value of a constant'''
  try:
    return getattr(_c, const)
  except AttributeError:
    raise MyNkEnvError(errno.EINVAL, u'No such constant: {0}'.format(const))
  except TypeError:
    raise TypeError(errno.EINVAL, u'const name must be a string or unicode object, not: {0}'.format(const.__class__.__name__))


def set_const(const, val):
  '''Convenience wrapper to reliably set the value of a constant from outside of package scope'''
  try:
    cur = getattr(_c, const)
  except AttributeError:
    raise MyNkEnvError(errno.ENOENT, u'no such constant: {0}'.format(const))
  except TypeError:
    raise TypeError(errno.EINVAL, u'const name must be a string or unicode object, not: {0}'.format(const.__class__.__name__))
  should_be = cur.__class__
  try:
    if not isinstance(val, should_be):
      if should_be is unicode or cur is None:
        val = coerce_unicode(val, _c.FSQ_CHARSET)
      elif should_be is int and const.endswith('MODE'):
        val = int(val, 8)
      elif isinstance(cur, numbers.Integral):
        val = int(val)
      else:
        should_be(val)
  except (TypeError, ValueError, ):
    raise MyNkEnvError(errno.EINVAL, u'invalid type for constant {0}, should be {1}, not: {2}'.format(const, should_be.__name__, val.__class__.__name__))
  setattr(_c, const, val)
  return val