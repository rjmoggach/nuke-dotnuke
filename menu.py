import os
import inspect
import sys
import builtins
import nuke

if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
else:
    from PySide2 import QtGui, QtCore, QtWidgets


# Set a globally accessible attribute called DOTNUKE_PATH
# this code should be used carefully with full knowledge of the implications
# We do this HERE because init.py would generally imply a non-gui
# mission-critical functionality and we're looking to extend the gui only
# ie. We don't want renders failing all over the place!!!
DOTNUKE_PATH = os.path.dirname(inspect.getfile(sys._getframe(0)))
builtins.DOTNUKE_PATH = DOTNUKE_PATH


if nuke.GUI:
    # MyNk personal workspace
    # ----------------------------------
    import mynk

    # Initialize the custom menu and toolbar
    mynk.gui.init_gui()

    # Set the format defaults
    mynk.formats.add_formats_from_config()

    # Set the knob defaults from mynk config
    mynk.knobs.set_knob_defaults_from_config()

    # Load the python tools from the mynk config'd path
    # if you want to add paths, add them one line at a time as follows
    # the following example is the default so not necessary to add
    # as it will find it if no other paths have been added
    #
    # mynk.tools.add_path('~/.nuke/tools/python')
    #
    mynk.tools.add_python_tools_from_path_list()

    mynk.gui.add_toolmunch_to_menu("mynk.tools.python")

    # nuke.tprint('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    # nuke_tb = nuke.menu("Nodes")
    # mynk_mnu = nuke_tb.addMenu("FOOOBAR", "mynk.png")
    # mynk_mnu.addCommand("Read", "nukescripts.create_read()", "r", icon="Read.png")
    # mynk_mnu.addCommand("Write", "nuke.createNode(\"Write\")", "w", icon="Write.png")

    # nuke.pluginAddPath('/Users/rob/.nuke/mygui', addToSysPath=False)

    # try:
    #   import DeadlineNukeClient
    #   menubar = nuke.menu("Nuke")
    #   tbmenu = menubar.addMenu("&Thinkbox")
    #   tbmenu.addCommand("Submit Nuke To Deadline", DeadlineNukeClient.main, "")
    #   try:
    #       if nuke.env[ 'studio' ]:
    #           import DeadlineNukeFrameServerClient
    #           tbmenu.addCommand("Reserve Frame Server Slaves", DeadlineNukeFrameServerClient.main, "")
    #   except:
    #       pass
    # except:
    #   pass


def guiMenuBar():
    """
    Prevent Nuke from using the native OS toolbar (like on macOS) and use the Nuke's default Qt toolbar instead.
    This will allow the user to work properly in fullscreen mode on a Mac without losing/hiding the menubar.
    Besides that the toolbar will behave like any other part of the interface.
    """
    # loop over all toplevel widgets and find all QMenuBars
    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        for child in widget.children():
            if isinstance(child, QtWidgets.QMenuBar):
                if child.isNativeMenuBar():
                    child.setNativeMenuBar(False)
                    return True

    return False


# guiMenuBar()
