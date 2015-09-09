'''
#Install Guide

add this into your menu.py:
----------------------------------------
import fviewer as fv
fvlayer = ('rgba','none')
nuke.addOnCreate(fv.init, nodeClass='Preferences')
nuke.addOnCreate(fv.init, nodeClass='Root')
----------------------------------------

Author: Erwan Leroy
Website: www.erwanleroy.com
Version: 1.0
'''

import nuke

###################################################################################
#Preferences

def preferencesCreatedCallback():
    pref = nuke.toNode('preferences')

    #Setup J_Ops prefs knobs if they don't exist.
    try:
        fvKnobsPresent = pref["fv_tab"]
    except (SyntaxError, NameError):
        k = nuke.Tab_Knob('fv_tab', 'Flame Viewer')
        k.setFlag(nuke.ALWAYS_SAVE)
        pref.addKnob(k)

        k = nuke.Text_Knob('fv_explain', '', 'Flame Viewer lets you view your nodes like you would on a Flame:\nhaving a Front, Back, Matte and Result View.\n\nThe Front View will display your A stream\nThe Back View will display your B stream\nThe Matte view will display your mask input\nThe result will show the result of that (similar to nuke viewer)\n\nRestart of Nuke needed to Apply any change')
        k.setFlag(nuke.ALWAYS_SAVE)
        pref.addKnob(k)

        k = nuke.Boolean_Knob('fv_enable', 'Enable')
        k.setFlag(nuke.ALWAYS_SAVE)
        k.setValue(1.0)
        pref.addKnob(k)

        k = nuke.Text_Knob('')
        k.setFlag(nuke.ALWAYS_SAVE)
        pref.addKnob(k)

        k = nuke.Text_Knob('fv_keyboard', 'Keyboard Shortcuts')
        k.setFlag(nuke.ALWAYS_SAVE)
        pref.addKnob(k)

        k = nuke.String_Knob('fv_front', 'Front', 'F1')
        k.setFlag(nuke.ALWAYS_SAVE)
        pref.addKnob(k)

        k = nuke.String_Knob('fv_back', 'Front', 'F2')
        k.setFlag(nuke.ALWAYS_SAVE)
        k.clearFlag(nuke.STARTLINE)
        pref.addKnob(k)

        k = nuke.String_Knob('fv_matte', 'Front', 'F3')
        k.setFlag(nuke.ALWAYS_SAVE)
        pref.addKnob(k)

        k = nuke.String_Knob('fv_result', 'Front', 'F4')
        k.setFlag(nuke.ALWAYS_SAVE)
        k.clearFlag(nuke.STARTLINE)
        pref.addKnob(k)



###################################################################################
#Actual Function

def view(view = 'result', layer = ('rgba','none')):
    '''
    Mimics the behavior of the Flame Viewer: F1 displays your A layers, F2 your B layers, F3 your mask, and F4 the result (F4 is similar to regular viewer, but doesn't reassign a view)

    @param view: Which view to display (front/back/matte/result)
  @param layer: which layer was last seen, and what was the latest mask layer viewed. Allows us to switch back to the right layer when pressing F1/F2/F4 after viewing the matte
    @return: same tuple as the @param layer, for next time.
    '''
    try:
        node = nuke.selectedNode()
    except ValueError:
        print 'No node selected'
        return layer
    viewer = nuke.activeViewer().node()

    #Find Current Input
    currentInput = None
    for i in range(0,node.inputs()):
        if node.input(i) == viewer.input(10):
            currentInput = i
            break

    #Find Mask Input. Thanks to Ean Carr for the help here.
    if node.Class() == 'Merge2':
        maskInput = 2
    elif node.knobs().has_key('maskChannelMask') or node.knobs().has_key('maskChannel'):
        maskInput = node.minInputs() - 1
    else:
        maskInput = None

    #find the layer that we want to be reverting back to after viewing the mask
    fvlayer = viewer.knob('channels').value()
    lastLayer = layer[0]
    mask = layer[1]
    if fvlayer == mask or 'none':
        fvlayer = lastLayer

    #find what we want to see depending on the view
    if view == 'front':
        if maskInput == 1 or node.inputs() == 1:
            viewer.knob('channels').setValue('none')
        else:
            #check if current input is a front
            if currentInput != 0 and currentInput != maskInput and currentInput != None:
                front = currentInput + 1
                if front == maskInput:
                    front += 1
                if front >= node.inputs():
                    front = 1
            else:
                front = 1

            viewer.setInput(10,node.input(front))
            viewer.knob('channels').setValue(lastLayer)

    elif view == 'back':
        viewer.setInput(10,node.input(0))
        viewer.knob('channels').setValue(lastLayer)

    elif view == 'matte':
        if maskInput:
            #if mask input is connected take the value from that knob, otherwise connect to node and take value from knob "mask"
            if node.input(maskInput):
                if node.knobs().has_key('maskChannelMask'):
                    mask = node.knob('maskChannelMask').value()
                else:
                    mask = node.knob('maskChannel').value()
                viewer.setInput(10,node.input(maskInput))
            else:
                mask = node.knob('mask').value()
                viewer.setInput(10,node)
        else:
            mask = 'none'
            viewer.setInput(10,node)
        viewer.knob('channels').setValue(mask)

    elif view == 'result':
        viewer.setInput(10,node)
        viewer.knob('channels').setValue(lastLayer)

    else:
        return layer

    #activate that view
    viewer.knob('input_number').setValue(10)
    return (fvlayer, mask)

# Assign keyboard shotcuts for fvview
def init():
    #Run the settings
    preferencesCreatedCallback()

    #Check for preference settings
    pref = nuke.toNode('preferences')
    fvEnabled = pref["fv_enable"].getValue()
    frontKey = pref["fv_front"].getValue()
    backKey = pref["fv_back"].getValue()
    matteKey = pref["fv_matte"].getValue()
    resultKey = pref["fv_result"].getValue()

    if fvEnabled == True:
        nuke.menu( 'Nuke' ).addCommand( 'Viewer/FlameViewer/Front', "fvlayer = fv.view('front',fvlayer)", frontKey )
        nuke.menu( 'Nuke' ).addCommand( 'Viewer/FlameViewer/Back', "fvlayer = fv.view('back',fvlayer)", backKey )
        nuke.menu( 'Nuke' ).addCommand( 'Viewer/FlameViewer/Matte', "fvlayer = fv.view('matte',fvlayer)", matteKey )
        nuke.menu( 'Nuke' ).addCommand( 'Viewer/FlameViewer/Result', "fvlayer = fv.view('result',fvlayer)", resultKey )
