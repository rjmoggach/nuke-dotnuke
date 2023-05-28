# ----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
version = "1.2"
releaseDate = "February 06 2018"

# ----------------------------------------------------------------------------------------------------------
#
# LICENSE
#
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
# import modules
# ----------------------------------------------------------------------------------------------------------

import nuke, nukescripts

# Choose between PySide and PySide2 based on Nuke version
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
else:
    from PySide2 import QtGui, QtCore, QtWidgets

import os
import re

from datetime import datetime as dt
from getpass import getuser


# ----------------------------------------------------------------------------------------------------------


def backdropper(nodeClass="Backdrop"):
    """
    Create node, ask user for text to put in the label. Coloirze node based on label.
    """

    # create panel instance
    panel = nuke.Panel(nodeClass)
    panel.addSingleLineInput("label", "")
    if panel.show():
        label = panel.value("label")

        if nodeClass == "StickyNote":
            label = "   %s   " % label.upper()
            node = nuke.createNode(nodeClass, inpanel=False)

        else:
            node = nukescripts.autoBackdrop()

        fontSize = preferencesNode.knob("backdropper%sFontSize" % nodeClass).value()
        node.knob("note_font_size").setValue(fontSize)

        if label:
            # set label
            node.knob("label").setValue(label)

            # colorize
            colorizeNode(node)

        else:
            # open properties
            nuke.show(node)


# ----------------------------------------------------------------------------------------------------------
# Node colors
# ----------------------------------------------------------------------------------------------------------


def indexKeywordColors():
    """
    Build color dictionary.
    """
    colorList = []
    colorsDict = {}

    for number in range(presetSlots):
        number += 1

        stringKnob = "backdropperColor%s" % str(number).zfill(2)
        colorKnob = "backdropperColor%sColor" % str(number).zfill(2)

        keys = [
            key for key in preferencesNode.knob(stringKnob).value().split(" ") if key
        ]

        # case sensitive
        if not preferencesNode.knob("backdropperCaseSensitive").value():
            keys = [key.lower() for key in keys]

        color = preferencesNode.knob(colorKnob).value()

        for key in keys:
            colorList.append(key)
            colorsDict[key] = color

    return colorList, colorsDict


def colorizeNode(node):
    """
    Set color for selected shuffle nodes
    """

    keywordList, keywordDict = indexKeywordColors()
    colorNamesList = reversed(sorted(colorNamesDict.keys(), key=len))

    nodeLabel = node.knob("label").value()

    # order
    # 0 = keywords first, 1 = color names first
    order = int(preferencesNode.knob("backdropperOrder").getValue() * 2 - 1)

    colorLists = [colorNamesList, keywordList][::order]
    colorDicts = [colorNamesDict, keywordDict][::order]

    for index, keys in enumerate(colorLists):
        label = nodeLabel

        if (
            not preferencesNode.knob("backdropperCaseSensitive").value()
            or keys == colorList
        ):
            label = label.lower()

        for key in keys:
            if key in label:
                node.knob("tile_color").setValue(colorDicts[index][key])
                return


# ----------------------------------------------------------------------------------------------------------
# Default colors
# ----------------------------------------------------------------------------------------------------------


