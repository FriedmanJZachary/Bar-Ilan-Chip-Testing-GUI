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
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import *
from kivy.uix.anchorlayout import AnchorLayout
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
from multiprocessing import Process
from kivy.uix.switch import Switch
import time
import sys
import os

Config.set('kivy','window_icon','sample.png')
Window.size = (800,600)

def myprint(obj,*args):
    print('BUTTON CLICKED')

class Display(BoxLayout):
        def __init__(self, **kwargs):
                super(Display, self).__init__(**kwargs)
                
                #Set initial frequency value
                fval = "?"

                #Print from data from one screen using another
                def foo2(obj,*args):
                    print('Text of Foo2')
                    print("Here's the thing: " + str(findByID(s2, 'subID')))
                    print("Here's the other thing: " + findByID(s2, 'text1').text)

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

                        #Mixed Button
                        def mixed(*args):
                            print('Mixed Mode Button Pushed')
                            p = Process(target=mixedprocess)
                            p.start()
                            nonlocal fval
                            fval = "95"
                            disp()

                        def mixedprocess(*args):
                             os.system('./run_test scripts/echo_loop.pl')

                        #Static Button
                        def static(*args):
                            p2 = Process(target=staticprocess)
                            p2.start()
                            print('Static Mode Button Pushed')
                            nonlocal fval
                            fval = "40"
                            disp()

                        
                        def staticprocess(*args):
                             os.system('./run_test scripts/echo_loop.pl')


                        #Formatting
                        inner = GridLayout(cols=2, rows=2, padding=10, pos=(00, 00),size=(Display.width, Display.height),spacing=50)
                        outer = GridLayout(cols=1, rows=2, padding=100, pos=(00, 00),size=(Display.width, Display.height),spacing=50)



                        #Widgets to be displayed
                        mix = Button(height=100,text="DML Mixed")
                        mix.bind(on_press=mixed)

                        sta = Button(height=100,text="DML Static")
                        sta.bind(on_press=static)
                        
                        inner.add_widget(mix)
                        inner.add_widget(sta)
                

                        def disp(*args):
                            outer.clear_widgets()
                            self.clear_widgets()
                            lab = Label(text="Frequency: " + fval + " HZ",font_size='20sp')
                            outer.add_widget(inner)
                            outer.add_widget(lab)
                            self.add_widget(outer)
                        
                        disp()
                        Clock.schedule_interval(disp, 0.5)
                        
                
                class Screen_Two(Screen):
                    def __init__(self, **kwargs):
                        super(Screen_Two, self).__init__(**kwargs)
                        self.name = "Two"
                        
                        #KILL Button
                        def killer(*args):
                            os.system('./killall_measurements')
                            print('KILL ALL Button Pushed')
                            nonlocal fval
                            fval = '?'
                        
                        outer2 = GridLayout(cols=1, rows=2, padding=200, pos=(00, 00),size=(Display.width, Display.height),spacing=50)
                        
                        kill = Button(text="Kill All",font_size='20sp',background_color=(1,0,0,1))
                        kill.bind(on_press=killer)
                        outer2.add_widget(kill)
                        self.add_widget(outer2)


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
    
                btn1 = Button(text='Tab 1', on_press=lambda a: sm.switch_to(s1))
                btn2 = Button(text='Tab 2', on_press=lambda a: sm.switch_to(s2))

                buttonlist = [btn1, btn2]
                screenlist = [s1, s2]
                sm = ScreenManager()
                for i in range(0, 2):
                        btnBar.add_widget(buttonlist[i])
                        sm.add_widget(screenlist[i])
                layout.add_widget(btnBar)
                layout.add_widget(sm)

class Demo1App(App):
    num1 = 40
    def build(self):
        return Display()

if __name__ == '__main__':
    myapp = Demo1App()
    myapp.run()     
    #Anything below this point will run only after the window is closed
    print('Application Terminated')        

