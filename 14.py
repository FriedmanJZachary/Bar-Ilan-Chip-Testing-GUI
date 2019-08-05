from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.event import EventDispatcher
from kivy.graphics import *
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from multiprocessing import Process
from kivy.uix.switch import Switch
from kivy.config import Config
import time
import sys
import os
sys.path.insert(0, '/opt/rh/rh-python36/root/usr/lib/python3.6/site-packages')
import serial

Window.size = (800,600)

def myprint(obj,*args):
    print('BUTTON CLICKED')

class Display(BoxLayout):
        def __init__(self, **kwargs):
                super(Display, self).__init__(**kwargs)

		#Print from data from one screen using another
                def foo2(obj,*args):
                    print('Text of Foo2')
                    print('Here is the thing: ' + str(findByID(s2, 'subID')))
                    print('Here is the other thing: ' + findByID(s2, 'text1').text)

		#Recursive function that searches through all widgets for a given ID
                def findByID(screen, ID):
                    findByID.selectedChild = None
                    def findID(screen, ID):
                        if screen.children:
                            for child in screen.children:
                                #print('Child: ' + str(child))
                                #print('ID: ' + str(child.id))
                                if str(child.id) == ID:
                                    #print('Gotchya')
                                    findByID.selectedChild = child
                                    #print('Selected Child: ' + str(findByID.selectedChild))
                                    return 1
                                else:
                                    findID(child, ID)
                    findID(screen, ID)
                    print('Selected Child: ' + str(findByID.selectedChild))
                    return findByID.selectedChild

                #Screens are their own classes, formed within the initialization of the display itself
                
                class Screen_One(Screen):
                    def __init__(self, **kwargs):
                        super(Screen_One, self).__init__(**kwargs)
                        self.name = 'One'
                        
                        #Different colors convey different chip statuses
                        rimg = Image(source='red.png')
                        gimg = Image(source='green.png')
                        yimg = Image(source='yellow.png')
                        bimg = Image(source='gray.png')
                        curimg = bimg
                        
                        killedAlready = True
                        #Checks the state of .txt file
                        def docheck(obj,*args):
                            checkval = 10
                            if abs(myChip.count) < checkval or keep.active == True:
                                #print('Check Confirmed')
                                nonlocal curimg
                                curimg = myChip.check(rimg, gimg, yimg, bimg)
                                Fimg.clear_widgets()
                                Fimg.add_widget(begEcho)
                                Fimg.add_widget(curimg)
                                #print('Count = ' + str(myChip.count))
                            else:
                                if myChip.testtime:
                                    os.system('./killall_measurements')
                                    myChip.testtime = False

                        def setVoltage(obj):
                            if findByID(s1, '6state1').active:
                                mySupply.setSequence('P6V',findByID(s1, '6sup1').text,mySupply.curmax)
                                time.sleep(0.2)
                            if findByID(s1, '25state1').active:
                                mySupply.setSequence('P25V',findByID(s1, '25sup1').text,mySupply.curmax)


                        #Boxes that contain voltage supply-setting elements
                        class Vbox(BoxLayout):

                            def __init__(self, **kwargs):
                                # make sure we aren't overriding any important functionality
                                super(Vbox, self).__init__(**kwargs)

                                with self.canvas.before:
                                    Color(0, .2, .3, 1)  # green; colors range from 0-1 instead of 0-255
                                    self.rect = Rectangle(size=self.size, pos=self.pos)
            
                                    self.bind(size=self._update_rect, pos=self._update_rect)

                            def _update_rect(self, instance, value):
                                self.rect.pos = instance.pos
                                self.rect.size = instance.size


                        Fouter = BoxLayout(orientation='horizontal',padding = [0,0,0,0])
                        Finner = BoxLayout(orientation='vertical',padding = [50,50,50,50], spacing=60)
                        Finner2 = BoxLayout(orientation='vertical',padding = [30,30,30,30], spacing=20)
                        Finner3 = BoxLayout(orientation='vertical',padding = [30,30,30,30], spacing=20)
                        Fvwrite = BoxLayout(orientation='horizontal',padding = [0,0,0,0],spacing=0,size_hint_y=None,height=45)

