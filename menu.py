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
import mynk

# Build the custom menu and toolbar
mynk.gui.init_gui()

# Set the format defaults
mynk.formats.add_formats_from_config()

# Load the python tools from the mynk config'd path
# if you want to add paths, add them one line at a time as follows
# the following example is the default so not necessary to add
# as it will find it if no other paths have been added
#
# mynk.tools.add_path('~/.nuke/tools/python')
#
mynk.tools.add_tools_from_path_list()

# Set the knob defaults from mynk config
mynk.knobs.set_knob_defaults_from_config()





