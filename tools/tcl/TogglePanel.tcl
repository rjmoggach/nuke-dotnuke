proc ToggleDefocus {} {

  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "Defocus"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
}

proc ToggleDirBlur {} {

  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "DirBlurWrapper"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
   }
   
proc ToggleDistort {} {

  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "IDistort"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
}

proc ToggleGrain {} {

  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "Grain"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
   #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "Grain2"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
}
   
proc ToggleGridwarp {} {

  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "GridWarp"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
}   

proc ToggleNewBlur {} {

  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "Blur"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
}

proc ToggleVBlur {} {

  #loop through all nodes in the script
  foreach cur_node [nodes] {
    #if you find a node that is a viewer node...
    if {[class $cur_node] == "VectorBlur"} {
      #use the inverse of it's current knob "hide_input" as the new value
      knob $cur_node.disable !$cur_node.disable
      }
    }
}

proc TogglePanel {} {

panel UberToggleTool {{"Vector Blur" vblur b} {"Grain" grain b} {"Defocus" defocus b} {"Distort" distort b} {"Blur" blur b} {"GridWarp" gridwarp b} {"DirBlur" dir_blur b}}

if {$distort == 1} {
  ToggleDistort
  }

if {$vblur == 1} {
  ToggleVBlur
  }
  
if {$blur == 1} {
  ToggleNewBlur
  }
  
if {$grain == 1} {
  ToggleGrain
  }
  
if {$defocus == 1} {
  ToggleDefocus
  }
  
if {$gridwarp == 1} {
  ToggleGridwarp
  }
if {$dir_blur == 1} {
  ToggleDirBlur
  }
}
