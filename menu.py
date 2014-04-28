import os
import inspect
import sys
import __builtin__

# Set a globally accessible attribute called DOTNUKE_PATH
# this code should be used carefully with full knowledge of the implications
# We do this HERE because init.py would generally imply a non-gui
# mission-critical functionality and we're looking to extend the gui only
# ie. We don't want renders failing all over the place!!!
DOTNUKE_PATH = os.path.dirname(inspect.getfile(sys._getframe(0)))
__builtin__.DOTNUKE_PATH = DOTNUKE_PATH



# MyNk personal workspace
# ----------------------------------
from mynk import MyNk

# Initialize the mynk object
mynk = MyNk()

# Set the format defaults
mynk.set_format_defaults(mynk.config['formats'])

# Set the knob defaults from mynk config
mynk.set_knob_defaults(mynk.config['knobs'])

# Load the python tools from the mynk config'd path
mynk.load_python_tools(mynk.config['paths']['tools']['python'])






