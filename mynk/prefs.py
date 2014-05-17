# mynk -- a python library for enhancing a user's experience/workspace
# with the foundry's nuke
#
# @author: Robert Moggach <rob@moggach.com>
#
# mynk/prefs.py -- maybe we replace the config with prefs...hmmm
#


def preferencesCreatedCallback():
    p = nuke.toNode('preferences')
    
    try:
        jopsKnobsPresent = p["J_Ops"]
    except (SyntaxError, NameError):
        k = nuke.Tab_Knob("J_Ops")
        k.setFlag(nuke.ALWAYS_SAVE)
        p.addKnob(k)

        v = nuke.Double_Knob("j_ops_ver", "j_ops_ver")
        v.setFlag(nuke.ALWAYS_SAVE)
        v.setFlag(nuke.INVISIBLE)
        v.setValue(2.0101)
        p.addKnob(v)
        
        k = nuke.Boolean_Knob("j_ops_enable_drop", "Improved drag and drop")
        k.setFlag(nuke.ALWAYS_SAVE)
        k.setFlag(nuke.STARTLINE)
        k.setValue(1.0)
        k.setTooltip("Enable/disable a somewhat improved drag and drop behaviour. Requires Nuke restart to take effect. Adds creation of geo, camera, light and vectorfield nodes based on incoming file extensions, as well as support for sequences when dropping folders onto DAG. Warning: does not observe hash vs regex file path expression, due to Nuke python functions ignoring it.")
        p.addKnob(k)

        k = nuke.Text_Knob("j_ops_dropdivider_label", "Drag And Drop")
        k.setFlag(nuke.ALWAYS_SAVE)
        p.addKnob(k)

        k = nuke.Boolean_Knob("j_ops_drop_recurse", "Recurse directories")
        k.setFlag(nuke.ALWAYS_SAVE)
        k.setValue(1.0)
        k.setTooltip("Enable/disable recursion into directories dropped on DAG. When enabled will result in entire directory structure being imported into DAG, when disabled only the directory dropped will be imported (ie none of its sub directories)")
        p.addKnob(k)
    
    #Knobs created. Hide obselete ones, update ver
    #2.1
	try:
		p["j_ops_ver"].setValue(2.0201)
		try:
			p["j_ops_enable_bookmark"].setFlag(nuke.INVISIBLE)
		except Exception:
			pass
	except Exception:
		pass
                    
    #Check for preference setting, and if drop enabled add its callback/
    dropEnabled = False
    try:
        dropEnabled = nuke.toNode('preferences')["j_ops_enable_drop"].getValue()
    except (SyntaxError, NameError):
        pass

    if dropEnabled == True:
        nukescripts.drop.addDropDataCallback(jopsDropHandler)

#Adding callbacks to ensure knobs added if needed, and interpreted. 
#Root is done to catch the case where there are no custom prefs,
#so no creation callback for it.
nuke.addOnCreate(preferencesCreatedCallback, nodeClass='Preferences')
nuke.addOnCreate(preferencesCreatedCallback, nodeClass='Root')
