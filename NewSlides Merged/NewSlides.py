import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView

#ns = Builder.load_file("NewSlides.kv")
class FilePopup(Popup):
    load = ObjectProperty()

class WindowManager(ScreenManager):
    pass

class HomeWindow(Screen, Widget):
    pass

class SlideView(GridLayout, Widget):
    slide = None

    def setSlide(self, Label):
        self.slide = Label

    def getSlideCount(self):
        return str(numSlides)

    def removeSlide(self):
        global numSlides
        global slidesUnselected
        #global selectedSlide
        #selectedSlide.remove(self)
        slideView = self.getCountDisplay()
        grid = self.parent
        grid.remove_widget(self)
        if(self.ids.checkbox.active):
            numSlides -= 1
        else:
            slidesUnselected -= 1
            numSlides -= 1
        slideView.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)
        for i in range(len(grid.children)):
            grid.children[len(grid.children)-i-1].ids.count.text = str(i+1)
           # selectedSlide[i] = grid.children[len(grid.children)-i-1]

    #def duplicateSlide(self, SlideView):
        #newSlide.parent = None
        #grid = self.parent
        #grid.add_widget(newSlide)

    def changeSlideCount(self, checkbox):
        slideView = self.getCountDisplay()
        global slidesUnselected
        if(checkbox.active):
            slidesUnselected -= 1
            slideView.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)
        else:
            slidesUnselected += 1
            slideView.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)

    def getCountDisplay(self):
        slideView = self.parent.parent.parent.parent.parent.parent.parent.ids.slideCount
        return slideView

    #def select(self):
        #global selectedSlide
        #selectedSlide.insert(0, selectedSlide.pop(selectedSlide.index(self)))
        #self.slide


class MainWindow(Screen, Widget):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)
    def newSlide(self):
        global numSlides
        #global selectedSlide
        currSlide = self.ids.slide
        grid = self.ids.slides
        count = self.ids.slideCount
        numSlides += 1
        slideName = "slide"+str(numSlides)+".png"
        slide = SlideView()
        grid.add_widget(slide)
        slideImage = Image(source="images/defaultimage.png", center_x=currSlide.x+50, center_y=currSlide.y+50, size=currSlide.size)
        #slideLabel = Label()
        #selectedSlide.insert(0, slide)
        #slideLabel.add_widget(slideImage)
        currSlide.add_widget(slideImage)
        currSlide.export_to_png(slideName)
        slide.setSlide(currSlide)
        grid.parent.scroll_to(grid.children[0])
        count.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)

    def open_popup(self):
        self.the_popup = FilePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        currSlide = self.ids.slide
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        image = Image(source=self.file_path)
        scatter = Scatter(center=currSlide.center)
        scatter.add_widget(image)
        currSlide.add_widget(scatter)

    def increaseFontSize(self):
        global fontSize
        if (fontSize < 150):
            fontSize += 1
            self.ids.fontsize.text = str(fontSize)
    def decreaseFontSize(self):
        global fontSize
        if(fontSize > 1):
            fontSize -= 1
            self.ids.fontsize.text = str(fontSize)
    #def changeFontSize(self):

    def loadImage(self, filename):
        try:
            self.add_widget(Image(source=filename[0]))
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
        slides = self.ids.slides
        for i in range(len(slides.children)):
            print(slides.children[i].slide.children)
            slides.children[i].slide.export_to_png("slide"+str(i)+".png")
        #self.export_to_png('oops.png')

    def AddText(self):
        global fontSize
        currSlide = self.ids.slide
        scatter = Scatter(center=currSlide.center)
        AddedText = Label(text=self.ids.textInput.text, color="black")
        # AddedText.font_name = 'Bengal'
        AddedText.bold = True
        AddedText.font_size = fontSize
        scatter.add_widget(AddedText)
        currSlide.add_widget(scatter)

class MyApp(App):
    def build(self):
        self.title = "New Slides"
        #self.main = MyApp.get_running_app()
        #print(self.main.root)
        Window.maximize()
        Window.clearcolor = (37/255,14/255,98/255,1)
        ns = Builder.load_file("NewSlides.kv")
        return ns

#selectedSlide = []
numSlides = 0
slidesUnselected = 0
fontSize = 10
MyApp().run()