import kivy
import json
import os
from fpdf import FPDF
import PIL.Image
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.audio import SoundLoader
from kivy.storage.jsonstore import JsonStore
from kivy.uix.filechooser import FileChooserIconView
from copy import copy

#ns = Builder.load_file("NewSlides.kv")

class FilePopup(Popup):
    load = ObjectProperty()

class PresentationWindow(Popup):
    slideDeck = []
    images = []
    currSlide = 0
    slideGrid = None
    mSlideDisplay = None
    def back(self):
        slideDisplay = self.ids.slideDisplay
        if(self.currSlide>0):
            slideDisplay.remove_widget(self.slideDeck[self.currSlide])
            self.currSlide -= 1
            slideDisplay.add_widget(self.slideDeck[self.currSlide])
    def next(self):
        slideDisplay = self.ids.slideDisplay
        print(self.slideDeck)
        if (self.currSlide < len(self.slideDeck)-1):
            slideDisplay.remove_widget(self.slideDeck[self.currSlide])
            self.currSlide += 1
            slideDisplay.add_widget(self.slideDeck[self.currSlide])
    def addSlideDeck(self, slideDeck):
        global slides
        self.mSlideDisplay = slideDeck[0].parent
        for i in range(len(slideDeck)):
            self.slideDeck.append(slideDeck[i].slide)
            print(self.slideDeck[i].parent)
            if(slides[0]==slideDeck[i].slide):
            #self.images[i] = slideDeck[i].slide.export_to_png()
                slideDeck[i].slide.parent.remove_widget(slideDeck[i].slide)
                self.slideGrid = slideDeck[i].slide.parent
            print(self.slideDeck[i].parent)
        slideDeck[0].y = self.ids.slideDisplay.center[1]+200
        slideDeck[0].x = self.ids.slideDisplay.center[0]+200
        self.slideDeck = self.slideDeck[::-1]
        self.ids.slideDisplay.add_widget(self.slideDeck[0])

class soundButton(Button):
    sound = ObjectProperty()
    playing = False
    def addSound(self, sound):
        self.sound = sound
    def play(self):
        if self.playing:
            self.sound.stop()
            self.playing = False
        else:
            self.sound.play()
            self.playing = True

class WindowManager(ScreenManager):
    pass

class HomeWindow(Screen, Widget):
    pass