#FINNER2
                        #Power supply control sections
                        vlay = Vbox(orientation='vertical',padding = [10,10,10,10], spacing=10)
                        vlay2 = Vbox(orientation='vertical',padding = [10,10,10,10], spacing=10)


                        #Blit voltage-controlling elements onto the screen
                        def blitVolt(vallist):
                            Finner2.remove_widget(Finner3)
                            Finner3.clear_widgets()
                            vlay.clear_widgets()
                            vlay2.clear_widgets()

                            mySupply.row1 = []
                            mySupply.row2 = []
                            mySupply.rows = [mySupply.row1, mySupply.row2]
                
                            if os.path.exists('voltagelog.txt'):
                                file1 = open('voltagelog.txt','r') 
                                i = 0
                                for value in mySupply.values:
                                    mySupply.values[i] = file1.readline().rstrip()
                                    print('Value: ' + value)
                                    print(mySupply.values)
                                    i += 1

                            mySupply.addrow('+6',0,'6sup1','6state1',mySupply.values[0])
                            mySupply.addrow('+25',0,'25sup1','25state1',mySupply.values[1])
                            mySupply.addrow('-25',0,'-25sup1','-25state1',mySupply.values[2])
                            print(mySupply.values)
                            mySupply.addrow('+6',1,'6sup2','6state2',mySupply.values[3])
                            mySupply.addrow('+25',1,'25sup2','25state2',mySupply.values[4])
                            mySupply.addrow('-25',1,'-25sup2','-25state2',mySupply.values[5])


                            vlay.add_widget(Label(text='Supply 1'))
                            for row in mySupply.rows[0]:
                                print('blitting row: ' + str(row))
                                vlay.add_widget(row)
                                
                            vlay2.add_widget(Label(text='Supply 2'))
                            for row in mySupply.rows[1]:
                                print('blitting row: ' + str(row))
                                vlay2.add_widget(row)

                            #Joining all sections
                            Finner3.add_widget(vlay)
                            Finner3.add_widget(vlay2)
                            Finner2.add_widget(Finner3, index=2)
 
                        #Button to set power supply settings
                        initiate = Button(size_hint_y=None,height=45,text='Set Voltages', id = 'initiate')
                        initiate.bind(on_press=setVoltage)

                        #Buttons to write and read voltage values from .txt file
                        write = Button(size_hint_y=None,height=45,text='Save')
                        read = Button(size_hint_y=None,height=45,text='Read')
                        Fvwrite.add_widget(write)
                        write.bind(on_press=mySupply.save)
                        Fvwrite.add_widget(read)
                        read.bind(on_press=blitVolt)

                        Finner2.add_widget(Finner3)
                        Finner2.add_widget(initiate)  
                        Finner2.add_widget(Fvwrite)
                        

                        #Run manually the first time; runs again each time the read button is pushed
                        blitVolt(mySupply.values)



