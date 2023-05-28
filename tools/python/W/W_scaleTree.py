# ----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
# March 2018
# v2.2
# ----------------------------------------------------------------------------------------------------------

import nuke
import os
from nukescripts import panels

__menus__ = {}

# Choose between PySide and PySide2 based on Nuke version
if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore, QtGui, QtGui as QtWidgets
else:
    from PySide2 import QtGui, QtCore, QtWidgets

# ----------------------------------------------------------------------------------------------------------
# Add to menu.py:
# ----------------------------------------------------------------------------------------------------------
"""
import W_scaleTree
nukeMenu.addCommand('Edit/Node/W_scaleTree', 'W_scaleTree.scaleTreeFloatingPanel()', 'alt+`')
"""
# ----------------------------------------------------------------------------------------------------------

# Location of the icons
iconFolder = os.getenv("HOME") + "/.nuke/icons/W_scaleTree"

# ----------------------------------------------------------------------------------------------------------


class scaleTreeWidget(QtWidgets.QWidget):
    def __init__(self):
        super(scaleTreeWidget, self).__init__()

        self.setWindowTitle("W_scaleTree")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(250)

        masterLayout = QtWidgets.QVBoxLayout()

        # --------------------------------------------------------------------------------------------------
        # Pivot manipulator
        # --------------------------------------------------------------------------------------------------

        self.setPivotWidget = pivotWidget()

        # add to layout
        pivotLayout = QtWidgets.QHBoxLayout()
        pivotLayout.addStretch()
        pivotLayout.addLayout(self.setPivotWidget)
        pivotLayout.addStretch()

        # --------------------------------------------------------------------------------------------------
        # Parameters
        # --------------------------------------------------------------------------------------------------

        self.ignore = False

        # --------------------------------------------------------------------------------------------------
        # Sliders
        # --------------------------------------------------------------------------------------------------

        sliderLayout = QtWidgets.QVBoxLayout()

        self.maxSlider = 200

        # uniform
        self.uniformSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.uniformSlider.setMinimum(0)
        self.uniformSlider.setMaximum(self.maxSlider)
        self.uniformSlider.setValue(self.maxSlider / 2)

        self.uniformSlider.sliderPressed.connect(self.scanTree)
        self.uniformSlider.sliderMoved.connect(
            lambda: self.scaleTree(self.uniformSlider, ["horizontal", "vertical"])
        )
        self.uniformSlider.sliderReleased.connect(self.resetSlider)

        # horizontal
        self.horizontalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.maxSlider)
        self.horizontalSlider.setValue(self.maxSlider / 2)

        self.horizontalSlider.sliderPressed.connect(self.scanTree)
        self.horizontalSlider.valueChanged.connect(
            lambda: self.scaleTree(self.horizontalSlider, ["horizontal"])
        )
        self.horizontalSlider.sliderReleased.connect(self.resetSlider)

        # vertical
        self.verticalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.verticalSlider.setMinimum(0)
        self.verticalSlider.setMaximum(self.maxSlider)
        self.verticalSlider.setValue(self.maxSlider / 2)

        self.verticalSlider.sliderPressed.connect(self.scanTree)
        self.verticalSlider.valueChanged.connect(
            lambda: self.scaleTree(self.verticalSlider, ["vertical"])
        )
        self.verticalSlider.sliderReleased.connect(self.resetSlider)

        # add to layout
        sliderLayout.addSpacing(25)
        sliderLayout.addWidget(QtWidgets.QLabel("Uniform"))
        sliderLayout.addWidget(self.uniformSlider)
        sliderLayout.addSpacing(25)
        sliderLayout.addWidget(QtWidgets.QLabel("Horizontal"))
        sliderLayout.addWidget(self.horizontalSlider)
        sliderLayout.addWidget(QtWidgets.QLabel("Vertical"))
        sliderLayout.addWidget(self.verticalSlider)

        # --------------------------------------------------------------------------------------------------
        # Spacing
        # --------------------------------------------------------------------------------------------------
        distributionLayout = QtWidgets.QVBoxLayout()
        distributionButtonLayout = QtWidgets.QHBoxLayout()

        self.horizontalButton = QtWidgets.QPushButton("Horizontal")
        self.verticalButton = QtWidgets.QPushButton("Vertical")

        self.horizontalButton.clicked.connect(lambda: self.distributeEvenly("x"))
        self.verticalButton.clicked.connect(lambda: self.distributeEvenly("y"))

        distributionButtonLayout.addStretch()
        distributionButtonLayout.addWidget(self.horizontalButton)
        distributionButtonLayout.addSpacing(10)
        distributionButtonLayout.addWidget(self.verticalButton)
        distributionButtonLayout.addStretch()

        distributionLayout.addWidget(QtWidgets.QLabel("Distribute Evenly"))
        distributionLayout.addLayout(distributionButtonLayout)

        # --------------------------------------------------------------------------------------------------
        # Assamble UI
        # --------------------------------------------------------------------------------------------------

        masterLayout.addSpacing(25)
        masterLayout.addLayout(pivotLayout)
        masterLayout.addSpacing(25)
        masterLayout.addLayout(sliderLayout)
        masterLayout.addSpacing(25)
        masterLayout.addLayout(distributionLayout)
        masterLayout.addSpacing(10)
        masterLayout.addStretch()

        self.setLayout(masterLayout)

        # --------------------------------------------------------------------------------------------------
        # Add shortcuts
        # --------------------------------------------------------------------------------------------------

        # quit
        try:
            self.closeAction = QtWidgets.QAction(self)
            shortcut = nuke.menu("Nuke").findItem("Edit/Node/W_scaleTree").shortcut()
            self.closeAction.setShortcut(QtGui.QKeySequence().fromString(shortcut))
            self.closeAction.triggered.connect(self.close)
            self.addAction(self.closeAction)
        except:
            pass

        # corners

        self.setPivotActionTL = QtWidgets.QAction(self)
        self.setPivotActionTR = QtWidgets.QAction(self)
        self.setPivotActionBL = QtWidgets.QAction(self)
        self.setPivotActionBR = QtWidgets.QAction(self)

        self.setPivotActionTL.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_1))
        self.setPivotActionTR.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_2))
        self.setPivotActionBL.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_3))
        self.setPivotActionBR.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_4))

        self.setPivotActionTL.triggered.connect(
            lambda: self.setPivotWidget.allButtons[0].mouseReleaseEvent("")
        )
        self.setPivotActionTR.triggered.connect(
            lambda: self.setPivotWidget.allButtons[2].mouseReleaseEvent("")
        )
        self.setPivotActionBL.triggered.connect(
            lambda: self.setPivotWidget.allButtons[6].mouseReleaseEvent("")
        )
        self.setPivotActionBR.triggered.connect(
            lambda: self.setPivotWidget.allButtons[8].mouseReleaseEvent("")
        )

        self.addAction(self.setPivotActionTL)
        self.addAction(self.setPivotActionTR)
        self.addAction(self.setPivotActionBL)
        self.addAction(self.setPivotActionBR)

        # --------------------------------------------------------------------------------------------------

        # Spawn widget at current location of cursor
        self.adjustSize()
        self.move(
            QtGui.QCursor().pos()
            - QtCore.QPoint((self.width() / 2), (self.height() / 2))
        )

        # set pivot to center
        self.setPivotWidget.allButtons[4].mouseReleaseEvent("")

    def getDAG(self):
        """
        Return the currently opened DAG in order to work correctly with groups.
        """

        rootNode = nuke.Root()

        # collect all DAG's
        allDAGWidgets = [
            w
            for w in QtWidgets.QApplication.instance().allWidgets()
            if "DAG" in w.objectName()
        ]

        for w in allDAGWidgets:
            if w.isVisible():
                windowTitle = w.windowTitle()
                if windowTitle != "Node Graph":
                    rootNode = nuke.toNode(windowTitle.split(" ")[0])
                    break

        return rootNode

    def getSelection(self):
        """
        Get selected nodes for active DAG.
        """

        with self.getDAG():
            selection = nuke.selectedNodes()

        return selection

    def scanTree(self):
        """
        Calculate all need information regarding the current selection. Before doing any actual scaling.
        This method is called when the user starts dragging one of the sliders.
        """

        selection = self.getSelection()

        # if there are less than two nodes selected. Don't do any scaling at all
        if len(selection) < 2:
            self.ignore = True
            self.undo = None
            return

        # Dictionary of all nodes with current position values. {[Node object] : (x pos, y position)}
        # Positions are all neutralized by taking the size of the node in account.

        self.nodePositions = {}

        allXpos = []
        allYpos = []

        for node in selection:
            # create lists and a dictionary storing position data
            if node.Class() != "BackdropNode":
                x = node.xpos() + (node.screenWidth() / 2)
                y = node.ypos() + (node.screenHeight() / 2)

                self.nodePositions[node] = (x, y)

                allXpos.append(x)
                allYpos.append(y)

            else:
                # If a backdrop node is encountered, store the width and height as well as the regular position data.

                # store the nodes inside the backdrop in a list
                backdropSelection = node.getNodes()

                if len(backdropSelection) > 0:
                    allPositionData = [
                        [n.xpos(), n.ypos(), n.screenWidth(), n.screenHeight()]
                        for n in backdropSelection
                    ]

                    selectionX = min([pos[0] + (pos[2] / 2) for pos in allPositionData])
                    selectionY = min([pos[1] + (pos[3] / 2) for pos in allPositionData])

                    selectionW = max([pos[0] + (pos[2] / 2) for pos in allPositionData])
                    selectionH = max([pos[1] + (pos[3] / 2) for pos in allPositionData])

                    offsetX = node.xpos() - selectionX
                    offsetY = node.ypos() - selectionY
                    offsetW = (node.xpos() + node.knob("bdwidth").value()) - selectionW
                    offsetH = (node.ypos() + node.knob("bdheight").value()) - selectionH

                    self.nodePositions[node] = (
                        selectionX,
                        selectionY,
                        selectionW,
                        selectionH,
                        offsetX,
                        offsetY,
                        offsetW,
                        offsetH,
                    )

                else:
                    # if backdrop is empty, threat it as any other node
                    x = node.xpos() + (node.screenWidth() / 2)
                    y = node.ypos() + (node.screenHeight() / 2)

                    self.nodePositions[node] = (x, y)

                    allXpos.append(x)
                    allYpos.append(y)

        # calculate the most extreme values to define the borders of the selection
        minXpos = min(allXpos)
        maxXpos = max(allXpos)

        maxYpos = max(allYpos)
        minYpos = min(allYpos)

        # set the pivotpoint
        self.pivotX = (maxXpos * self.setPivotWidget.pivot[0]) + (
            minXpos * (1 - self.setPivotWidget.pivot[0])
        )
        self.pivotY = (maxYpos * self.setPivotWidget.pivot[1]) + (
            minYpos * (1 - self.setPivotWidget.pivot[1])
        )

        self.ignore = False

        # add the scaling of the nodes to the stack of preformed actions to offer the user the option to undo it.
        self.undo = nuke.Undo()
        self.undo.begin("Scale Nodes")

    def scaleTree(self, slider, mode):
        """
        Scale the currently selected nodes.
        This method is called when the user is actually moving one of the sliders.
        """

        if not self.ignore:
            multiplier = float(slider.value()) / (self.maxSlider / 2)
            # make the slider act exponential rather than linear when the value is above 1.
            if multiplier > 1:
                multiplier *= multiplier

            for i in self.nodePositions.keys():
                if len(self.nodePositions[i]) == 2:
                    # wehn dealing with a backdrop node, not only adjust the postion but also the scale.

                    if "horizontal" in mode:
                        screenWidth = i.screenWidth() / 2
                        newPos = int(
                            (
                                self.pivotX
                                - (
                                    (self.pivotX - self.nodePositions[i][0])
                                    * multiplier
                                )
                            )
                            - screenWidth
                        )
                        i.setXpos(newPos)

                    if "vertical" in mode:
                        screenHeight = i.screenHeight() / 2
                        newPos = int(
                            (
                                self.pivotY
                                - (
                                    (self.pivotY - self.nodePositions[i][1])
                                    * multiplier
                                )
                            )
                            - screenHeight
                        )
                        i.setYpos(newPos)

                else:
                    if "horizontal" in mode:
                        newPos = (
                            int(
                                self.pivotX
                                - (
                                    (self.pivotX - self.nodePositions[i][0])
                                    * multiplier
                                )
                            )
                            + self.nodePositions[i][4]
                        )
                        newWidth = (
                            int(
                                (
                                    self.pivotX
                                    - (
                                        (self.pivotX - self.nodePositions[i][2])
                                        * multiplier
                                    )
                                )
                                + self.nodePositions[i][6]
                            )
                            - newPos
                        )

                        i.knob("bdwidth").setValue(newWidth)
                        i.setXpos(newPos)

                    if "vertical" in mode:
                        newPos = (
                            int(
                                self.pivotY
                                - (
                                    (self.pivotY - self.nodePositions[i][1])
                                    * multiplier
                                )
                            )
                            + self.nodePositions[i][5]
                        )
                        newHeight = (
                            int(
                                (
                                    self.pivotY
                                    - (
                                        (self.pivotY - self.nodePositions[i][3])
                                        * multiplier
                                    )
                                )
                                + self.nodePositions[i][7]
                            )
                            - newPos
                        )

                        i.knob("bdheight").setValue(newHeight)
                        i.setYpos(newPos)

    def resetSlider(self):
        # reset the sliders when the user releases the mouse.
        # use the ignore variable to make sure the nodes in the DAG are not affected by this.

        currentIgnoreValue = self.ignore
        self.ignore = True
        self.uniformSlider.setValue(self.maxSlider / 2)
        self.horizontalSlider.setValue(self.maxSlider / 2)
        self.verticalSlider.setValue(self.maxSlider / 2)
        self.ignore = currentIgnoreValue

        if self.undo:
            self.undo.end()

    def getScreenSize(self, node, axis):
        if axis == "x":
            return node.screenWidth() / 2
        else:
            return node.screenHeight() / 2

    def distributeEvenly(self, axis):
        """
        Equalize the amount of space between selected nodes.
        """

        selection = self.getSelection()

        allPositionsDict = {}

        for node in selection:
            position = float(
                node.knob(axis + "pos").value() + self.getScreenSize(node, axis)
            )

            if position in allPositionsDict.keys():
                allPositionsDict[position].append(node)
            else:
                allPositionsDict[position] = [node]

        allPositions = sorted(allPositionsDict.keys())

        amount = len(allPositions)
        if amount < 3:
            return

        minPos = allPositions[0]
        maxPos = allPositions[-1]

        stepSize = (maxPos - minPos) / (amount - 1)

        self.undo = nuke.Undo()
        self.undo.begin("Distribute evenly")

        for index, i in enumerate(allPositions):
            newPos = minPos + index * stepSize
            for node in allPositionsDict[i]:
                node.knob(axis + "pos").setValue(
                    newPos - self.getScreenSize(node, axis)
                )

        self.undo.end()
        self.undo = None


