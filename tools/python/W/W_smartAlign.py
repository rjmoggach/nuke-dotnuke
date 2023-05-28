# ----------------------------------------------------------------------------------------------------------
# Wouter Gilsing
# woutergilsing@hotmail.com
# May 2016
# v1.1
# ----------------------------------------------------------------------------------------------------------

# menuBar.addCommand('Edit/Node/Align/Left', 'W_smartAlign.alignNodes("left")', 'Ctrl+Alt+left', shortcutContext=2)
__menus__ = {
    "Edit/Node/Align/Left": {
        "cmd": 'alignNodes("left")',
        "hotkey": "Ctrl+Alt+left",
        "icon": "",
    },
    "Edit/Node/Align/Right": {
        "cmd": 'alignNodes("right")',
        "hotkey": "Ctrl+Alt+right",
        "icon": "",
    },
    "Edit/Node/Align/Up": {
        "cmd": 'alignNodes("up")',
        "hotkey": "Ctrl+Alt+up",
        "icon": "",
    },
    "Edit/Node/Align/Down": {
        "cmd": 'alignNodes("down")',
        "hotkey": "Ctrl+Alt+down",
        "icon": "",
    },
}

import nuke
import operator


def alignNodes(direction):
    # --------------------------------------
    # USER SETTINGS
    # when nodes are about to overlap as a result of an alignment, the nodes are placed next to each other instead.
    # the multiplier variables define the amount of space that's kept between the nodes
    # 1 is default, the higher the multiplier, the more space.
    # --------------------------------------
    multiplierX = 1
    multiplierY = 1
    # --------------------------------------

    selection = nuke.selectedNodes()
    dontmove = False

    if direction in ["left", "right"]:
        axis = "x"
        index = 0
    else:
        axis = "y"
        index = 1

    # --------------------------------------
    # MULTIPLE NODES
    # if multiple nodes are selected, all the nodes will align to the node that's the furthest away in the specified direction
    # --------------------------------------

    if len(selection) > 1:
        allPos = [[], []]
        for i in selection:
            allPos[0].append(i.knob("xpos").value() + (getScreenSize(i)[0]))
            allPos[1].append(i.knob("ypos").value() + (getScreenSize(i)[1]))

        # check whether all selected nodes already share the same position values to prevent overlapping
        # if so, do nothing
        if not allPos[1 - index].count(allPos[1 - index][0]) == len(allPos[1 - index]):
            if direction in ["left", "up"]:
                destination = min(allPos[index])
            else:
                destination = max(allPos[index])
        else:
            dontmove = True

    # --------------------------------------
    # SINGLE NODE
    # if only one node is selected, the selected node will snap to the nearest connected node (both input and output) in the specified direction
    # --------------------------------------

    elif len(selection) == 1:
        curNode = selection[0]

        # create a list of all the connected nodes
        inputNodes = curNode.dependencies()
        outputNodes = curNode.dependent()

        # remove nodes with hidden inputs and viewer nodes,
        # as you probably wouldn't want to snap to those
        # not every node has a hide input knob (read node for example), so use a "try" in case it hasn't
        for i in outputNodes:
            try:
                if i.knob("hide_input").value() or i.Class() == "Viewer":
                    outputNodes.remove(i)
            except:
                pass

        if curNode.knob("hide_input"):
            if curNode.knob("hide_input").value():
                inputNodes = []

        connectedNodes = inputNodes + outputNodes

        # create a list for every connected node containing the following [xpos,ypos,relative xpos, relative ypos, node]
        # store those lists in an other list

        positions = []

        for i in connectedNodes:
            xPos = i.xpos() + getScreenSize(i)[0]
            yPos = i.ypos() + getScreenSize(i)[1]
            curNodexPos = curNode.xpos() + getScreenSize(curNode)[0]
            curNodeyPos = curNode.ypos() + getScreenSize(curNode)[1]

            positions.append([xPos, yPos, xPos - curNodexPos, yPos - curNodeyPos, i])

        # sort the list based on the relative positions
        sortedList = sorted(positions, key=operator.itemgetter(index + 2))

        # remove nodes from list to make sure the first item is the node closest to the curNode
        # use the operator module to switch dynamically between ">=" and "<="
        # the positiveDirection variable is used later to correctly calculate to offset in case nodes are about to overlap
        if direction in ["right", "down"]:
            equation = operator.le
            positiveDirection = -1
        else:
            sortedList.reverse()
            equation = operator.ge
            positiveDirection = 1

        try:
            while equation(sortedList[0][index + 2], 0):
                sortedList.pop(0)
        except:
            pass

        # checking whether there are nodes to align to in the desired direction
        # if there are none, don't move the node
        if len(sortedList) != 0:
            destination = sortedList[0][index]

            curPosition = [curNodexPos, curNodeyPos]
            destinationPosition = [curNodexPos, curNodeyPos]
            destinationPosition[index] = destination

            # remove the relative positions from the positionlist
            for i in range(len(positions)):
                positions[i] = [positions[i][:2], positions[i][-1]]

            # Making sure the nodes won't overlap after being aligned.
            # If they are about to overlap the node will be placed next to the node it tried to snap to.
            for i in positions:
                # calculate the difference between the destination and the position of the node it will align to
                difference = [
                    (abs(i[0][0] - destinationPosition[0])) * 1.5,
                    (abs(i[0][1] - destinationPosition[1])) * 1.5,
                ]

                # define the amount of units a node should offsetted to not overlap
                offsetX = 0.75 * (
                    3 * getScreenSize(curNode)[0] + getScreenSize(i[1])[0]
                )
                offsetY = 3 * getScreenSize(curNode)[1] + getScreenSize(i[1])[1]
                offsets = [int(offsetX), int(offsetY)]

                # check in both directions whether the node is about to overlap:
                if difference[0] < offsets[0] and difference[1] < offsets[1]:
                    multiplier = [multiplierX, multiplierY][index]
                    offset = positiveDirection * multiplier * offsets[index]

                    # find out whether the nodes are already very close to each other
                    # (even closer than they would be after aligning)
                    # don't move the node if that's the case
                    if abs(offset) < abs(destination - curPosition[index]):
                        destination = destination + offset

                    else:
                        dontmove = True

                    # stop looping through the list when a suitable node to align to is found
                    break
        else:
            dontmove = True

    else:
        dontmove = True

    # --------------------------------------
    # MOVE THE SELECTED NODES
    # --------------------------------------

    nuke.Undo().name("Align Nodes")
    nuke.Undo().begin()

    for i in selection:
        if not dontmove:
            if axis == "x":
                i.setXpos(int(destination - getScreenSize(i)[index]))
            else:
                i.setYpos(int(destination - getScreenSize(i)[index]))

    nuke.Undo().end()


def getScreenSize(node):
    # --------------------------------------
    # To get the position of a node in the DAG you can use the xpos/ypos knobs.
    # However, that position is heavely influenced by the size of the node.
    # When horizontally aligned, a Dot node will have a different ypos than a blur node for example.
    # To neuralize a nodes postionvalues you have to add the half the nodes screen dimensions to the positionvalues.
    # --------------------------------------

    return [node.screenWidth() / 2, node.screenHeight() / 2]


# --------------------------------------
# EXAMPLE MENU.PY CODE
# --------------------------------------

"""
import W_smartAlign

menuBar = nuke.menu("Nuke")
menuBar.addCommand("Edit/Node/Align/Left", 'W_smartAlign.alignNodes("left")', "Alt+left", shortcutContext=2)
menuBar.addCommand("Edit/Node/Align/Right", 'W_smartAlign.alignNodes("right")', "Alt+right", shortcutContext=2)
menuBar.addCommand("Edit/Node/Align/Up", 'W_smartAlign.alignNodes("up")', "Alt+up", shortcutContext=2)
menuBar.addCommand("Edit/Node/Align/Down", 'W_smartAlign.alignNodes("down")', "Alt+down", shortcutContext=2)

"""
