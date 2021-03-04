import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import (Rectangle, Ellipse, Line)
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput


class Slide(FloatLayout):
    def __init__(self, s, **kwargs):
        super(Slide, self).__init__(**kwargs)
        #self.source = s

        AddText = TextInput(font_size=30, size_hint_y=None, height=100, text='default')
        floaty = FloatLayout()
        scatter = Scatter()
        label = Label(text='default', font_size=30)
        label.color = 'red'
        AddText.bind(text=label.setter('text'))
        floaty.add_widget(scatter)
        scatter.add_widget(label)
        self.add_widget(AddText)
        self.add_widget(floaty)
        #im.export_to_png('oops')
        im = Image(source=s)
        self.add_widget(im)
        self.export_to_png('here.png')




def MakeSlide():
    return Slide('images\MLG_Glasses.png')

class MyApp(App):

    def build(self):
        s = MakeSlide()

        return s
if __name__ == '__main__':
    MyApp().run()