def indexDefaultColors():
    # matplotlibColors is turning out to be problematic
    # only seems to works for certain  versions of Nuke, etc.
    # So I decided to just past the color dict in here directly...
    # Very neat, I know...
    colors = {
        "indigo": "#4B0082",
        "gold": "#FFD700",
        "hotpink": "#FF69B4",
        "firebrick": "#B22222",
        "indianred": "#CD5C5C",
        "yellow": "#FFFF00",
        "mistyrose": "#FFE4E1",
        "darkolivegreen": "#556B2F",
        "olive": "#808000",
        "darkseagreen": "#8FBC8F",
        "pink": "#FFC0CB",
        "tomato": "#FF6347",
        "lightcoral": "#F08080",
        "orangered": "#FF4500",
        "navajowhite": "#FFDEAD",
        "lime": "#00FF00",
        "palegreen": "#98FB98",
        "darkslategrey": "#2F4F4F",
        "greenyellow": "#ADFF2F",
        "burlywood": "#DEB887",
        "seashell": "#FFF5EE",
        "mediumspringgreen": "#00FA9A",
        "fuchsia": "#FF00FF",
        "papayawhip": "#FFEFD5",
        "blanchedalmond": "#FFEBCD",
        "chartreuse": "#7FFF00",
        "dimgray": "#696969",
        "black": "#000000",
        "peachpuff": "#FFDAB9",
        "springgreen": "#00FF7F",
        "aquamarine": "#7FFFD4",
        "white": "#FFFFFF",
        "orange": "#FFA500",
        "lightsalmon": "#FFA07A",
        "darkslategray": "#2F4F4F",
        "brown": "#A52A2A",
        "ivory": "#FFFFF0",
        "dodgerblue": "#1E90FF",
        "peru": "#CD853F",
        "darkgrey": "#A9A9A9",
        "lawngreen": "#7CFC00",
        "chocolate": "#D2691E",
        "crimson": "#DC143C",
        "forestgreen": "#228B22",
        "slateblue": "#6A5ACD",
        "lightseagreen": "#20B2AA",
        "cyan": "#00FFFF",
        "mintcream": "#F5FFFA",
        "silver": "#C0C0C0",
        "antiquewhite": "#FAEBD7",
        "mediumorchid": "#BA55D3",
        "skyblue": "#87CEEB",
        "gray": "#808080",
        "darkturquoise": "#00CED1",
        "goldenrod": "#DAA520",
        "darkgreen": "#006400",
        "floralwhite": "#FFFAF0",
        "darkviolet": "#9400D3",
        "darkgray": "#A9A9A9",
        "moccasin": "#FFE4B5",
        "saddlebrown": "#8B4513",
        "grey": "#808080",
        "darkslateblue": "#483D8B",
        "lightskyblue": "#87CEFA",
        "lightpink": "#FFB6C1",
        "mediumvioletred": "#C71585",
        "slategrey": "#708090",
        "red": "#FF0000",
        "deeppink": "#FF1493",
        "limegreen": "#32CD32",
        "darkmagenta": "#8B008B",
        "palegoldenrod": "#EEE8AA",
        "plum": "#DDA0DD",
        "turquoise": "#40E0D0",
        "lightgrey": "#D3D3D3",
        "lightgoldenrodyellow": "#FAFAD2",
        "darkgoldenrod": "#B8860B",
        "lavender": "#E6E6FA",
        "maroon": "#800000",
        "yellowgreen": "#9ACD32",
        "sandybrown": "#FAA460",
        "thistle": "#D8BFD8",
        "violet": "#EE82EE",
        "navy": "#000080",
        "magenta": "#FF00FF",
        "dimgrey": "#696969",
        "tan": "#D2B48C",
        "rosybrown": "#BC8F8F",
        "olivedrab": "#6B8E23",
        "blue": "#0000FF",
        "lightblue": "#ADD8E6",
        "ghostwhite": "#F8F8FF",
        "honeydew": "#F0FFF0",
        "cornflowerblue": "#6495ED",
        "linen": "#FAF0E6",
        "darkblue": "#00008B",
        "powderblue": "#B0E0E6",
        "seagreen": "#2E8B57",
        "darkkhaki": "#BDB76B",
        "snow": "#FFFAFA",
        "sienna": "#A0522D",
        "mediumblue": "#0000CD",
        "royalblue": "#4169E1",
        "lightcyan": "#E0FFFF",
        "green": "#008000",
        "mediumpurple": "#9370DB",
        "midnightblue": "#191970",
        "cornsilk": "#FFF8DC",
        "paleturquoise": "#AFEEEE",
        "bisque": "#FFE4C4",
        "slategray": "#708090",
        "darkcyan": "#008B8B",
        "khaki": "#F0E68C",
        "wheat": "#F5DEB3",
        "teal": "#008080",
        "darkorchid": "#9932CC",
        "deepskyblue": "#00BFFF",
        "salmon": "#FA8072",
        "darkred": "#8B0000",
        "steelblue": "#4682B4",
        "palevioletred": "#DB7093",
        "lightslategray": "#778899",
        "aliceblue": "#F0F8FF",
        "lightslategrey": "#778899",
        "lightgreen": "#90EE90",
        "orchid": "#DA70D6",
        "gainsboro": "#DCDCDC",
        "mediumseagreen": "#3CB371",
        "lightgray": "#D3D3D3",
        "mediumturquoise": "#48D1CC",
        "lemonchiffon": "#FFFACD",
        "cadetblue": "#5F9EA0",
        "lightyellow": "#FFFFE0",
        "lavenderblush": "#FFF0F5",
        "coral": "#FF7F50",
        "purple": "#800080",
        "aqua": "#00FFFF",
        "whitesmoke": "#F5F5F5",
        "mediumslateblue": "#7B68EE",
        "darkorange": "#FF8C00",
        "mediumaquamarine": "#66CDAA",
        "darksalmon": "#E9967A",
        "beige": "#F5F5DC",
        "blueviolet": "#8A2BE2",
        "azure": "#F0FFFF",
        "lightsteelblue": "#B0C4DE",
        "oldlace": "#FDF5E6",
    }

    defaultColors = {}

    for colorName in colors.keys():
        hexColor = colors[colorName]
        colorValue = hex2interface(hexColor)

        for prefix in ["deep", "dark", "medium", "light"]:
            colorName = colorName.replace(prefix, prefix + " ")

        defaultColors[colorName] = colorValue

    return defaultColors