#FINNER1


                        #Buttons to run and kill testing script
                        begEcho = Button(height=100,text='Connect to Chip', id = 'echo')
                        kill = Button(height=100,text='Kill All', id = 'kill',background_color=(1,0,0,1))
                        begEcho.bind(on_press=myChip.keepEcho)
                        kill.bind(on_press=myChip.killer)
                        choose = Button(height=10, text='Choose Chip', id = 'choose')
                        
                        #Run check every 1/2 sec
                        Clock.schedule_interval(docheck, 0.5)
                        
                        #Checkbox Section 1
                        Fbox = BoxLayout(orientation='horizontal',padding = [0,0,0,0])
                        ck = Label(text='Bist (Not Direct)')
                        bist = Switch(active=True)
                        Fbox.add_widget(ck)
                        Fbox.add_widget(bist)
                        Finner.add_widget(Fbox)
                        
                        #Image Section
                        Fimg = BoxLayout(orientation='horizontal',padding = [0,0,0,0], spacing=0)
                        Fimg.add_widget(begEcho)
                        Fimg.add_widget(curimg)
                        Finner.add_widget(Fimg)

                        #Checkbox Section 2
                        Fkeep = BoxLayout(orientation='horizontal',padding = [0,0,0,0], spacing=0)
                        clab = Label(text='Continue echo')
                        keep = Switch(active=False)
                        Fkeep.add_widget(clab)
                        Fkeep.add_widget(keep)
                        Finner.add_widget(Fkeep)
                  
                        Finner.add_widget(kill)
                        Finner.add_widget(choose)
                        Fouter.add_widget(Finner)
                        Fouter.add_widget(Finner2)
                        self.add_widget(Fouter)

                class Screen_Two(Screen):
                        def __init__(self, **kwargs):
                                super(Screen_Two, self).__init__(**kwargs)
                                self.name = 'Two'
                                
				#Nested grids allow for better arrangement of widgets
                                outer = GridLayout(cols=1, pos=(00, 00),size=(Display.width, Display.height))
                                inner = GridLayout(cols=4, rows=2, padding=100, pos=(00, 00),size=(Display.width, Display.height))
                                
				#Add text boxes, check boxes, and corresponding labels
                                ckL1 = Label(text='Check1: ',halign='right', valign='center')
                                ckL2 = Label(text='Check2: ',halign='right', valign='center')
                                txtL1 = Label(text='Text1: ',halign='right', valign='center')
                                txtL2 = Label(text='Text2: ',halign='right', valign='center')
                                ck1 = CheckBox()
                                ck2 = CheckBox()
                                txt1 =  TextInput(id='text1')
                                txt2 = TextInput()
                                
                                widList = [ckL1, ck1, txtL1, txt1, ckL2, ck2, txtL2, txt2]
                                for wid in widList:
                                    inner.add_widget(wid)
                                outer.add_widget(inner)
                                
                                submit = AnchorLayout(anchor_y='bottom',padding = [100,100,100,100])
                                btnS = Button(height=10, text='Submit', id = 'subID')
                                submit.add_widget(btnS)
                                outer.add_widget(submit)
                                self.add_widget(outer)

                                def runtest(obj,*args):
                                        print('From Screen {}:'.format(self.name))
                                        inputs = self.children[0].children[1].children
                                        text_inputs = [inp for inp in inputs if isinstance(inp, TextInput)]
                                        for ti in text_inputs:
                                                print(ti.text)
                                        print('test: ' + self.children[0].children[1].children[4].text)
                                 
                                btnS.bind(on_press=runtest)


                class Screen_Three(Screen):
                    def __init__(self, **kwargs):
                        
                        super(Screen_Three, self).__init__(**kwargs)
                        self.name = 'Three'
                        btnC = Button(text='Text')
                        btnC.bind(on_press = foo2)
                        self.add_widget(btnC)
                            
                class Screen_Four(Screen):
                    def __init__(self, **kwargs):
                        super(Screen_Four, self).__init__(**kwargs)
                        self.name = 'Four'

                        class Vbox(BoxLayout):

                            def __init__(self, **kwargs):
                                # make sure we aren't overriding any important functionality
                                super(Vbox, self).__init__(**kwargs)

                                with self.canvas.before:
                                    Color(.5, .5, .6, 1)  # green; colors range from 0-1 instead of 0-255
                                    self.rect = Rectangle(size=self.size, pos=self.pos)
                                    
                                self.bind(size=self._update_rect, pos=self._update_rect)

                            def _update_rect(self, instance, value):
                                self.rect.pos = instance.pos
                                self.rect.size = instance.size

                        vlay = Vbox(orientation='horizontal',padding = [10,10,10,10], spacing=10)
                        vlay2 = Vbox(orientation='horizontal',padding = [10,10,10,10], spacing=10)
                        outer = BoxLayout(orientation='vertical',padding = [10,10,10,10], spacing=10)
                        
                        l1 = Label(text='label 1')
                        l2 = Label(text='label 2')
                        vlay.add_widget(l1)
                        vlay2.add_widget(l2)

              
                        outer.add_widget(vlay)
                        outer.add_widget(vlay2)
                        self.add_widget(outer)


                class Screen_Five(Screen):
                    def __init__(self, **kwargs):
                        
                        super(Screen_Five, self).__init__(**kwargs)
                        self.name = 'Five'
                        
                        #Set current and device variables for the Screen 1 tests; still needs work
                        def setVals(obj):
                            mySupply.deviceName = findByID(s5,'dev').text
                            mySupply.curmax = findByID(s5,'max').text 

                        outer = BoxLayout(orientation='horizontal', padding = [50,50,50,50])
                        inner = BoxLayout(orientation='vertical')
                        empty = Image(source='blank.png')

                        advrows = []
                        def addrow(lab,txt,myID):
                            lab = Label(text=lab)
                            valLay  = AnchorLayout(anchor_x='right', anchor_y='center')
                            val = TextInput(size_hint=(1, None),height=31,multiline=False,text=txt,id=myID)
                            valLay.add_widget(val)

                            advrows.append(BoxLayout())
                            advrows[-1].add_widget(lab)
                            advrows[-1].add_widget(valLay)

                        addrow('Supply 1 Location',mySupply.deviceName,'dev')
                        addrow('Maximum Current',mySupply.curmax,'max')
                        for row in advrows:
                            inner.add_widget(row)
                
                        submit = Button(text='Submit',size_hint_y=None,height=50)
                        submit.bind(on_press=setVals)
                        inner.add_widget(submit)

                        outer.add_widget(inner)
                        outer.add_widget(empty)
                        self.add_widget(outer)

                #Begin adding elements to main display: includes screens and navigation buttons
                layout = BoxLayout(orientation='vertical')
                self.add_widget(layout)
                
                btnBar = BoxLayout(orientation='horizontal', size_hint=(1, None),height='48dp')
                
                with self.canvas.before:
                    Color(0, 0.05, 0.15)
                    Rectangle(pos=(0, 0), size=(2000, 2000))
                
                #create screens (as instances of the above classes) and buttons to navigate between them
                s1 = Screen_One()
                s2 = Screen_Two()
                s3 = Screen_Three()
                s4 = Screen_Four()
                s5 = Screen_Five()

                btn1 = Button(text='GENERAL', on_press=lambda a: sm.switch_to(s1))
                btn2 = Button(text='BIST', on_press=lambda a: sm.switch_to(s2))
                btn3 = Button(text='DIRECT', on_press=lambda a: sm.switch_to(s3))
                btn4 = Button(text='DEMO', on_press=lambda a: sm.switch_to(s4))
                btn5 = Button(text='ADVANCED', on_press=lambda a: sm.switch_to(s5))
               
                buttonlist = [btn1, btn2, btn3, btn4, btn5]
                screenlist = [s1, s2, s3, s4, s5]
                sm = ScreenManager()
                for i in range(0, 5):
                        btnBar.add_widget(buttonlist[i])
                        sm.add_widget(screenlist[i])
                layout.add_widget(btnBar)
                layout.add_widget(sm)

