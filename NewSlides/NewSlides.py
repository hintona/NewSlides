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

#ns = Builder.load_file("NewSlides.kv")

class WindowManager(ScreenManager):
    def buttonAnimInit(self, widget):
        animate = Animation(background_color=(95 / 255, 158 / 255, 160 / 255, 1), duration=.1)
        animate.start(widget)

    def buttonAnimFin(self, widget):
        animate = Animation(background_color=(0, 0, 0, 0), duration=.1)
        animate.start(widget)

class HomeWindow(Screen, Widget):
    def buttonAnimInit(self, widget):
        animate = Animation(background_color=(95 / 255, 158 / 255, 160 / 255, 1), duration=.1)
        animate.start(widget)

    def buttonAnimFin(self, widget):
        animate = Animation(background_color=(0, 0, 0, 0), duration=.1)
        animate.start(widget)

class MainWindow(Screen, Widget):
    def newSlide(self):
        grid = self.ids.slides
        grid.add_widget(Button(text="Slide", size_hint_y=None, height=200, background_color=(0,0,.1,.1), color=(0,0,.9,1)))
    def buttonAnimInit(self, widget):
        animate = Animation(background_color=(95/255,158/255,160/255,1), duration=.1)
        animate.start(widget)
    def buttonAnimFin(self, widget):
        animate = Animation(background_color=(0, 0, 0, 0), duration=.1)
        animate.start(widget)
class MyApp(App):
    def build(self):
        Window.maximize()
        Window.clearcolor = (1,1,1,1)
        ns = Builder.load_file("NewSlides.kv")
        return ns

MyApp().run()
