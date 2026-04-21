import os
import sys
import inspect

# System Path
# Add the current folder to the sys.path
DOTNUKE_PATH = os.path.dirname(inspect.getfile(sys._getframe(0)))
sys.path.append(DOTNUKE_PATH)

# Gizmo Path
# Add tools/gizmos to the nuke plugin path so gizmos are found
import nuke
nuke.pluginAddPath(os.path.join(DOTNUKE_PATH, "tools", "gizmos"))

import platform

# import mynk.settings
# from mynk.loader.python import NukePythonTools


# Python Tools
# this class allows us to import python files into our namespace
# and automagically import them and modules from
# a given path in our settings object
# nkTools = NukePythonTools(settings=mynk.settings, verbose=False)


# Filename Fix
# fix paths based on
# def filenameFix(filename):
#     if platform.system() in ("Windows", "Microsoft"):
#         filename = filename.replace( "/psyop/pfs", "P:" )
#     else:
#         filename = filename.replace( "P:", "/psyop/pfs" )
#     return filename


if nuke.GUI:
    try:
        import nuke
    except:
        print("Could not import: nuke")
    # try:
    #     import hiero_tools
    # except:
    #     print "Could not import: hiero_tools"
    nuke_toolbar = nuke.menu("Nodes")
    foot = nuke_toolbar.addMenu("Foooo", icon="mynk.png")
    foot.addCommand("-", "", "")
