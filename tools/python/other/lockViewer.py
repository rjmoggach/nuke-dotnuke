import nuke

__menus__ = {
  'Other/Lock Viewer/1':  { 'cmd': 'LockViewer1()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/2':  { 'cmd': 'LockViewer2()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/3':  { 'cmd': 'LockViewer3()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/4':  { 'cmd': 'LockViewer4{)', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/5':  { 'cmd': 'LockViewer5()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/6':  { 'cmd': 'LockViewer6()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/7':  { 'cmd': 'LockViewer7()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/8':  { 'cmd': 'LockViewer8()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/9':  { 'cmd': 'LockViewer9()', 'hotkey': '', 'icon': ''},
  'Other/Lock Viewer/10':  { 'cmd': 'LockViewer10()', 'hotkey': '', 'icon': ''},
}

# Viewerbuffer are offsetted in Nuke by 1 -> for example: viewer1=0, viewer2=1, viewer3=2
#    line to edit - nuke.activeViewer().node().setInput(0, nuke.toNode(selectednodename)) // setInput(#VIEWERNR, ...

def LockViewer1():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer1():
        nuke.activeViewer().node().setInput(0, nuke.toNode(selectednodename))
    def callbackLockThisViewer1():
        nuke.addKnobChanged(LockThisViewer1,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer1()

def LockViewer2():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer2():
        nuke.activeViewer().node().setInput(1, nuke.toNode(selectednodename))
    def callbackLockThisViewer2():
        nuke.addKnobChanged(LockThisViewer2,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer2()

def LockViewer3():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer3():
        nuke.activeViewer().node().setInput(2, nuke.toNode(selectednodename))
    def callbackLockThisViewer3():
        nuke.addKnobChanged(LockThisViewer3,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer3()

def LockViewer4():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer4():
        nuke.activeViewer().node().setInput(3, nuke.toNode(selectednodename))
    def callbackLockThisViewer4():
        nuke.addKnobChanged(LockThisViewer4,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer4()
        
def LockViewer5():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer5():
        nuke.activeViewer().node().setInput(4, nuke.toNode(selectednodename))
    def callbackLockThisViewer5():
        nuke.addKnobChanged(LockThisViewer5,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer5()
        
def LockViewer6():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer6():
        nuke.activeViewer().node().setInput(5, nuke.toNode(selectednodename))
    def callbackLockThisViewer6():
        nuke.addKnobChanged(LockThisViewer6,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer6()
        
def LockViewer7():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer7():
        nuke.activeViewer().node().setInput(6, nuke.toNode(selectednodename))
    def callbackLockThisViewer7():
        nuke.addKnobChanged(LockThisViewer7,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer7()
        
def LockViewer8():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer8():
        nuke.activeViewer().node().setInput(7, nuke.toNode(selectednodename))
    def callbackLockThisViewer8():
        nuke.addKnobChanged(LockThisViewer8,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer8()
        
def LockViewer9():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer9():
        nuke.activeViewer().node().setInput(8, nuke.toNode(selectednodename))
    def callbackLockThisViewer9():
        nuke.addKnobChanged(LockThisViewer9,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer9()
        
def LockViewer10():
    selectednodename = nuke.selectedNode().name()
    def LockThisViewer10():
        nuke.activeViewer().node().setInput(9, nuke.toNode(selectednodename))
    def callbackLockThisViewer10():
        nuke.addKnobChanged(LockThisViewer10,nodeClass='Viewer')
    if __name__ == '__main__':
        callbackLockThisViewer10()
