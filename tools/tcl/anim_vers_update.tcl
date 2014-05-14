proc anim_vers_update {} {

set name [join [lrange [split [file tail [file root [file root [value [selected_node].file]]]] _ ] 3 end] _]
  foreach mynode [nodes] {
    if {[class $mynode] == "Write"} {
      if {[exists $mynode.Descriptor]} {
        if {[llength [split [value $mynode.Descriptor] _ ]] > 1} {
          knob $mynode.Descriptor [join [lreplace [split [value $mynode.Descriptor] _ ] 1 end $name]  _ ]
        } else {
          knob $mynode.Descriptor [join [lreplace [split [value $mynode.Descriptor] _ ] 0 end $name]  _ ]
        }
      }   
    }
  }  
}