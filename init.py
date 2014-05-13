import os
import sys
import inspect

# System Path
# Add the current folder to the sys.path
sys.path.append(os.path.dirname(inspect.getfile(sys._getframe(0))))

import platform

#import mynk.settings
#from mynk.loader.python import NukePythonTools




# Python Tools
# this class allows us to import python files into our namespace
# and automagically import them and modules from
# a given path in our settings object
#nkTools = NukePythonTools(settings=mynk.settings, verbose=False)


# Filename Fix
# fix paths based on 
def filenameFix(filename):
  if platform.system() in ("Windows", "Microsoft"):
    filename = filename.replace( "/psyop/pfs", "P:" )
  else:
    filename = filename.replace( "P:", "/psyop/pfs" )
  return filename


import nuke
nuke_toolbar = nuke.menu("Nodes")
foot=nuke_toolbar.addMenu('Foooo', icon="mynk.png")
foot.addCommand('-','','')