def hex2interface(hexColor):
    """
    Convert a color stored as hex values to a 32 bit value as used by nuke for interface colors.
    """
    hexColor = hexColor.lstrip("#")
    rgb = tuple(int(hexColor[i : i + 2], 16) for i in (0, 2, 4))
    rgb += (255,)

    return int("%02x%02x%02x%02x" % rgb, 16)


# ----------------------------------------------------------------------------------------------------------
# Menu item
# ----------------------------------------------------------------------------------------------------------


def setMenuItem(itemName):
    """
    Change the shortcut of the menu item of the defined nodeclass.
    """

    otherMenu = nuke.menu("Nodes").findItem("Other")

    index = nodeClasses.index(itemName)

    replace = int(
        preferencesNode.knob("backdropper%sReplaceMenuItem" % itemName).value()
    )

    customItemName = itemName + " (W_backdropper)"

    # don't replace
    if not replace:
        # restore original
        function = originalMenuItemScripts[index]
        menuItem = otherMenu.addCommand(itemName, function, icon=itemName + ".png")

    # replace
    else:
        # remove if applicable
        if otherMenu.findItem(customItemName):
            otherMenu.removeItem(customItemName)

    # new item
    shortcut = preferencesNode.knob("backdropper%sShortcut" % itemName).value()
    function = 'W_backdropper.backdropper("%s")' % itemName
    menuItem = otherMenu.addCommand(
        [customItemName, itemName][replace], function, shortcut, icon=itemName + ".png"
    )


# ----------------------------------------------------------------------------------------------------------
# Preferences
# ----------------------------------------------------------------------------------------------------------


def addKnobToPreferences(knobObject, tooltip=None):
    """
    Add a knob to the preference panel.
    Save current preferences to the prefencesfile in the .nuke folder.
    """

    if knobObject.name() not in preferencesNode.knobs().keys():
        if tooltip != None:
            knobObject.setTooltip(tooltip)

        preferencesNode.addKnob(knobObject)
        savePreferencesToFile()

        return preferencesNode.knob(knobObject.name())


def savePreferencesToFile():
    """
    Save current preferences to the prefencesfile in the .nuke folder.
    Pythonic alternative to the 'ok' button of the preferences panel.
    """

    nukeFolder = os.path.expanduser("~") + "/.nuke/"
    preferencesFile = nukeFolder + "preferences{0}.{1}.nk".format(
        nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR
    )

    preferencesNode = nuke.toNode("preferences")

    customPrefences = preferencesNode.writeKnobs(
        nuke.WRITE_USER_KNOB_DEFS
        | nuke.WRITE_NON_DEFAULT_ONLY
        | nuke.TO_SCRIPT
        | nuke.TO_VALUE
    )
    customPrefences = customPrefences.replace("\n", "\n  ")

    preferencesCode = (
        "Preferences {\n inputs 0\n name Preferences%s\n}" % customPrefences
    )

    # write to file
    openPreferencesFile = open(preferencesFile, "w")
    openPreferencesFile.write(preferencesCode)
    openPreferencesFile.close()


