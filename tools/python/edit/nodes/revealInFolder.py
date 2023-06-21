import platform
import os

NAUTILUS_CMD = "/usr/bin/nautilus"
KONQUEROR_CMD = "/usr/bin/konqueror"
DOLPHIN_CMD = "/usr/bin/dolphin"
MACOSX_CMD = "open"
WINDOWS_CMD = "explorer"
MAX_NODES = 4

# SHORT CUT SYNTAX
# 'Ctrl-s' "^s"
# 'Ctrl-Shift-s' "^+s"
# 'Alt-Shift-s' "#+s"
# 'Shift+F4' "+F4"
file_manager = "/usr/bin/dolphin"
# file_manager ='/usr/bin/thunar'

if platform.system() == "Linux":
    BROWSER = "Dolphin"
elif platform.system() == "Darwin":
    BROWSER = "Finder"
else:
    BROWSER = "Explorer"

__menus__ = {
    "Edit/Nodes/Show in {0}".format(BROWSER): {
        "cmd": "openup()",
        "hotkey": "#r",
        "icon": "",
    }
}


"""======================================================================================================================
DEVELOPER: Tor Andreassen - www.fxtor.net
DATE: June 12, 2022
VERSION: v2.2 (nuke13)

DESCRIPTION:

    This script loops through all selected nodes and checks if the node has a file knob.
    If a file knob is present, the path will be opened in the OS file manager/browser.
    The user will be notified if nothing is selected or if the user does not select any nodes that have an existing file-path.
    If a selected node has a nonexistent path, this will be printed in the script editor, and the script will continue to process
    the next selected node.

    When opening multiple file paths that all have the same folder, only one instance of the folder will be opened (to avoid opening duplicate paths).

    OS Support: Windows, OSX, Linux

    Supports: Existing paths of the type:

        - scripted paths (for example, paths made up of TCL)
        - local paths
        - server paths


USAGE:

    copy this python file into your .nuke directory/fxT_tools/fxt_reveal_in_folder
    copy the icon files into your .nuke directory/icons/fxT_icons


    put this in your init.py file:

        # add nuke plugin paths for fxT tools and icons
        nuke.pluginAddPath('./fxT_tools/fxT_reveal_in_folder')
        nuke.pluginAddPath('./fxT_tools/icons/')


    put this in your menu.py file:

        # add fxT menu
        sideBar = nuke.menu('Nodes')
        fxT = sideBar.addMenu('fxT', icon='fxT_menuicon.png')

        # add fxT_revealInFolder to the fxT menu
        import fxT_reveal_in_folder
        fxT.addCommand('fxT_revealInFolder', 'fxT_reveal_in_folder.openup()', icon='openInFolder.png')


NOTES:

    Place these icons and python files in the suggested paths above or wherever your NUKE_PATH is located.
    If you don't have a meny.py file or an init.py file, create one and place it in your .nuke directory or wherever your NUKE_PATH is located.

    As there is no standard file manager on Linux, I have chosen to set the file manager/browser for Linux as a fixed variable.
    This can be set in the 'fxT_set_linux_file_manager.py' file, where you can also find instructions for how to set your chosen file manager.


======================================================================================================================"""
import nuke
import nukescripts
import os
import sys
import time
import subprocess

# import fxT_set_linux_file_manager


