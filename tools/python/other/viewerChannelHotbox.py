# -*- coding: utf-8 -*-

"""
channel Hotbox v1.3 for Nuke
by Falk Hofmann, Vancouver, 2013
all rights reserved
falk@kombinat-13b.de

import hotbox
nuke.menu("Nuke").findItem("Edit").addCommand("HotBox", 'hotbox.create_it()', "`")

"""

import math
import nuke
from PySide2 import QtGui, QtWidgets


class LayerButton(QtWidgets.QPushButton):
    def __init__(self, name, butWidth, parent=None):
        super(LayerButton, self).__init__(parent)
        self.setMouseTracking(True)
        self.setText(name)

        # self.setMinimumWidth ( butWidth/2 )
        self.setStyleSheet(" background-color:#282828;  font:  13px ")

    def enterEvent(self, event):
        self.setStyleSheet("background-color:#C26828; font: 13px")

    def leaveEvent(self, event):
        self.setStyleSheet("background-color:#282828; font:  13px ")


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent, layerlist):
        super(LineEdit, self).__init__(parent)
        layer = []
        for i in layerlist:
            layer.append(i)
        self.completerList = []
        self.completer = QtGui.QCompleter(layer, self)
        self.completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.setCompleter(self.completer)
        self.completer.activated.connect(self.clicked)

    def clicked(self):
        nuke.activeViewer().node()["channels"].setValue(self.text())


class HotBox(QtWidgets.QWidget):
    def __init__(self):
        super(HotBox, self).__init__()

        av = nuke.activeViewer().node()
        vn = av.input(nuke.activeViewer().activeInput()).name()

        channels = nuke.toNode(vn).channels()
        layer = list(set([c.split(".")[0] for c in channels]))
        layer.sort()

        if "rgba" in layer:
            layer.remove("rgba")
            layer.insert(0, "rgba")
            if "rgb" in layer:
                layer.remove("rgb")
                layer.insert(1, "rgb")
                if "alpha" in layer:
                    layer.remove("alpha")
                    layer.insert(2, "alpha")
            elif "alpha" in layer:
                layer.remove("alpha")
                layer.insert(1, "alpha")

        length = math.ceil(math.sqrt(len(layer) + 1))

        width = length * 200
        height = length * 50
        point = QtGui.QCursor.pos()
        offsetX = width * 0.5
        offsetY = height * 0.5

        offset = QtCore.QPoint(offsetX, offsetY)
        point -= offset

        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.move(point)
        self.setWindowTitle("Hotbox")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        length = math.ceil(math.sqrt(len(layer) + 1))
        columnCounter = 0
        rowCounter = 0
        butWidth = width / length

        for i in layer:
            button = LayerButton(i, butWidth)
            button.clicked.connect(
                self.clicked,
            )
            button.setSizePolicy(
                QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding
            )
            grid.addWidget(button, rowCounter, columnCounter)

            if columnCounter > length:
                rowCounter = rowCounter + 1
                columnCounter = 0
            else:
                columnCounter = columnCounter + 1

            self.input = LineEdit(self, layer)
            self.input.setSizePolicy(
                QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding
            )
            grid.addWidget(self.input, rowCounter, columnCounter)
            self.input.returnPressed.connect(self.lineEnter)
            self.input.setFocus()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def clicked(self):
        modifiers = QtGui.QApplication.keyboardModifiers()

        if modifiers == QtCore.Qt.ControlModifier:
            node = nuke.toNode(
                nuke.activeViewer()
                .node()
                .input(nuke.activeViewer().activeInput())
                .name()
            )
            shuffle = nuke.nodes.Shuffle(
                xpos=(node.xpos() + 100), ypos=(node.ypos()), label=self.sender().text()
            )
            shuffle["in"].setValue(self.sender().text())
            shuffle.setInput(0, node)
            super(HotBox, self).close()

        else:
            nuke.activeViewer().node()["channels"].setValue(self.sender().text())
            super(HotBox, self).close()

    def lineClicked(self, item):
        self.input.setText(item.text())
        self.enter()
        self.close()

    def lineEnter(self):
        nuke.activeViewer().node()["channels"].setValue(self.input.text())
        self.close()


woop = None


def create_it():
    global woop
    woop = HotBox()
    woop.show()