# ----------------------------------------------------------------------------------------------------------


class pivotWidget(QtWidgets.QGridLayout):
    """
    A widget that let's the user interactivaly set a pivot point fro where the nodes in the DAG will be scaled.
    """

    def __init__(self):
        super(pivotWidget, self).__init__()

        self.allButtons = []

        self.setSpacing(0)
        for i in range(9):
            button = pivotButton(self, i)
            self.addWidget(button, i / 3, i % 3)
            self.allButtons.append(button)

        self.pivot = (0.5, 0.5)

    def updateButtons(self, buttonID):
        for i in self.allButtons:
            i.update(buttonID)


# ----------------------------------------------------------------------------------------------------------


class pivotButton(QtWidgets.QLabel):
    """
    The buttons that are used to built the pivotWidget.
    """

    def __init__(self, parent, position):
        super(pivotButton, self).__init__()

        self.parent = parent
        self.position = position

        # make sure the path to the icon folder doesn't end with a slash
        global iconFolder
        while iconFolder[-1] == "/":
            iconFolder = iconFolder[:-1]

        self.imageFile = "%s/W_scaleTree_pivotArrow_%i.png" % (iconFolder, position)

        self.setPixmap(QtGui.QPixmap(self.imageFile))

    def mouseReleaseEvent(self, event):
        # set pivot
        self.parent.updateButtons(self.position)
        self.parent.pivot = [(self.position % 3) / 2.0, (self.position / 3) / 2.0]

    def update(self, buttonID):
        """
        Change the icon of the buttons when the user changes the pivot.
        """

        # the button in the center of the widget has index 4
        offset = 4 - buttonID

        newPosition = self.position + offset

        # when placing the pivot in one of the side tiles,
        # tiles will reappear on the other side of the widget (like snake)
        # make sure that doesn't happen by forcing those tiles to be empty.
        for i in [[0, 3, 6], [2, 5, 8]]:
            if buttonID in i and newPosition in i:
                newPosition = 9
                break

        # there are only 9 icons (9 being an empty tile).
        # if a button ends up getting a new postion outside this range,
        # force those tiles to be empty.
        if newPosition not in range(9):
            newPosition = 9

        # set new icons
        self.imageFile = "%s/W_scaleTree_pivotArrow_%i.png" % (iconFolder, newPosition)
        self.setPixmap(QtGui.QPixmap(self.imageFile))


# ----------------------------------------------------------------------------------------------------------
# Floating Panel
# ----------------------------------------------------------------------------------------------------------

scaleTreeWidgetInstance = None


def scaleTreeFloatingPanel():
    global scaleTreeWidgetInstance
    if scaleTreeWidgetInstance != None:
        try:
            scaleTreeWidgetInstance.close()
        except:
            pass

    scaleTreeWidgetInstance = scaleTreeWidget()
    scaleTreeWidgetInstance.show()


# ----------------------------------------------------------------------------------------------------------
# Docked Panel
# ----------------------------------------------------------------------------------------------------------

panels.registerWidgetAsPanel(
    "W_scaleTree.scaleTreeWidget", "W_scaleTree", "W_scaleTree.widget"
)

# ----------------------------------------------------------------------------------------------------------
