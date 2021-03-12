import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
import copy

#ns = Builder.load_file("NewSlides.kv")
class WindowManager(ScreenManager):
    pass

class HomeWindow(Screen, Widget):
    pass

class SlideView(GridLayout, Widget):
    def getSlideCount(self):
        return str(numSlides)

    def removeSlide(self):
        global numSlides
        slideView = self.getCountDisplay()
        grid = self.parent
        grid.remove_widget(self)
        numSlides -= 1
        slideView.text = "Slide Count: " + str(numSlides)
        for i in range(len(grid.children)):
            grid.children[len(grid.children)-i-1].ids.count.text = str(i+1)

    def duplicateSlide(self, SlideView):
        newSlide = copy.deepcopy(SlideView)
        newSlide.parent = None
        grid = self.parent
        grid.add_widget(newSlide)

    def changeSlideCount(self, checkbox):
        slideView = self.getCountDisplay()
        global numSlides
        if(checkbox.active):
            numSlides += 1
            slideView.text = "Slide Count: " + str(numSlides)
        else:
            numSlides -= 1
            slideView.text = "Slide Count: " + str(numSlides)

    def getCountDisplay(self):
        slideView = self.parent.parent.parent.parent.parent.parent.parent.ids.slideCount
        return slideView


class MainWindow(Screen, Widget):
    def newSlide(self):
        grid = self.ids.slides
        count = self.ids.slideCount
        global numSlides
        numSlides += 1
        grid.add_widget(SlideView())
        count.text = "Slide Count: " + str(numSlides)

class MyApp(App):
    def build(self):
        self.title = "New Slides"
        #self.main = MyApp.get_running_app()
        #print(self.main.root)
        Window.maximize()
        Window.clearcolor = (37/255,14/255,98/255,1)
        ns = Builder.load_file("NewSlides.kv")
        return ns

numSlides = 0
MyApp().run()