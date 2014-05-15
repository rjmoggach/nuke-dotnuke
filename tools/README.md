# "Tools" Directory

This is where users (me mostly) should put their helper scripts for non-mission-critical
convenience functions (or ones being tested locally).

TCL is NOT currently working... will get this back in when I decide on best practice
way of doing it.

## Guidelines

There's only one requirement really for these to work and that's an internal attribute **__menus__**
that is part of the mynk tools init and will create menus for the commands.

Here's an example from the shuffleToLayers.py tool:

    __menus__ = {
      'Tools/Layers/Shuffle Layers': {
        'cmd': 'shuffleToLayers(nuke.selectedNodes())',
        'hotkey': '',
        'icon': ''
      }
    }

It's a dict of dicts... key on the top level defines the menu item and hierarchy. The menu scope
is the top of the MyNk menu and toolbar entries. There can be multiple entries here as tools
often have multiple uses. Within those dicts are the command in the local scope (dotted prefix will be added as necessary),
any hotkey you want to assign and an icon. This is all pretty loose right now but it works.

As for the folder hierarchy, it's purely for organization but is replicated in the mynk object.

Eg. the above tool would be accessed at **mynk.tools.python.shuffleToLayers.shuffleToLayers()**
while another deeper example is **mynk.tools.python.nodes.align.alignNodes.alignNodes()**