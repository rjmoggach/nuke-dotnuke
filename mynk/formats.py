# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/formats.py -- provides functions for setting image format defaults: add_format, add_formats_from_dict
#

import nuke

from . import constants as _c
from . import LOG
from . import config

LOG.info(' [MyNk] initializing custom user image formats')


def add_format(W, H, x, y, r, t, pa, format_name):
  '''Add a format based on provided attributes'''
  if not W is None and not H is None and not format_name is None:
      x = 0 if x is None else x
      y = 0 if y is None else y
      r = W if r is None else r
      t = H if t is None else t
      pa = 1 if pa is None else pa
      format_str = u'{0} {1} {2} {3} {4} {5} {6} {7}'.format(W, H, x, y, r, t, pa, format_name)
      nuke.addFormat(format_str)
      msg = u'Added format: {0}'.format(format_str)
      LOG.debug(msg)


def add_formats_from_dict(defaults_dict):
  '''Add nuke formats from an iterated dict of formats'''
  for format_name, format in defaults_dict.iteritems():
    if format.get('active', False) in ['1', 'true', 'True']:
      W = format.get('W', None)
      H = format.get('H', None)
      x = format.get('x', 0)
      y = format.get('y', 0)
      r = format.get('r', W)
      t = format.get('r', H)
      pa = format.get('pa', 1)
      add_format(W, H, x, y, r, t, pa, format_name)


def add_formats_from_config():
  '''wrapper for adding formats from config dict'''
  add_formats_from_dict(config['formats'])