def deletePreferences(clicked=False):
    """
    Delete all the W_backdropper related items from the properties panel.
    """

    firstLaunch = True

    for knobName in preferencesNode.knobs().keys():
        if knobName.startswith("backdropper"):
            preferencesNode.removeKnob(preferencesNode.knob(knobName))
            firstLaunch = False

    # remove TabKnob
    try:
        preferencesNode.removeKnob(preferencesNode.knob("backdropperLabel"))
    except:
        pass

    if not firstLaunch:
        savePreferencesToFile()

    if clicked:
        # click the cancel button
        closePreferencesPanel()

        # re open panel
        openPreferencesPanel()


def resetPreferences():
    """
    Reset all the W_backdropper related knobs to their default values.
    """

    # colorknobs
    for number in range(presetSlots):
        number = str(number + 1).zfill(2)

        knob = "backdropperColor%s" % number
        preferencesNode.knob(knob).setValue("")

        knob += "Color"
        preferencesNode.knob(knob).setValue(defaultColor)

    for index, knob in enumerate(["Backdrop", "StickyNote"]):
        preferencesNode.knob("backdropper%sFontSize" % knob).setValue(
            defaultFontSizes[index]
        )


def updatePreferences(forceUpdate=False):
    """
    Check whether the script was updated since the last launch. If so refresh the preferences.
    """

    allKnobs = preferencesNode.knobs().keys()

    # always update if beta version
    if "b" in version:
        forceUpdate = True

    # check if current version differs from the previously loaded version.
    if "backdropperVersion" in allKnobs and not forceUpdate:
        if version == str(preferencesNode.knob("backdropperVersion").value()):
            return

    currentSettings = {
        knob: preferencesNode.knob(knob).value()
        for knob in allKnobs
        if knob.startswith("backdropper") and knob != "backdropperVersion"
    }

    # amount of slots
    if "backdropperSlotCount" in preferencesNode.knobs().keys():
        global presetSlots
        presetSlots = min(
            50, max(0, int(preferencesNode.knob("backdropperSlotCount").value()))
        )

    # delete all the preferences
    deletePreferences()

    # re-add all the knobs
    addPreferences()

    # restore settings
    for knob in currentSettings.keys():
        try:
            preferencesNode.knob(knob).setValue(currentSettings[knob])
        except:
            pass

    # save to file
    savePreferencesToFile()


def closePreferencesPanel(save=False):
    """
    Find and invoke a button found at the bottom of the preferences panel.
    """

    buttonText = ["Cancel", "OK"][int(save)]
    preferencesButton = None

    # find preferences
    for widget in QtWidgets.QApplication.instance().allWidgets():
        if widget.objectName() == "foundry.hiero.preferencesdialog":
            # loop over children
            for child in widget.children():
                if isinstance(child, QtWidgets.QDialogButtonBox):
                    # buttons
                    for button in child.buttons():
                        if button.text() == buttonText:
                            preferencesButton = button
                            break
                    break
            break

    if preferencesButton:
        preferencesButton.click()


def updateSlotCount():
    """
    Update the slot count.
    """

    # close panel and save
    closePreferencesPanel(True)
    # update knobs
    updatePreferences(True)
    # close panel
    openPreferencesPanel()


def openPreferencesPanel():
    """
    Open the preferences panel
    """

    event = QtGui.QKeyEvent(
        QtCore.QEvent.KeyPress, QtCore.Qt.Key_S, QtCore.Qt.ShiftModifier
    )
    nukeInstance = QtWidgets.QApplication.instance()
    nukeInstance.postEvent(nukeInstance, event)


