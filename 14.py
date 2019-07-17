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
from kivy.uix.checkbox import CheckBox
from kivy.graphics import *
from kivy.uix.anchorlayout import AnchorLayout
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.clock import Clock
from multiprocessing import Process
import sys
import os

Config.set('kivy','window_icon','sample.png')

def myprint(obj,*args):
    print('BUTTON CLICKED')

class Display(BoxLayout):
        def __init__(self, **kwargs):
                super(Display, self).__init__(**kwargs)

		#Print from data from one screen using another
                def foo2(obj,*args):
                    print('Text of Foo2')
                    print("Here's the thing: " + str(findByID(s1, 'subID')))
                    print("Here's the other thing: " + findByID(s1, 'text1').text)

		#Check text file for condition; will be used to evaluate chip state
                def check():
                    try:
                        fileHandle = open('dump.txt',"r")
                        lineList = fileHandle.readlines()
                        fileHandle.close()
                        last = lineList[len(lineList)-3]
                        print('2nd-to-last Line: ' + last)
                        if "OK" in last:
                            print('Green')
                            return 0
                        elif "Fail" in last:
                            print('Red')
                            return 1
                        else:
                            print('Yellow')
                            return 2
                    except:
                        print('ERROR gray')
                        return 3

		#Recursive function that searches through all widgets for a given ID
                def findByID(screen, ID):
                    findByID.selectedChild = None
                    def findID(screen, ID):
                        if screen.children:
                            for child in screen.children:
                                print('Child: ' + str(child))
                                print('ID: ' + str(child.id))
                                if str(child.id) == ID:
                                    print('Gotchya')
                                    findByID.selectedChild = child
                                    print('Selected Child: ' + str(findByID.selectedChild))
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
                                self.name = "One"
                                
				#Nested grids allow for better arrangement of widgets
                                outer = GridLayout(cols=1, pos=(00, 00),size=(Display.width, Display.height))
                                inner = GridLayout(cols=4, rows=2, padding=100, pos=(00, 00),size=(Display.width, Display.height))
                                
				#Add text boxes, check boxes, and corresponding labels
                                ckL1 = Label(text="Check1: ",halign='right', valign='center')
                                ckL2 = Label(text="Check2: ",halign='right', valign='center')
                                txtL1 = Label(text="Text1: ",halign='right', valign='center')
                                txtL2 = Label(text="Text2: ",halign='right', valign='center')
                                ck1 = CheckBox()
                                ck2 = CheckBox()
                                txt1 =  TextInput(id='text1')
                                txt2 = TextInput()
                                
                                widList = [ckL1, ck1, txtL1, txt1, ckL2, ck2, txtL2, txt2]
                                for wid in widList:
                                        inner.add_widget(wid)
                                outer.add_widget(inner)
                                
                                submit = AnchorLayout(anchor_y='bottom',padding = [100,100,100,100])
                                btnS = Button(height=10, text="Submit", id = 'subID')
                                submit.add_widget(btnS)
                                outer.add_widget(submit)

                                self.add_widget(outer)

                                def runtest(obj,*args):
                                        print("From Screen {}:".format(self.name))
                                        inputs = self.children[0].children[1].children
                                        text_inputs = [inp for inp in inputs if isinstance(inp, TextInput)]
                                        for ti in text_inputs:
                                                print(ti.text)
                                        print('test: ' + self.children[0].children[1].children[4].text)
                                 
                                btnS.bind(on_press=runtest)

                class Screen_Two(Screen):
                    def __init__(self, **kwargs):
                        super(Screen_Two, self).__init__(**kwargs)
                        self.name = "Two"

                class Screen_Three(Screen):
                    def __init__(self, **kwargs):
                        
                        super(Screen_Three, self).__init__(**kwargs)
                        self.name = "Three"
                        btnC = Button(text='Text')
                        btnC.bind(on_press = foo2)
                        self.add_widget(btnC)

                class Screen_Four(Screen):
                    def __init__(self, **kwargs):
                        super(Screen_Four, self).__init__(**kwargs)
                        self.name = "Four"

			#Checks the state of .txt file
                        def docheck(obj,*args):
                            print('Check Confirmed')
                            val = check()
                            Fouter.clear_widgets()
                            if val==0:
                                print('Check Positive')
                                curimg = gimg                                   
                            elif val==1:
                                curimg = rimg                                 
                            elif val==2:
                                curimg = yimg
                            else:
                                curimg = bimg

                            Fouter.add_widget(Finner)
                            Fouter.add_widget(curimg)
                            
                        Fouter = BoxLayout(orientation='horizontal',padding = [100,100,100,100])
                        Finner = BoxLayout(orientation='vertical',padding = [50,50,50,50], spacing=50)

                        rimg = Image(source='red.png')
                        gimg = Image(source='green.png')
                        yimg = Image(source='yellow.png')
                        bimg = Image(source='gray.png')
                        
                        curimg = yimg
                        begEcho = Button(height=100,text="Begin Echo", id = 'echo')
                        kill = Button(height=100,text="Kill All", id = 'kill',background_color=(1,0,0,1))
                        begEcho.bind(on_press=myChip.keepEcho)
                        kill.bind(on_press=myChip.killer)
                        
                    
                        Clock.schedule_interval(docheck, 0.5)
                        Finner.add_widget(begEcho)
                        Finner.add_widget(kill)
                        Fouter.add_widget(Finner)
                        Fouter.add_widget(curimg)
                        self.add_widget(Fouter)
                
                #Begin adding elements to main display: includes screens and navigation buttons
                layout = BoxLayout(orientation='vertical')
                self.add_widget(layout)
                
                btnBar = BoxLayout(orientation='horizontal', size_hint=(1, None),height='48dp')
                
                with self.canvas.before:
                    Color(0, 0, 0.15)
                    Rectangle(pos=(0, 0), size=(2000, 2000))
                
                s1 = Screen_One()
                s2 = Screen_Two()
                s3 = Screen_Three()
                s4 = Screen_Four()
                
                btn1 = Button(text='1', on_press=lambda a: sm.switch_to(s1))
                btn2 = Button(text='2', on_press=lambda a: sm.switch_to(s2))
                btn3 = Button(text='3', on_press=lambda a: sm.switch_to(s3))
                btn4 = Button(text='4', on_press=lambda a: sm.switch_to(s4))
               
                buttonlist = [btn1, btn2, btn3, btn4]
                screenlist = [s1, s2, s3, s4]
                sm = ScreenManager()
                for i in range(0, 4):
                        btnBar.add_widget(buttonlist[i])
                        sm.add_widget(screenlist[i])
                layout.add_widget(btnBar)
                layout.add_widget(sm)

#Contains variables and functions for testing whether the chip is on and functional 
class chipOn:
    def __init__(self):
        self.testtime = False

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
        self.testtime = False
        print('Test Time = ' + str(self.testtime))
        os.system('./killall_measurements')
        os.system('rm dump.txt')
        f=open("dump.txt", "w+")
        f.close()

myChip = chipOn()

class Demo1App(App):
    num1 = 40
    def build(self):
        return Display()

if __name__ == '__main__':
    myapp = Demo1App()
    myapp.run()     
    #Anything below this point will run only after the window is closed
    print('Application Terminated')        
    os.system('./killall_measurements')
    os.system('rm dump.txt')
    f=open("dump.txt", "w+")
    f.close()