#Contains variables and functions for testing whether the chip is on and functional 
class chipOn:
    def __init__(self):
        self.testtime = False
        self.count = 0

    #Begin testing if not already doing so
    def keepEcho(self,obj,*arg):
        if self.testtime:
            print('Why are you pressing me?')
        else:
            p = Process(target=self.test)
            p.start()
            self.testtime = True
            print('Test Time = ' + str(self.testtime))

    #Run BASH script to see if chip is working
    def test(obj,*args):
        os.system('./run_test scripts/echo_loop.pl > dump.txt')

    #Kill testing process initiated by test()
    def killer(self,obj,*args):
        self.count = 0
        self.testtime = False
        print('Test Time = ' + str(self.testtime))
        os.system('./killall_measurements')
        os.system('rm dump.txt')
        f=open('dump.txt', 'w+')
        f.close()

    #Check text file for condition; will be used to evaluate chip state
    def check(self,rimg,gimg,yimg,bimg):
        try:
            fileHandle = open('dump.txt','r')
            lineList = fileHandle.readlines()
            fileHandle.close()
            last = lineList[len(lineList)-3]
            print('2nd-to-last Line: ' + last)
            if 'OK' in last:
                print('Green')
                myChip.count=0 if myChip.count<0 else myChip.count+1
                return gimg
            elif 'Fail' in last:
                print('Red')
                myChip.count=0 if myChip.count>0 else myChip.count-1
                return rimg
            else:
                print('Yellow')
                return yimg
        except:
            #print('ERROR gray')
            return bimg

