# ----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
# version = 1.0
# releaseDate = 'December 8 2018'

# ----------------------------------------------------------------------------------------------------------
# MENU.PY
# ----------------------------------------------------------------------------------------------------------

"""

import W_dontUseNativeMenuBar
W_dontUseNativeMenuBar.init()

"""

# ----------------------------------------------------------------------------------------------------------
# LICENSE
# ----------------------------------------------------------------------------------------------------------

"""
Copyright (c) 2018, Wouter Gilsing
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Redistribution of this software in source or binary forms shall be free
      of all charges or fees to the recipient of this software.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# ----------------------------------------------------------------------------------------------------------

import nuke

if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
else:
    from PySide2 import QtGui, QtCore, QtWidgets


def init():
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
