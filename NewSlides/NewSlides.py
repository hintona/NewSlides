import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button

Builder.load_file("venv/NewSlides.kv")


class MyLayout(Widget):
    def newSlide(self):
        grid = self.ids.slides
        grid.add_widget(Button(text="1"))

class MyApp(App):
    def build(self):
        Window.maximize()
        Window.clearcolor = (1,1,1,1)
        return MyLayout()

MyApp().run()