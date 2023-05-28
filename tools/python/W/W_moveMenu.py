# ----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
# 4 July 2017
# v1.0
# ----------------------------------------------------------------------------------------------------------
__menus__ = {}

import nuke

# Choose between PySide and PySide2 based on Nuke version
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
else:
    from PySide2 import QtGui, QtCore, QtWidgets

# ----------------------------------------------------------------------------------------------------------


def moveMenu(
    sourceMenuNames,
    destinationMenuName,
    icon,
    sourceRoot,
    destinationRoot,
    remove,
    contentsOnly,
):
    """
    Move a menu into another menu.
    """

    # if string instead of list, convert to list
    if isinstance(sourceMenuNames, basestring):
        sourceMenuNames = [sourceMenuNames]

    if not destinationRoot:
        destinationRoot = sourceRoot

    sourceRoot = nuke.menu(sourceRoot)
    destinationRoot = nuke.menu(destinationRoot)

    if not sourceRoot or not destinationRoot:
        return

    # ------------------------------------------------------------------------------------------------------

    if destinationMenuName:
        # check if menu entries with same name as desired destination menu exists
        allCommands = [
            menu.name()
            for menu in destinationRoot.items()
            if not isinstance(menu, nuke.Menu)
        ]
        destinationMenu = nameCheck(destinationMenuName, allCommands)

        # if destination menu is part of the source menu's as well, find another name for the destination.
        if sourceRoot == destinationRoot:
            if destinationMenu in sourceMenuNames:
                allItems = [menu.name() for menu in sourceRoot.items()]
                destinationMenu = nameCheck(destinationMenu, allItems)

        # ------------------------------------------------------------------------------------------------------

        # if destination menu already exists, use that. Otherwise, create a new one.
        if destinationRoot.menu(destinationMenu):
            destinationMenu = destinationRoot.menu(destinationMenu)

        else:
            destinationMenu = destinationRoot.addMenu(destinationMenu, icon)

    else:
        destinationMenu = destinationRoot

    # ------------------------------------------------------------------------------------------------------

    # move menus
    for menuName in sourceMenuNames:
        menuItem = sourceRoot.findItem(menuName)

        if menuItem:
            # add qmenu
            copyMenu(menuItem, destinationMenu, contentsOnly)

            # remove old menu
            if remove:
                parentMenu = sourceRoot

                sourceMenuName = menuName.strip("/").split("/")

                for submenu in sourceMenuName[:-1]:
                    parentMenu = parentMenu.findItem(submenu)

                parentMenu.removeItem(sourceMenuName[-1])

    # ------------------------------------------------------------------------------------------------------


def copyMenu(menu, destinationMenu, contentsOnly=False):
    """
    Copy a nuke.Menu into a new parent.
    """
    if isinstance(menu, nuke.Menu):
        if not contentsOnly:
            destinationMenu = destinationMenu.addMenu(menu.name())
        items = menu.items()
    else:
        items = [menu]

    for item in items:
        if isinstance(item, nuke.Menu):
            copyMenu(item, destinationMenu)
        else:
            destinationMenu.addAction(item.action())


def nameCheck(name, itemList):
    """
    Check if item present in given list, if so append with number. Return unique name.
    """

    if name in itemList:
        counter = 0
        baseName = name

        while name in itemList:
            counter += 1
            name = "%s_%s" % (baseName, counter)

    return name


def moveMenus(
    sourceMenus,
    destinationMenu="",
    icon="noIconDefined",
    sourceRoot="Nodes",
    destinationRoot="",
    remove=True,
    contentsOnly=False,
):
    """
    During the execution of the script Nuke will add and remove menus. However, since this happens before the gui is fully initialised,
    the menus are actually empty at the time. This can be worked around by deferring the menu creation using a QTimer.
    The 0 length timer will trigger when Qt events start being processed.
    Thanks to Foundy's support team/developers for clearifing this and coming up with a workaround.
    """

    QtCore.QTimer.singleShot(
        0,
        lambda: moveMenu(
            sourceMenus,
            destinationMenu,
            icon,
            sourceRoot,
            destinationRoot,
            remove,
            contentsOnly,
        ),
    )
