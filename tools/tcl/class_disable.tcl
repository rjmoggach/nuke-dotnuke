proc class_disable {} {

set an [class [selected_nodes]]
  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == $an} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
}
