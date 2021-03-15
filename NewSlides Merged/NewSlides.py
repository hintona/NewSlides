import kivy
import json
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.storage.jsonstore import JsonStore
from kivy.uix.filechooser import FileChooserIconView
from copy import copy

#ns = Builder.load_file("NewSlides.kv")
class FilePopup(Popup):
    load = ObjectProperty()

class PresentationWindow(Popup):
    slideDeck = []
    currSlide = 0
    def back(self):
        slideDisplay = self.ids.slideDisplay
        if(self.currSlide>0):
            slideDisplay.remove_widget(self.slideDect(self.currSlide))
            self.currSlide -= 1
            slideDisplay.add_widget(self.slideDeck[self.currSlide])
    def next(self):
        slideDisplay = self.ids.slideDisplay
        if (self.currSlide < len(self.slideDeck)-1):
            slideDisplay.remove_widget(self.slideDect(self.currSlide))
            self.currSlide += 1
            slideDisplay.add_widget(self.slideDeck[self.currSlide])
    def addSlideDeck(self, slideDeck):
        for i in range(len(slideDeck)):
            self.slideDeck.append(slideDeck[i].slide)
            print(self.slideDeck[i].parent)
            self.slideDeck[i].parent.remove_widget(self.slideDeck[i])
            print(self.slideDeck[i].parent)
            print("yes")
        slideDeck[0].center = self.ids.slideDisplay.center
        self.ids.slideDisplay.add_widget(self.slideDeck[0])
        print("yes")

class WindowManager(ScreenManager):
    pass

class HomeWindow(Screen, Widget):
    pass

class SlideView(GridLayout, Widget):
    slide = None
    def setSlide(self, slide):
        self.slide = slide

    def getSlideCount(self):
        return str(numSlides)

    def removeSlide(self):
        global numSlides
        global slidesUnselected
        global slides
        slides.remove(self.slide)
        slideContainer = self.getSlideContainer()
        slideContainer.remove_widget(self.slide)
        slideView = self.getCountDisplay()
        grid = self.parent
        grid.remove_widget(self)
        print(len(slides))
        if(len(slides)>=1):
            slideContainer.add_widget(slides[0])
        if(self.ids.checkbox.active):
            numSlides -= 1
        else:
            slidesUnselected -= 1
            numSlides -= 1
        slideView.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)
        for i in range(len(grid.children)):
            grid.children[len(grid.children)-i-1].ids.count.text = str(i+1)

    def select(self):
        global slides
        global numSlides
        slideContainer = self.getSlideContainer()
        if(numSlides>1):
            slides.insert(0, slides.pop(slides.index(self.slide)))
            slideContainer.remove_widget(slides[1])
        slideContainer.add_widget(self.slide)

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

    def getSlideContainer(self):
        slideContainer = self.parent.parent.parent.parent.parent.parent.parent.ids.slide
        return slideContainer

class MainWindow(Screen, Widget):
    file_path = StringProperty("No file chosen")
    flieSelector = ObjectProperty(None)
    pWindow = ObjectProperty(None)
    #saveFile = JsonStore("save_file.json")
    def newSlide(self):
        global numSlides
        global slides
        currSlide = self.ids.slide
        grid = self.ids.slides
        count = self.ids.slideCount
        numSlides += 1
        slideName = "slide"+str(numSlides)+".png"
        slide = Slide(center=currSlide.center)
        slides.insert(0,slide)
        slideDisplay = SlideView()
        slideDisplay.setSlide(slide)
        grid.add_widget(slideDisplay)
        slideImage = Image(source="images/default_image.png", center_x=currSlide.x+50, center_y=currSlide.y+50, size=currSlide.size)
        slide.addImage(slideImage)
        if(numSlides>1):
            currSlide.remove_widget(slides[1])
        currSlide.add_widget(slide)
        slide.export_to_png(slideName)
        grid.parent.scroll_to(grid.children[0])
        count.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)

    def present(self):
        slideView = self.ids.slides.children
        self.pWindow = PresentationWindow()
        self.pWindow.open()
        self.pWindow.addSlideDeck(slideView)
    def open_popup(self):
        self.fileSelector = FilePopup(load=self.load)
        self.fileSelector.open()

    def load(self, selection, type):
        global slides
        currSlide = slides[0]
        self.file_path = selection[0]
        self.fileSelector.dismiss()
        if (type == "image"):
            image = Image(source=self.file_path)
            scatter = Scatter(center=currSlide.center)
            scatter.add_widget(image)
            currSlide.add_widget(scatter)
        else:
            video = VideoPlayer(source=self.file_path)
            scatter = Scatter(center=currSlide.center)
            scatter.add_widget(video)
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

    def getSlides(self):
        retlist = []
        slides = self.ids.slides.children
        for i in range(len(slides)):
            retlist.append(slides[i].slide)
        return retlist

    def saveSlides(self):
        slides = self.getSlides()
        slides = slides[::-1]
        for i in range(len(slides)):
            print(type(slides[i]).__name__)
            list = []
            storeFile = os.path.dirname(__file__)+'/slideData/'+str(type(slides[i]).__name__)+str(i)+".json"
            for x in range(len(slides[i].children)):
                childList = slides[i].children[::-1]
                widgetName = type(childList[x]).__name__
                data = {}
                for y in range(len(childList[x].children)):
                    widget = childList[x].children[y]
                    data[widgetName] = []
                    if(type(widget).__name__ == "Label"):
                        list.append({"type": "Label", "text": widget.text, "fontsize": widget.font_size})
                    elif(type(widget).__name__=="Image" or type(widget).__name__=="VideoPlayer"):
                        list.append({"type": str(type(widget).__name__),"source": widget.source})
                data[widgetName] = list
                self.saveToJSON(data, storeFile)

    def loadSlides(self):
        pass
    #def loadSlides(self):

    def saveToJSON(self, data, filename):
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    #def save(self):
        #global slides
        #saveFile = JsonStore("save_file.json")
        #for i in range(len(slides)):
            #numWidgets = len(slides[i].children)
            #saveFile.put("slide"+str(i), length=str(numWidgets))
            #for x in range(numWidgets):
                #currWidget = type(slides[i].children[x])
                #saveFile.put(str(currWidget), center=str(currWidget.get_top(currWidget)))
    def AddText(self):
        global fontSize
        global slides
        currSlide = slides[0]
        scatter = Scatter(center=currSlide.center)
        AddedText = Label(text=self.ids.textInput.text, color="black")
        # AddedText.font_name = 'Bengal'
        AddedText.bold = True
        AddedText.font_size = fontSize
        scatter.add_widget(AddedText)
        currSlide.add_widget(scatter)

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

    def addImage(self, image):
        self.add_widget(image)
class MyApp(App):
    def build(self):
        self.title = "New Slides"
        Window.maximize()
        Window.clearcolor = (37/255,14/255,98/255,1)
        ns = Builder.load_file("NewSlides.kv")
        return ns

slides = []
numSlides = 0
slidesUnselected = 0
currSlide = None
fontSize = 10
MyApp().run()