def addPreferences():
    """
    Add knobs to the preferences needed for this module to work properly.
    """

    # tab
    addKnobToPreferences(nuke.Tab_Knob("backdropperLabel", "W_backdropper"))

    # version knob to check whether the backdropper was updated
    knob = nuke.String_Knob("backdropperVersion", "version")
    knob.setValue(version)
    knob.setVisible(False)
    addKnobToPreferences(knob)

    # case sensitive
    knob = nuke.Boolean_Knob("backdropperCaseSensitive", "Case sensitive")
    knob.setValue(False)
    tooltip = "Only colorize nodes when the casing is matching."
    addKnobToPreferences(knob, tooltip)

    # case sensitive
    knob = nuke.Boolean_Knob("backdropperRecognizeColors", "Recognize color names")
    knob.setValue(True)
    # knob.clearFlag(nuke.STARTLINE)
    tooltip = 'Change the color of the node whenever it\'s label contains a color name (eg. color the node red when the label contains the word "red").'
    addKnobToPreferences(knob, tooltip)

    # Rule/Class order
    knob = nuke.Enumeration_Knob(
        "backdropperOrder", "", ["Keywords - Color names", "Color names - Keywords"]
    )
    knob.clearFlag(nuke.STARTLINE)
    tooltip = "Order of importance regarding matching a label of a node to a color."
    addKnobToPreferences(knob, tooltip)

    addKnobToPreferences(nuke.Text_Knob("backdropperKeywordLabel", "<b>Keywords</b>"))

    # colorknobs
    for number in range(int(presetSlots)):
        number = str(number + 1).zfill(2)

        name = "backdropperColor%s" % number
        knob = nuke.String_Knob(name, "")
        tooltip = "The labels that will have the given default color."

        addKnobToPreferences(knob, tooltip)

        name += "Color"
        knob = nuke.ColorChip_Knob(name, "")
        knob.setValue(defaultColor)
        knob.clearFlag(nuke.STARTLINE)
        tooltip = "The default color for the given labels."

        addKnobToPreferences(knob, tooltip)

    for nodeClass in nodeClasses:
        index = nodeClasses.index(nodeClass)

        addKnobToPreferences(
            nuke.Text_Knob("backdropper%sLabel" % nodeClass, "<b>%s</b>" % nodeClass)
        )

        # backdrop font size
        knob = nuke.Int_Knob("backdropper%sFontSize" % nodeClass, "Font size")
        knob.setValue(defaultFontSizes[index])
        tooltip = "Default font size for the label of %s nodes." % nodeClass
        addKnobToPreferences(knob, tooltip)

        # backdrop shortcut knob
        knob = nuke.String_Knob("backdropper%sShortcut" % nodeClass, "    Shortcut ")
        knob.setValue("Alt+" + ["b", "n"][index])
        knob.clearFlag(nuke.STARTLINE)
        tooltip = "Shortcut to create a %s node." % nodeClass
        addKnobToPreferences(knob, tooltip)

        # change shortcut

        knob = nuke.PyScript_Knob(
            "backdropper%sSetShortcut" % nodeClass,
            "set",
            'W_backdropper.setMenuItem("%s")' % nodeClass,
        )
        tooltip = "Apply shortcut."
        addKnobToPreferences(knob, tooltip)

        # replace sticky note
        knob = nuke.Boolean_Knob("backdropper%sReplaceMenuItem" % nodeClass, "replace")
        knob.setValue(False)
        tooltip = "Replace original menu item."
        addKnobToPreferences(knob, tooltip)

    addKnobToPreferences(nuke.Text_Knob("backdropperPreferences", "<b>Preferences</b>"))

    # slot count
    knob = nuke.Int_Knob("backdropperSlotCount", "Slots")
    knob.setValue(presetSlots)
    tooltip = "The amount of slots available to the user."
    addKnobToPreferences(knob, tooltip)

    # set slot count
    knob = nuke.PyScript_Knob(
        "backdropperUpdateSlotCount", "set", "W_backdropper.updateSlotCount()"
    )
    tooltip = "Reset all the W_backdropper related knobs to their default values."
    addKnobToPreferences(knob, tooltip)

    # import preferences button knob
    knob = nuke.PyScript_Knob(
        "backdropperImportExportPreferences",
        " import/export ",
        "W_backdropper.importExportPanel()",
    )
    tooltip = "Reset all the W_backdropper related knobs to their default values."
    addKnobToPreferences(knob, tooltip)

    # delete preferences button knob
    knob = nuke.PyScript_Knob(
        "backdropperResetPreferences", "clear", "W_backdropper.resetPreferences()"
    )
    tooltip = "Reset all the W_backdropper related knobs to their default values."
    addKnobToPreferences(knob, tooltip)

    # delete preferences button knob
    knob = nuke.PyScript_Knob(
        "backdropperDeletePreferences",
        " uninstall ",
        "W_backdropper.deletePreferences(True)",
    )
    tooltip = "Delete all the W_backdropper related knobs from the Preferences Panel. After clicking this button the Preferences Panel should be closed by clicking the 'cancel' button."
    addKnobToPreferences(knob, tooltip)


# ----------------------------------------------------------------------------------------------------------
# Import/Export
# ----------------------------------------------------------------------------------------------------------


class ImportExportWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ImportExportWidget, self).__init__()

        self.setParent(QtWidgets.QApplication.instance().activeWindow())
        self.setWindowFlags(QtCore.Qt.Tool)

        dividerLine = "-" * 106
        self.header = [
            "#%s" % dividerLine,
            "#",
            "# W_BACKDROPPER SETTINGS FILE",
            "#",
            "# CREATED ON {0} BY {1}".format(
                dt.now().strftime("%A %d %B %Y (%H:%M)").upper(), getuser().upper()
            ),
            "#",
            "#%s\n\n" % dividerLine,
        ]
        self.header = "\n".join(self.header)

        # --------------------------------------------------------------------------------------------------

        self.clipboardRadioButton = QtWidgets.QRadioButton("Clipboard")
        self.clipboardRadioButton.setChecked(True)

        self.fileRadioButton = QtWidgets.QRadioButton("File")
        self.fileRadioButton.toggled.connect(self.toggleFileWidgets)

        modeLayout = QtWidgets.QHBoxLayout()
        modeLayout.addStretch()
        for widget in [self.clipboardRadioButton, self.fileRadioButton]:
            modeLayout.addWidget(widget)
        modeLayout.addStretch()

        # --------------------------------------------------------------------------------------------------

        self.pathLabel = QtWidgets.QLabel("Path")
        self.pathLineEdit = QtWidgets.QLineEdit("")
        self.pathButton = QtWidgets.QPushButton("Browse")
        self.pathButton.clicked.connect(self.browseFile)

        self.toggleFileWidgets()

        pathLayout = QtWidgets.QHBoxLayout()
        for widget in [self.pathLabel, self.pathLineEdit, self.pathButton]:
            pathLayout.addWidget(widget)

        # --------------------------------------------------------------------------------------------------

        self.importButton = QtWidgets.QPushButton("Import")
        self.importButton.clicked.connect(self.importSettings)

        self.exportButton = QtWidgets.QPushButton("Export")
        self.exportButton.clicked.connect(self.exportSettings)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.close)

        buttonLayout = QtWidgets.QHBoxLayout()
        for widget in [self.importButton, self.exportButton, self.cancelButton]:
            buttonLayout.addWidget(widget)

        # --------------------------------------------------------------------------------------------------

        mainLayout = QtWidgets.QVBoxLayout()

        for layout in [modeLayout, pathLayout, LineWidget(), buttonLayout]:
            if isinstance(layout, QtWidgets.QHBoxLayout):
                mainLayout.addLayout(layout)
            else:
                mainLayout.addWidget(layout)

        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(mainLayout)

        # --------------------------------------------------------------------------------------------------

        self.adjustSize()
        self.move(
            QtGui.QCursor().pos()
            - QtCore.QPoint((self.width() / 2), (self.height() / 2))
        )

    def toggleFileWidgets(self):
        """
        Disable parts of the interface when the switch checkbox changes state
        """

        state = self.fileRadioButton.isChecked()

        for widget in [self.pathLineEdit, self.pathButton]:
            widget.setEnabled(state)

    def browseFile(self):
        """
        Launch browser to navigate to the desired file
        """
        extension = ".backdropper"
        filePath = nuke.getFilename("W_backdropper", "*" + extension)
        if filePath:
            if not filePath.endswith(extension):
                filePath += extension

            self.pathLineEdit.setText(filePath)

    def exportSettings(self):
        """
        Export the current settings to either a file or the clipboard.
        """

        settings = preferencesNode.writeKnobs(nuke.TO_VALUE | nuke.WRITE_USER_KNOB_DEFS)

        # replace numbers with placeholder
        indexPlaceHolder = "_*BACKDROPINDEX*_"
        settings = re.sub(
            r"(?<=backdropperColor)([0-9]{2})(?<![\s C])", indexPlaceHolder, settings
        )

        settings = settings.split("\n")
        settings = [line for line in settings if "backdropperColor" in line]

        # split in chunks of four (textinput and colorswatch, adduserknob command and the stored value)
        settings = [settings[index : index + 4] for index in range(0, len(settings), 4)]

        settings = [
            line
            for line in settings
            if not (line[1].split()[-1] == '""' and line[3].split()[-1] == "0xccccccff")
        ]

        settings = ["\n".join(line) for line in settings]
        settings = [
            line.replace(indexPlaceHolder, str(index + 1).zfill(2))
            for index, line in enumerate(settings)
        ]

        settings = "\n".join(settings)

        settings = self.header + settings

        if self.fileRadioButton.isChecked():
            location = self.pathLineEdit.text()
            with open(location, "w") as file:
                file.write(settings)

        else:
            QtWidgets.QApplication.clipboard().setText(settings)
            location = "clipboard"

        nuke.message(
            "W_backdropper settings succesfully writen to {0}.".format(location)
        )
        self.close()

    def importSettings(self):
        """
        Import settings from either a file or the clipboard.
        """

        preferencesKnobs = preferencesNode.knobs().keys()
        slotPrefix = "backdropperColor"

        if self.fileRadioButton.isChecked():
            location = self.pathLineEdit.text()
            if not location.endswith(".backdropper"):
                nuke.message("Invalid file")
                return

            with open(location) as file:
                settings = file.read()

        else:
            settings = QtWidgets.QApplication.clipboard().text()

        # remove header and split in lines
        settings = [
            line for line in settings.split("\n") if line and not line.startswith("#")
        ]

        # filter addUserKnob line for knobs that are already present
        for line in settings[::1]:
            if line.startswith("addUserKnob"):
                for word in line.split(" "):
                    if word.startswith(slotPrefix):
                        if word in preferencesKnobs:
                            settings.remove(line)
                        break

        settings = "\n".join(settings)

        # apply
        preferencesNode.readKnobs(settings)

        # count slots
        slotCount = len(
            [
                knob
                for knob in preferencesNode.knobs().keys()
                if knob.startswith("backdropperColor") and knob[-1].isdigit()
            ]
        )

        slotCountKnob = preferencesNode.knob("backdropperSlotCount")
        if slotCount != slotCountKnob.value():
            slotCountKnob.setValue(slotCount)

            # save to disk and close preferences
            closePreferencesPanel(True)
            updatePreferences(True)
            openPreferencesPanel()

        self.close()


