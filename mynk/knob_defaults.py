import nuke
from .defaults import *

# Define a number of custom knob defaults
for d in KNOB_DEFAULTS:
  nuke.knobDefault('%s.%s' % (d[0], d[1]) , '%s' %d[2])
