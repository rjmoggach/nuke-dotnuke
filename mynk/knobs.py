# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# fsq/knobs.py -- provides functions for setting knob defaults: add_defaults, add_defaults_from_dict
#

import nuke

from . import constants as _c
from . import LOG
from . import config

LOG.info(' [MyNk] initializing custom user knob defaults')


def add_knob_default(node, knob, default):
  '''Add a knob default for a given node'''
  knob_default={ 'node': node, 'knob': knob, 'default': default }
  nuke.knobDefault(u'{node}.{knob}'.format(**knob_default) , '{default}'.format(**knob_default))
  LOG.debug(u'Added knob default: {node}.{knob} = {default}'.format(**knob_default))


def add_knob_defaults_from_dict(defaults_dict):
  '''Add defaults for given node knobs from an iterated dict of node knob defaults'''
  for node, defaults in defaults_dict.iteritems():
    for knob, default in defaults.iteritems():
      add_knob_default(node, knob, default)


def set_knob_defaults_from_config():
  '''Sets the nuke defaults from a provided config dict'''
  knob_defaults = config['knobs']
  add_knob_defaults_from_dict(knob_defaults)
  