class LineWidget(QtWidgets.QFrame):
    def __init__(self):
        super(LineWidget, self).__init__()

        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


def importExportPanel():
    """
    Open panel to allow the user to export or import settings.
    """
    global importExportPanelInstance
    try:
        importExportPanelInstance.close()
    except:
        pass

    importExportPanelInstance = ImportExportWidget()
    importExportPanelInstance.show()


# ----------------------------------------------------------------------------------------------------------


def colorizeNodes(all=False):
    """
    Colorize all nodes of a specific class. Pick colors according to their labels.
    """

    nodeClasses = ["BackdropNode", "StickyNote"]

    # selection
    if all:
        selection = nuke.allNodes()

        # create panel instance
        panel = nuke.Panel(
            "W_backdropper - Colorize %s nodes" % ["selected", "all"][int(all)]
        )

        for nodeClass in nodeClasses:
            panel.addBooleanCheckBox(nodeClass, True)

        if panel.show():
            for nodeClass in nodeClasses:
                if not panel.value(nodeClass):
                    nodeClasses.remove(nodeClass)

    else:
        selection = nuke.selectedNodes()

    # selection
    selection = [node for node in selection if node.Class() in nodeClasses]

    for node in selection:
        colorizeNode(node)


# ----------------------------------------------------------------------------------------------------------

colorNamesDict = indexDefaultColors()
preferencesNode = nuke.toNode("preferences")
importExportPanelInstance = None

defaultColor = 3435973887
defaultFontSizes = [42, 11]

presetSlots = 15

nodeClasses = ["Backdrop", "StickyNote"]

originalMenuItemScripts = [
    nuke.menu("Nodes").findItem("Other/" + nodeClass).script()
    for nodeClass in nodeClasses
]


def init():
    # preferences
    updatePreferences()

    # node menu items
    for nodeClass in nodeClasses:
        setMenuItem(nodeClass)

    # edit menu items
    menu = nuke.menu("Nuke").findItem("&Edit/Node")
    menu = menu.addMenu("W_backdropper")

    for nodeClass in nodeClasses:
        menu.addCommand("Colorize selected nodes", colorizeNodes)
        menu.addCommand("Colorize all nodes", lambda: colorizeNodes(True))


# ----------------------------------------------------------------------------------------------------------

init()
