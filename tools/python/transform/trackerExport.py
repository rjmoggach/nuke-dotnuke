import nuke

__menus__ = {}

def track_to_roto():
  def track_to_roto_in():
    panel=nuke.Panel("roto name")
    panel.addSingleLineInput("name","")
    panel.addBooleanCheckBox('create RotoPaint', False)
    panel.show()
    name = panel.value("name")
    kind = panel.value("create RotoPaint")

    track = nuke.selectedNode()
    if kind == 1:
      roto = nuke.nodes.RotoPaint()
    else:
      roto = nuke.nodes.Roto()
    x = track['xpos'].value()
    y = track['ypos'].value()
    roto.setXYpos(x,y+100)
    #roto['label'].setValue(track['label'].value())
    first = nuke.Root().knob('first_frame').getValue()
    first = int(first)
    last = nuke.Root().knob('last_frame').getValue()
    last = int(last)+1
    frame = first
    Knobs = roto['curves']
    root=Knobs.rootLayer
    transform = root.getTransform()

    
    roto['name'].setValue(name)
    roto.setSelected(True)
    nuke.show(roto)
    track.setSelected(False)
    while frame<last:
      r = track['rotate'].getValueAt(frame,0)
      rr = transform.getRotationAnimCurve(2)
      rr.addKey(frame,r)
      tx = track['translate'].getValueAt(frame,0)
      translx = transform.getTranslationAnimCurve(0)
      translx.addKey(frame,tx)
      ty = track['translate'].getValueAt(frame,1)
      transly = transform.getTranslationAnimCurve(1)
      transly.addKey(frame,ty)
      sx = track['scale'].getValueAt(frame,0)
      ssx = transform.getScaleAnimCurve(0)
      ssx.addKey(frame,sx)
      sy = track['scale'].getValueAt(frame,1)
      ssy = transform.getScaleAnimCurve(1)
      ssy.addKey(frame,sy)
      cx = track['center'].getValueAt(frame,0)
      ccx = transform.getPivotPointAnimCurve(0)
      ccx.addKey(frame,cx)
      cy = track['center'].getValueAt(frame,1)
      ccy = transform.getPivotPointAnimCurve(1)
      ccy.addKey(frame,cy)
      frame = frame+1

  try:
    tracker = nuke.selectedNode()
    if "Tracker"in tracker.Class():
      track_to_roto_in()
    else:
      tra = nuke.selectedNode()
      rot = nuke.createNode("Roto")
      #x = tra['xpos'].value()
      #y = tra['ypos'].value()
      #rot.setXYpos(x,y+50)
  except:
    nuke.createNode("Roto")