#Contains variables and functions for controlling the voltage supply
class vSet():
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(vSet, self).__init__(**kwargs)
        self.curmax = '0.2'
        self.row1 = []
        self.row2 = []
        self.rows = [self.row1, self.row2]
        #Voltage supply configuration
        self.deviceName = '/dev/ttyUSB0'
        #Create list of all voltage values to be looped through in setting and reading them
        self.s6v1 = '0.9'
        self.s25v1 = '0.8'
        self.sn25v1 = '0.9'
        self.s6v2 = '0.9'
        self.s25v2 = '0.8'
        self.sn25v2 = '0.9'
        self.values=[self.s6v1,self.s25v1,self.sn25v1,self.s6v2,self.s25v2,self.sn25v2]

    def addrow(self,rail,supply,myID,stateID,value,**kwargs):
        rail = Label(text=rail)
        valLay  = AnchorLayout(anchor_x='right', anchor_y='center')
        val = TextInput(size_hint=(1, None),height=31,multiline=False,text=value,id=myID)
        state = CheckBox(active=True,id=stateID)
        textopt = TextInput(size_hint=(1, None),height=31,multiline=False)

        self.rows[supply].append(BoxLayout())
        self.rows[supply][-1].add_widget(rail)
        self.rows[supply][-1].add_widget(val)
        self.rows[supply][-1].add_widget(textopt)
        self.rows[supply][-1].add_widget(state)

        print('Supply: ' + str(supply))
    
    #Save the current voltage values by finding anchor layouts and reading from their children (the text inputs)
    def save(self,obj):
        try:
            os.remove('voltagelog.txt')
        except:
            pass
        file1 = open('voltagelog.txt','a+')
        for row in self.rows:
            for child in row:
                inputs = child.children
                #print(str(inputs))
                anchor_inputs = [inp for inp in inputs if isinstance(inp, AnchorLayout)]
                for ai in anchor_inputs:
                    #print(str(ai))
                    text_inputs = ai.children
                    for ti in text_inputs:
                        print(ti.text)
                        file1.write(ti.text + '\n')

    #Writes a command directy to the supply
    def wcom(self,cmd):
        cmd += '\n'
        ser.write(cmd.encode(encoding='ascii',errors='strict'))

    #Sequentially shuts supply, sets voltage and current values, and turns the supply back on
    def setSequence(self,rail,volt,curr):
        self.wcom('SYSTEM:REMOTE')
        self.wcom('OUTPUT:STATE ' + ('OFF'))
        #time.sleep(0.1)
        self.wcom('APPL %s, %s, %s' % (rail,volt,curr))
        self.wcom('OUTPUT:STATE ' + ('ON'))

#Objects of the above classes through which the functions and variables in them are used
myChip = chipOn()
mySupply = vSet()

#Serial connection to voltage supply
ser = serial.Serial(
    port=mySupply.deviceName,
    timeout=2,
    parity=serial.PARITY_NONE,
    stopbits=2,
    dsrdtr=1
)

class BEER(App):
    num1 = 40
    def build(self):
        self.icon = 'sample.png'
        return Display()

if __name__ == '__main__':
    myapp = BEER()
    myapp.run()     
    #Anything below this point will run only after the window is closed
    print('Application Terminated')        
    os.system('./killall_measurements')
    os.system('rm dump.txt')
    f=open('dump.txt', 'w+')
    f.close()
