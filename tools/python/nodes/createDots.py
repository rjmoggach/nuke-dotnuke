def createDots(nodes):
	'''
	Creates more organized trees using intermediary dots
	'''
	for n in nodes:
		nX = n.xpos()
		nY = n.ypos()
		nW = n.screenWidth()
		nH = n.screenHeight()
		try:
			A = n.input(0)
			AX = A.xpos()
			AY = A.ypos()
			AW = A.screenWidth()
			AH = A.screenHeight()
			B = n.input(1)
			dot = nuke.nodes.Dot()
			if B:
				BX = B.xpos()
				BY = B.ypos()
				BW = B.screenWidth()
				BH = B.screenHeight()
				dot.setInput(0,B)
				n.setInput(1,dot)
				dot.setXYpos(BX+BW/2-6,nY+4)
				if A.Class()== "Dot":
					n.knob("xpos").setValue(AX-nW/2+6)
				else:
					n.knob("xpos").setValue(AX)
			else:
				dot.setInput(0,A)
				n.setInput(0,dot)
				dot.setXYpos(nX+nW/2-6,AY+AH/2-6)
		except:
			pass
