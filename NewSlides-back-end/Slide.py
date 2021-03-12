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
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
Builder.load_file("venv/Slide.kv")
LabelBase.register(name = 'Bengal', fn_bold='fonts/SutonnyMJ_Bold.ttf', fn_regular='fonts/SutonnyMJ_Regular.ttf',
                   fn_bolditalic="fonts/SutonnyMJ_Bold_Italic.ttf")
class Slide(Widget):
    def loadImage(self, filename):
        try:
            self.add_widget(Image(source = filename[0]))
        except:
            print('Error: file not found')
            pass
    def loadBackground(self, filename):
        try:
            self.ids.Background.source = filename[0]
        except:
            print('Error: file not found')
            pass
    def save(self):

        self.export_to_png('oops.png')
    def AddText(self):
        floaty = FloatLayout()
        scatter = Scatter()
        AddedText = Label(text='Enter your text here')
        #AddedText.font_name = 'Bengal'
        AddedText.bold = True
        TextAddition = TextInput(text='Enter your text here')
        FontSize = self.ids.FontSize
        FontSize.bind(text=AddedText.setter("font_size"))
        TextAddition.bind(text=AddedText.setter('text'))
        floaty.add_widget(scatter)
        scatter.add_widget(AddedText)
        self.add_widget(TextAddition)
        self.add_widget(floaty)








def MakeSlide():
    return Slide()


class MyApp(App):

    def build(self):
        s = MakeSlide()
        s.save()
        return s
if __name__ == '__main__':
    MyApp().run()
    #Window.screenshot(name='here.png')
