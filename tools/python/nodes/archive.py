import os
import shutil
import threading
import time

import nuke
import nukescripts


class archiveInterface():
        def interface(self):
                self.panel = nukescripts.PythonPanel('Archive script')
                self.file = nuke.File_Knob('Output','Output folder:')
                self.panel.addKnob(self.file)
                self.scriptName = nuke.String_Knob('name','Script name:','script.nk')
                self.panel.addKnob(self.scriptName)
                self.log = nuke.Boolean_Knob('log','Generate log:',True)
                self.panel.addKnob(self.log)
                self.comment = nuke.Multiline_Eval_String_Knob('comment','Comments:')
                self.panel.addKnob(self.comment)
                result = self.panel.showModalDialog()
                self.scriptInfo = nukescripts.get_script_data()
                if result:
                        self.action()
        
        def action(self):
                readList =      []
                writeList=      []
                fbxList=        []
                nuke.scriptSaveAs(self.file.value() + self.scriptName.value())
                readToCopy=     []
                writeToCopy=  []
                self.scriptRoot = '''[file dirname [knob root.name]]'''
                DESTINATION = self.file.value()
                LAYERS =        DESTINATION + 'LAYERS/'
                FBX =           DESTINATION + 'FBX/'
                WRITE =         DESTINATION + 'WRITE/'  
                # Read  
                for n in nuke.allNodes('Read'):
                        if n.knob('file').value() not in readList:
                                readList.append(n.knob('file').value())
                for p in readList:
                    if os.path.exists(os.path.dirname(p)):
                        for f in os.listdir(os.path.dirname(p)):
                            if os.path.splitext(f)[-1] == os.path.splitext(p)[-1]:
                                if len(f.split('.')[0]) == len(os.path.basename(p).split('.')[0]):
                                    path = '/'.join([os.path.dirname(p),os.path.basename(f)])
                                    if os.path.isfile(path):
                                        readToCopy.append(path)
                #FBX
                for n in nuke.allNodes():
                        if n.Class() in ['ReadGeo2','Camera2','Axis2','WriteGeo']:
                                if n.knob('read_from_file').value():
                                        if n.knob('file').value() not in fbxList:
                                                fbxList.append(n.knob('file').value())
                #Write
                for n in nuke.allNodes('Write'):
                        if n.knob('file').value() not in writeList:
                                if n.knob('file').value() != '':
                                        if os.path.isdir( os.path.dirname( n.knob('file').value() ) ):
                                                writeList.append(n.knob('file').value())
                
                for p in writeList:
                    if os.path.exists(os.path.dirname(p)):
                        for f in os.listdir(os.path.dirname(p)):
                            if os.path.splitext(f)[-1] == os.path.splitext(p)[-1]:
                                if f.split('.')[0] == os.path.basename(p).split('.')[0]:
                                    path = '/'.join([os.path.dirname(p),os.path.basename(f)])
                                    if os.path.isfile(path):
                                        writeToCopy.append(path)
                self.copyDic = {}
                for p in readToCopy:
                        folder = os.path.dirname(p).split('/')[-1] + '/'
                        if os.path.exists(LAYERS + folder) == False:
                                os.makedirs(LAYERS + folder)
                        self.copyDic[p] = [LAYERS + folder + os.path.basename(p),os.path.getsize(p)]
                for p in fbxList:
                        if os.path.exists(FBX) == False:
                                os.makedirs(FBX)
                        #shutil.copy( p , FBX  + os.path.basename(p) )  
                        self.copyDic[p] = [FBX  + os.path.basename(p),os.path.getsize(p)]
                for p in writeToCopy:
                        folder = os.path.dirname(p).split('/')[-1] + '/'
                        if os.path.exists(WRITE + folder) == False:
                                os.makedirs(WRITE + folder)
                        #shutil.copy( p , WRITE + folder + os.path.basename(p) )
                        self.copyDic[p] = [WRITE + folder + os.path.basename(p),os.path.getsize(p)]
                threading.Thread( None, self.action2 ).start()
        
        def action2(self):
                task = nuke.ProgressTask("Copying")
                task.setMessage('fsdf')
                lenght = len(self.copyDic)
                x = 0.0
                totalSize = 0.0
                for k,v in self.copyDic.iteritems():
                        totalSize+= v[1]
                totalSize = round((totalSize/1000000000),2)
                toGoSize = 0.0
                myList = []
                for i in self.copyDic:
                        myList.append(i)
                myList.sort()
                for i in myList:
                        p = int((x/lenght)*100)
                        task.setProgress(p)
                        toGoSize = toGoSize + self.copyDic[i][1]
                        progressStr = '   (%s/%s)' % (int(x),lenght)
                        size = '  '+str(round((toGoSize/1000000000),2))+' / ' +str(totalSize) +' GB'
                        task.setMessage(os.path.basename(i) + progressStr +size)
                        shutil.copy( i,self.copyDic[i][0])
                        x+=1
                        if task.isCancelled(): 
                                nuke.executeInMainThread( nuke.message, args=( "Canceled" ) )
                                break
                self.replacePath()

        def replacePath(self):
                for n in nuke.allNodes():
                        if n.Class() in ['ReadGeo2','Camera2','Axis2','WriteGeo']:
                            a = n.knob('file').value()
                            a = a.replace( os.path.dirname(a) , self.scriptRoot+'/FBX')
                            n.knob('file').setValue(a)
                for n in nuke.allNodes('Read'):
                        a = n.knob('file').value()
                        a = a.replace( '/'.join(os.path.dirname(a).split('/')[0:-1]) , self.scriptRoot+'/LAYERS')
                        n.knob('file').setValue(a)
                for n in nuke.allNodes('Write'):
                        a = n.knob('file').value()
                        a = a.replace( '/'.join(os.path.dirname(a).split('/')[0:-1]) , self.scriptRoot+'/WRITE')
                        n.knob('file').setValue(a)
                nuke.scriptSave("")
                if self.log.value():
                    self.generateLog()
            
        def generateLog(self):
            if self.comment.value() != '':
                note  = 'Notes\n\n' + self.comment.value() + '\n\n===================\n\n'
            else:
                note = self.comment.value()
            nodeInfo = ''
            a = {}
            b = []
            c = []
            for n in nuke.allNodes():
                a[n.Class()] = 0
            for n in nuke.allNodes():
                c.append(n.Class())
            for i in a:
                b.append(i)
            b.sort()
            for i in c:
                a[i] +=1
            for i in b:
                nodeInfo = nodeInfo + '('+str(a[i])+')'  + ' ' + i +'\n'
            stats = nukescripts.get_script_data()
            logFile = open(self.file.value()+ 'log.txt','w')
            logFile.write(note+nodeInfo+'\n\n\n\n'+stats)
            logFile.close()


ai = archiveInterface()