class SlideView(GridLayout, Widget):
    slide = None
    widgets = []
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
            if(slides[0].parent!=None):
                slides[0].parent.remove_widget(slides[0])
            slideContainer.add_widget(slides[0])
        if(self.ids.checkbox.active):
            numSlides -= 1
        else:
            slidesUnselected -= 1
            numSlides -= 1
        slideView.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)
        for i in range(len(grid.children)):
            grid.children[len(grid.children)-i-1].ids.count.text = "Slide " + str(i)

    #def addWidgets(self, list):
        #for i in range(len(list)):
            #self.widgets.append(list[i])

    def select(self):
        global slides
        global numSlides
        for i in range(len(self.widgets)):
            self.slide.add_widget(self.widgets[i])
        slideContainer = self.getSlideContainer()
        if(slides[0]!=self.slide):
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
        slide = Slide(pos=currSlide.pos)
        slide.size = currSlide.size
        slides.insert(0,slide)
        slideDisplay = SlideView()
        slideDisplay.setSlide(slide)
        grid.add_widget(slideDisplay)
        if(numSlides>1):
            currSlide.remove_widget(slides[1])
        currSlide.add_widget(slide)
        grid.parent.scroll_to(grid.children[0])
        count.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)

    def addSlide(self, slide):
        global numSlides
        global slides
        currSlide = self.ids.slide
        grid = self.ids.slides
        count = self.ids.slideCount
        numSlides += 1
        print(numSlides)
        slideName = "slide"+str(numSlides)+".png"
        slide.slide.pos = currSlide.pos
        slide.slide.size = currSlide.size
        slides.insert(0,slide.slide)
        slideDisplay = slide
        grid.add_widget(slideDisplay)
        if(numSlides>1):
            currSlide.remove_widget(slides[1])
        currSlide.add_widget(slide.slide)
        grid.parent.scroll_to(grid.children[0])
        count.text = "Slide Count: " + str(numSlides-slidesUnselected) + "/" + str(numSlides)
        print(numSlides)

    def present(self):
        slideView = self.ids.slides.children
        if(len(slideView)>0):
            self.pWindow = PresentationWindow()
            self.pWindow.open()
            self.pWindow.addSlideDeck(slideView)

    def open_popup(self):
        self.fileSelector = FilePopup(load=self.load)
        self.fileSelector.open()

    def spinner_clicked(self, font):
        regfont = self.ids.fontsize
        if(font == "Bengali"):
            self.ids.textInput.font_name = font
        else:
            self.ids.textInput.font_name = regfont.font_name

    def load(self, selection, type):
        global slides
        if (len(selection)>0 and len(slides)>0):
            currSlide = slides[0]
            self.file_path = selection[0]
            print(self.file_path)
            self.fileSelector.dismiss()
            if (type == "image"):
                formats = ["PNG","JPEG",]
                for format in formats:
                    if format in self.file_path:
                        image = Image(source=self.file_path)
                        scatter = Scatter(center=currSlide.center)
                        scatter.add_widget(image)
                        currSlide.add_widget(scatter)
            elif (type == "video"):
                formats = ["MP4", "M4V", "AVI"]
                for format in formats:
                    if format in self.file_path:
                        video = VideoPlayer(source=self.file_path, allow_fullscreen="false")
                        scatter = Scatter(center=currSlide.center)
                        scatter.add_widget(video)
                        currSlide.add_widget(scatter)
            elif (type == "audio"):
                formats = ["MP3", "WAV"]
                for format in formats:
                    if format in self.file_path:
                        sButton = soundButton()
                        sButton.addSound(SoundLoader.load(self.file_path))
                        sButton.y = currSlide.center[1]+currSlide.height/3.3
                        sButton.x = currSlide.center[0]+currSlide.width/3.3
                        currSlide.add_widget(sButton)
            elif (type == "presentation"):
                print(selection)
                #try:
                folder = selection
                print(folder)
                self.loadSlides(folder)
                #except:
                    #print("Wrong File Format")

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

    def clearSlides(self):
        slides = self.ids.slides
        slides.clear_widgets()

    def exportToPNG(self):
        slides = self.getSlides()
        slides = slides[::-1]
        slideImages = os.path.dirname(__file__)+"/slideImages/"
        for i in range(len(slides)):
            slides[i].export_to_png(slideImages + "Slide" + str(i) + ".png")
            image = PIL.Image.open(slideImages + "Slide" + str(i) + ".png")
            image = image.resize((650,750))
            image.save(slideImages + "Slide" + str(i) + ".png")

    def exportToPDF(self):
        slides = self.getSlides()
        if(len(slides)>0):
            self.exportToPNG()
            imagesPath = os.path.dirname(__file__)+"/slideImages/"
            slideImages = os.listdir(imagesPath)
            pdf = FPDF()
            for i in range(len(slideImages)):
                pdf.add_page(orientation="P")
                pdf.image(imagesPath+slideImages[i])
            pdf.output("Presentation.pdf", "F")
    def saveSlides(self):
        slides = self.getSlides()
        slides = slides[::-1]
        for i in range(len(slides)):
            print(type(slides[i]).__name__)
            list = []
            storeFile = os.path.dirname(__file__)+'/slideData/'+str(type(slides[i]).__name__)+str(i)+".json"
            for x in range(len(slides[i].children)):
                childList = slides[i].children[::-1]
                print(childList)
                widgetName = type(childList[x]).__name__
                data = {}
                for y in range(len(childList[x].children)):
                    widget = childList[x].children[y]
                    data[widgetName] = []
                    if(type(widget).__name__ == "Label"):
                        list.append({"type": "Label", "text": widget.text, "fontsize": widget.font_size})
                    elif(type(widget).__name__=="Image" or type(widget).__name__=="VideoPlayer"):
                        list.append({"type": str(type(widget).__name__),"source": widget.source})
                    elif (type(widget).__name__ == "soundButton"):
                        list.append({"type": str(type(widget.sound).__name__), "source": widget.sound.source})
                        print(str(type(widget).__name__))
                        print(str(type(widget.sound).__name__), widget.sound.source)
                data[widgetName] = list
                self.saveToJSON(data, storeFile)

    def loadSlides(self, folderPath):
        folder = os.listdir(folderPath+"\slideData")
        self.clearSlides()
        self.ids.slide.clear_widgets()
        global numSlides
        global slidesUnselected
        numSlides = 0
        slidesUnselected = 0
        for i in range(len(folder)):
            fileName = folderPath+"\slideData\\"+folder[i]
            print(fileName)
            with open(fileName) as f:
                data = json.load(f)
                print(data)
                keys = list(data.keys())
                widget = None
                slide = SlideView()
                slide.slide = Slide()
                for x in range(len(keys)):
                    print(data[keys[x]])
                    keyChildren = data[keys[x]]
                    widgetChild = None
                    if(keys[x] == "Scatter"):
                        widget = Scatter()
                    for y in range(len(keyChildren)):
                        child = keyChildren[y]
                        if(child['type'] == "Label"):
                            scatter = Scatter()
                            scatter.add_widget(Label(text=child['text'], font_size=child['fontsize'], color="black"))
                            widget.add_widget(scatter)
                        elif (child['type'] == "Image"):
                            scatter = Scatter()
                            scatter.add_widget(Image(source=child['source']))
                            widget.add_widget(scatter)
                        elif (child['type'] == "Video"):
                            scatter = Scatter()
                            scatter.add_widget(VideoPlayer(source=child['source']))
                            widget.add_widget(scatter)
                        elif (child['type'] == "Sound"):
                            scatter = Scatter()
                            sButton = soundButton()
                            sButton.addSound(child['source'])
                            scatter.add_widget(sButton)
                            widget.add_widget(scatter)
                print(widget.children)
                slide.slide.add_widget(widget)
                self.addSlide(slide)
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
        if(len(slides)>0):
            currSlide = slides[0]
            scatter = Scatter(center=currSlide.center)
            AddedText = Label(text=self.ids.textInput.text, color="black")
            # AddedText.font_name = 'Bengal'
            AddedText.bold = True
            AddedText.font_name = self.ids.textInput.font_name
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
        AddedText.font_name = self.textInput.font.font_name
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
fontSize = 50
MyApp().run()