proc set_label {} {
  knob [selected_node].label [get_input "Enter label text" [knob [selected_node].label]]
}