def reveal_in_folder():
    # set variables for OS platform and selected nodes
    platform = sys.platform
    selected_nodes = nuke.selectedNodes()
    # linux_browser = fxT_set_linux_file_manager.file_manager
    linux_browser = file_manager

    # if nothing is selected: throw popup message at user and exit the function
    if not selected_nodes:
        nuke.message("Nothing is selected, no file(s) to open.")
        return 0

    # save all selected nodes with a file-knob to a list, except the Viewer-node
    has_file_knob = []

    for i in selected_nodes:
        if "file" in i.knobs() and not i.name().startswith("Viewer"):
            has_file_knob.append(i)

    # if no selected node(s) has a file knob: throw popup message at user and exit the function
    if not has_file_knob:
        nuke.message(
            "No file(s) to open.\n\nThis tool can only open the folder of the selected node(s) if one or more file-knobs exists."
        )
        return 0

    # loop over the saved list of nodes that has file-knobs to generate the correct directory path

    for i in has_file_knob:
        # get the evaluated path of the file knob (to ensure scripted paths will work)
        file_knob = i.knob("file").evaluate()

        # save the original evaluated path of the file knob for later use
        original_file_knob = file_knob

        # testing that the file-knob text input field is not empty
        # and that it is not a write node; write nodes are handled separately (see below)

        if file_knob:
            # get the directory path
            nuke_directory = os.path.dirname(file_knob)

            # if the directory exists, do stuff
            if os.path.isdir(nuke_directory):
                # generating paths with OS specific separators
                nuke_folder = nuke_directory.split(
                    "/"
                )  # splitting on '/' since Nuke always works with forward slashes
                os_folder = ""

                # if user is running on Windows, generate Windows specific paths
                if platform.startswith("win"):
                    # Windows local paths:

                    if not original_file_knob.startswith("//"):
                        win_drive = nuke_folder[0]
                        os_folder = nuke_folder[1:]
                        os_folder = os.path.join("", *os_folder)
                        os_folder = win_drive + os.sep + os_folder

                    # Windows server paths:
                    if original_file_knob.startswith("//"):
                        os_folder = os.sep + os.path.join(os.sep, *nuke_folder)

                else:
                    # if user is not running Windows: generate Unix paths:
                    os_folder = os.path.join(os.sep, *nuke_folder)

                # get start of filename
                filename_start = os.path.basename(original_file_knob)
                filename_start = filename_start.split(".")
                filename_start = filename_start[0]

                # get extension of filename
                filename_end = os.path.basename(original_file_knob)
                filename_end = filename_end.split(".")
                filename_end = filename_end[-1]

                # loop throw directory to get a valid filename
                for file in os.listdir(os_folder):
                    # if filename start and ends with the same name as what is in the file_knob: grab the first filename in the directory
                    # then break out of the loop as one only need one matching filename to verify that the file exists.
                    # PS: .startswith() and .endswith() will not guarantee a perfect file match, but it gives some leeway if the filename
                    # for example is accidentally changed while this tool is running, and it allows for both sequences and singles files
                    # (it will skip padding matching).

                    # create variable to test against for an existing file path
                    real_path = ""
                    if file.startswith(filename_start) and file.endswith(filename_end):
                        filename = file

                        if platform.startswith("win"):
                            # local path Windows
                            if not original_file_knob.startswith("//"):
                                # removing string-escape, windows paths (regular vs server paths) might need reworking (currently don't have a test case)
                                # this should now work for non-server paths at least
                                # real_path = str(os_folder.encode('string-escape'))+os.sep+os.sep+filename
                                real_path = os_folder + os.sep + filename

                            # server path for Windows
                            else:
                                real_path = os_folder + os.sep + filename

                        # paths for Unix
                        else:
                            real_path = os_folder + os.sep + filename

                            # if user is opening multiple paths: wait for 0.5 seconds to not process code too fast (avoiding dropped paths on OSX):
                            # (0.3) seems to be enough wait time, but using (0.5) to make sure slower computers don't have any problems

                            if len(has_file_knob) > 1:
                                time.sleep(0.5)

                        # break out of the loop as one only need one filename to confirm an existing path (to not loop over large sequences of files)
                        break

                # if file exists in the selected node(s): open directory path in the OS browser.
                if os.path.isfile(real_path):
                    # print what node and filepath is being opened in the script editor
                    print(
                        "{name}: Opening folder; {folder}".format(
                            name=i.name(), folder=os_folder
                        )
                    )

                    # open in OS browser
                    open_path = os.path.dirname(os_folder + os.sep)

                    if platform.startswith("win") or platform == "darwin":
                        nukescripts.start(open_path)

                        # if opening multiple paths: wait for 0.5 seconds to let Finder and 3rd party browsers not drop any paths due to python executing
                        # code while process is still processing. (0.3) seems to be enough wait time. However, using (0.5)
                        # to make sure slower computers don't have any problems

                        if len(has_file_knob) > 1:
                            time.sleep(0.5)

                    elif platform.startswith("linux"):
                        subprocess.Popen([linux_browser, open_path])

                        if len(has_file_knob) > 1:
                            time.sleep(0.5)
                else:
                    # if the file does not exist: printing useful info in the script editor
                    display_file_dir = original_file_knob.replace("/", os.sep)
                    print(
                        "{name}: Nonexistent file-path; {filedir}".format(
                            name=i.name(), filedir=display_file_dir
                        )
                    )

            else:
                # if the directory does not exist: printing useful info in the script editor
                # printing the directory path of the original file_knob with correct OS separators
                # if the user tries to open a path that only have characters and no folders, print the raw string
                display_dir = original_file_knob

                if "/" in display_dir:
                    display_dir = display_dir.split("/")
                    display_dir = display_dir[0:-1]
                    display_dir = "/".join(display_dir)
                    display_dir = display_dir.replace("/", os.sep)

                print(
                    "{name}: Nonexistent directory-path; {displaydir}".format(
                        name=i.name(), displaydir=display_dir
                    )
                )


def openup():
    return reveal_in_folder()
