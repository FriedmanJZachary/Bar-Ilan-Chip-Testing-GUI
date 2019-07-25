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
                
                #Set initial values
                DMfval = "?"
                DMval2 = "?"
                DMval3 = "?"
                
                CMfval = "?"
                CMval2 = "?"
                CMval3 = "?"

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
                            os.system('')
                            print('Mixed Mode Button Pushed')
                            nonlocal DMfval
                            DMfval = "21"
                            nonlocal DMval2
                            DMval2 = "22"
                            nonlocal DMval3
                            DMval3 = "23"
                            
                            nonlocal CMfval
                            CMfval = "24"
                            nonlocal CMval2
                            CMval2 = "25"
                            nonlocal CMval3
                            CMval3 = "26"
                            
                            Clock.schedule_once(mixeddelay, 5)
                            disp()
                        
                        #Mixed Button
                        def mixeddelay(*args):
                            os.system('')
                            print('Mixed Mode Delay Done')
                            nonlocal DMfval
                            DMfval = "44"
                            nonlocal DMval2
                            DMval2 = "45"
                            nonlocal DMval3
                            DMval3 = "46"
                            
                            nonlocal CMfval
                            CMfval = "47"
                            nonlocal CMval2
                            CMval2 = "48"
                            nonlocal CMval3
                            CMval3 = "4"
                            
                            disp()
                        
                        #Static Button
                        def static(*args):
                            os.system('')
                            print('Static Mode Button Pushed')
                            nonlocal DMfval
                            DMfval = "33"
                            nonlocal CMfval
                            CMfval = "34"
                            
                            Clock.schedule_once(staticdelay, 5)
                            disp()

                        
                        #Static Button
                        def staticdelay(*args):
                            os.system('')
                            print('Static Mode Delay Done')
                            nonlocal DMfval
                            DMfval = "11"
                            nonlocal CMfval
                            CMfval = "12"
                            
                            disp()

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
                            
                            typeVals = BoxLayout(orientation='horizontal')
                            
                            labtxt1 = "DML:\n___________________\n\nFrequency: " + DMfval + " HZ \n Average Energy: " + DMval2 + "\n Errors: " + DMval3 + "\n"
                            
                            labtxt2 = "CMOS:\n___________________\n\nFrequency: " + CMfval + " HZ \n Average Energy: " + CMval2 + "\n Errors: " + CMval3 + "\n"
                            lab = Label(text=labtxt1,font_size='20sp')
                            lab2 = Label(text=labtxt2,font_size='20sp')
                            
                            typeVals.add_widget(lab)
                            typeVals.add_widget(lab2)
                            
                            outer.add_widget(inner)
                            outer.add_widget(typeVals)
                            self.add_widget(outer)
                        
                        disp()
                        Clock.schedule_interval(disp, 0.5)
                        
                
                class Screen_Two(Screen):
                    def __init__(self, **kwargs):
                        super(Screen_Two, self).__init__(**kwargs)
                        self.name = "Two"
                        
                        #KILL Button
                        def killer(*args):
                            os.system('')
                            print('KILL ALL Button Pushed')
                            nonlocal DMfval
                            DMfval = '?'
                            nonlocal DMval2
                            DMval2 = "?"
                            nonlocal DMval3
                            DMval3 = "?"
                        
                            nonlocal CMfval
                            CMfval = '?'
                            nonlocal CMval2
                            CMval2 = "?"
                            nonlocal CMval3
                            CMval3 = "?"
                        
                        
                        outer2 = GridLayout(cols=1, rows=2, padding=200, pos=(00, 00),size=(Display.width, Display.height),spacing=50)
                        
                        kill = Button(text="Kill All",font_size='25sp',background_color=(1,0,0,1))
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

