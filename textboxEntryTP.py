#file for all things text box related
#includes searching for a specific word and suggesting replacements for repetitive words
from tkinter import *
from tkinter.colorchooser import *
import string
from nltk.corpus import stopwords
import nltkTP as nltk
import nltk as n
import datetime


'''
Text box information from http://effbot.org/tkinterbook/text.htm
Entry information from http://effbot.org/tkinterbook/entry.htm
Menu design information from http://effbot.org/tkinterbook/menu.htm
Grid/packing information from https://effbot.org/tkinterbook/grid.htm

Word searching from http://effbot.org/tkinterbook/canvas.htm#Tkinter.Canvas.create_image-method
Datetime module information from https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
'''
class TextBox():
    def __init__(self, textBoxDims, data):
        self.master = Tk()
        self.drawWidgets(data)
        self.clickedButton = False
        self.typedText = ""     
        self.textColor = "black"   
        self.boxColor = (None, "white")
        self.font = "Times New Roman"
        self.fontSize = 12
        
        self.textBoxDims = textBoxDims
        self.x0 = textBoxDims[0]
        self.y0 = textBoxDims[1]
        self.x1 = textBoxDims[2]
        self.y1 = textBoxDims[3]
        self.page = data.leftPage
        
        self.moveBoxX = 0
        self.moveBoxY = 0
        
        self.category = False
        self.categoryName = ""
        
        self.journal = False #journal entry
        
        #searching text stuff
        self.setOfText = set()
        self.repWords = set()
        self.openSugg = 0 #0 = False
        
        self.wordSearch = None
        self.timeStamp = datetime.datetime.now()
        
    def drawWidgets(self, data):
        self.text = Text(self.master)
        self.text.grid(row=0, rowspan=10, column=0, columnspan=10)
        
        self.button = Button(self.master, text="submit", command=self.submitInfo)
        self.button.grid(row=11, column=1, columnspan=10)
        
        self.colorLabel = Label(self.master, text="type the color!")
        self.colorLabel.grid(row=1, column=11)
        self.colorEntry = Entry(self.master)
        self.colorEntry.grid(row=2, column=11)
        
        self.fontSizeLabel = Label(self.master, text="set font size!")
        self.fontSizeLabel.grid(row=3, column=11)
        self.fontSizeEntry = Entry(self.master)
        self.fontSizeEntry.grid(row=4, column=11)
        
        self.fontLabel = Label(self.master, text="set font!")
        self.fontLabel.grid(row=5, column=11)
        self.fontEntry = Entry(self.master)
        self.fontEntry.grid(row=6, column=11)
        
        self.question = Button(self.master, text="?", command=self.instructions)
        self.question.grid(row=11, column=0)
        
        self.catButt = Button(self.master, text="category", command=lambda:self.setCat(data))
        self.catButt.grid(row=7, column=11)
        
        self.entButt = Button(self.master, text="journal entry", command=self.setEnt)
        self.entButt.grid(row=8, column=11)
            
        self.analyzeButt = Button(self.master, text="analyze", command=lambda:self.searchText(3))
        self.analyzeButt.grid(row=11, column=2)

        #menu stuff
        menu = Menu(self.master)
        self.master.config(menu=menu)
        colormenu = Menu(menu)
        menu.add_cascade(label='Colors',menu=colormenu)
        colormenu.add_command(label='Text Color',command=self.changeTextColor)
        colormenu.add_command(label='Text Box Color',command=self.changeBoxColor)
    
    def setCat(self, data):
        self.category = True
        self.journal = False
        if self.text.get("1.0", "2.0-1c") not in data.categories:
            data.categories.append(self.text.get("1.0", "2.0-1c"))

        
    def setEnt(self):
        self.category = False
        self.journal = True
    
    def draw(self, canvas, data):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.boxColor[1])
        canvas.create_text(self.x0, self.y0, anchor=NW, text=self.typedText, width=self.x1-self.x0, fill=self.textColor, font=(self.font, self.fontSize))

    def inBox(self, x, y):
        if x < self.x1 and x > self.x0 and y < self.y1 and y > self.y0:
            return True
        return False
        
    def editText(self, x, y, str, index, data):
        if self.inBox(x, y):
            self.master = Tk()
            self.text = Text(self.master)
            self.text.grid(row=0, rowspan=10, column=0, columnspan=10)
            self.text.insert(END, self.typedText)
    
            self.button = Button(self.master, text="submit", command=self.submitInfo)
            self.button.grid(row=11, column=1, columnspan=10)
            
            self.colorLabel = Label(self.master, text="type the color!")
            self.colorLabel.grid(row=1, column=11)
            self.colorEntry = Entry(self.master)
            self.colorEntry.grid(row=2, column=11)
            
            self.fontSizeLabel = Label(self.master, text="set font size!")
            self.fontSizeLabel.grid(row=3, column=11)
            self.fontSizeEntry = Entry(self.master)
            self.fontSizeEntry.grid(row=4, column=11)
            
            self.fontLabel = Label(self.master, text="set font!")
            self.fontLabel.grid(row=5, column=11)
            self.fontEntry = Entry(self.master)
            self.fontEntry.grid(row=6, column=11)
            
            self.question = Button(self.master, text="?", command=self.instructions)
            self.question.grid(row=11, column=0)
            
            self.catButt = Button(self.master, text="category", command=lambda:self.setCat(data))
            self.catButt.grid(row=7, column=11)
            
            self.entButt = Button(self.master, text="journal entry", command=self.setEnt)
            self.entButt.grid(row=8, column=11)
            
            self.analyzeButt = Button(self.master, text="analyze", command=lambda:self.searchText(3))
            self.analyzeButt.grid(row=11, column=2)
            
            
            #menu stuff
            menu = Menu(self.master)
            self.master.config(menu=menu)
            colormenu = Menu(menu)
            menu.add_cascade(label='Colors',menu=colormenu)
            colormenu.add_command(label='Text Color',command=self.changeTextColor)
            colormenu.add_command(label='Text Box Color',command=self.changeBoxColor)
            
            self.openSugg = 3
            self.searchText(3)
            if self.boxColor[1] == "#b4ffff" and self.wordSearch != None:
                self.searchWord(data)
                
    # text searching information from http://effbot.org/tkinterbook/text.htm
    def searchWord(self, data): #search text for specific word
        clean = self.cleanText(self.typedText)
        if self.wordSearch in clean:
            self.boxColor = (None, "white")
            start = 1.0
            while True:
                index = self.text.search(self.wordSearch, start, stopindex="end", nocase=True)
                if not index:
                    break
                self.text.tag_add("found", index, "%s + %sc" %(index, len(self.wordSearch)))
                start = index + "+1c"
            self.text.tag_config("found", background="#b4ffff")
                
    def cleanText(self, string): #for searchWord
        clean = []
        tokens = n.word_tokenize(string)
        for elem in tokens:
            if elem.isalpha():
                clean.append(elem.lower())
        return clean
                
    def checkPunct(self, text):
        for punct in string.punctuation:
            if text.endswith(punct):
                return True
        return False
        
    def readText(self):
        stopWords = set(stopwords.words("english"))
        for text in self.typedText.split(" "):
            if self.checkPunct(text):
                if text[:-1].lower() not in stopWords:
                    self.setOfText.add(text[:-1].lower())
            else:
                if text.lower() not in stopWords:
                    self.setOfText.add(text.lower())
            
    def submitInfo(self):
        typedText = self.text.get("1.0", "end-1c") 
        self.typedText = typedText
        
        if self.category == True:
            self.categoryName = self.typedText
        self.clickedButton = True
        textColor = self.colorEntry.get()
        if textColor != "":
            self.textColor = textColor
        font = self.fontEntry.get()
        if font != "":
            self.font = font
        fontSize = self.fontSizeEntry.get()
        if fontSize != "":
            self.fontSize = int(fontSize)
        self.openSugg = 0
    
        self.searchText()
        if len(self.repWords) != 0:
            self.boxColor = (None, "#B7E8E8")
        else:
            self.boxColor = (None, "white")
            
        self.master.destroy()
        
# font list from https://stackoverflow.com/questions/39614027/list-available-font-families-in-tkinter
    def instructions(self):
        root = Tk()
        text = Text(root)
        text.pack()
        
        str = "To set the color, type in the name of the color in all lower case.\n\nTo set the font, here is a list of some possible fonts:\nMS Serif\nArial\nCambria Math\nComic Sans MS\nGeorgia\nImpact\nTahoma\nTimes New Roman"
        
        text.insert(END, str)
        root.mainloop()
        
    def setColor(self):
        color = self.entry.get()
        self.textColor = color
        
    def changeTextColor(self):
        color = askcolor()
        self.textColor = color[1]
        
    def changeBoxColor(self):
        color = askcolor()
        self.boxColor = color
        
    def moveBoxPress(self, x, y):
        if self.inBox(x, y):
            self.moveBoxX = x
            self.moveBoxY = y
        
    def moveTextBox(self, x, y):
        if self.inBox(x, y):
            width = self.x1 - self.x0
            height = self.y1 - self.y0
            dx = self.moveBoxX - self.x0
            self.x0 = x - dx
            self.x1 = self.x0 + width
            dy = self.moveBoxY - self.y0
            self.y0 = y - dy
            self.y1 = self.y0 + height
            self.moveBoxX = x
            self.moveBoxY = y

    #word searching, checking for repetitive words
    #tkinter colors from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    # text searching information from http://effbot.org/tkinterbook/text.htm
    def searchText(self, open=0):
        highColors = ["yellow", "plum1", "turquoise1", "PaleGreen1", "light pink"]
        self.typedText = self.text.get("1.0", "end-1c") 
        self.readText()
        i = -1
        self.repWords = set()
        cleanList = nltk.cleanTextStr(self.typedText)
        d = dict()
        for key in cleanList:
            if key in d:
                d[key] += 1
            else:
                d[key] = 1
        for word in self.setOfText:
            start = 1.0
            if word in d:
                if word != "" and word!= "\n" and d[word] >= 3:
                    i += 1
                    self.repWords.add(word)
                    while True:
                        self.index = self.text.search(word, start, stopindex="end", nocase=True)
                        if not self.index:
                            break
                        self.text.tag_add(str(i), self.index, "%s + %sc" %(self.index, len(word)))
                        start = self.index + "+1c"
                    self.text.tag_config(str(i), background=highColors[i%len(highColors)])
                    self.boxColor = (None, "#B7E8E8")
        self.master.update()
        if len(self.repWords) != 0 and open == 3:
            self.wordSuggestions(sorted(self.repWords))
        self.setOfText = set()
        
    
    def wordSuggestions(self, setOfWords):
        self.newRoot = Tk()
        self.textS = Text(self.newRoot)
        self.textS.grid(row=0, rowspan=10, column=0, columnspan=10)
        
        leftButton = Button(self.newRoot, text="back", command=lambda:self.changeWord("back"))
        leftButton.grid(row=11, column=0)
        
        rightButton = Button(self.newRoot, text="next", command=lambda:self.changeWord("next"))
        rightButton.grid(row=11, column=1)
        
        closeButton = Button(self.newRoot, text="close", command=self.closeWordSuggestions)
        closeButton.grid(row=11, column=2)
        
        self.wordResult = []
        for word in setOfWords:
            self.wordResult.append(nltk.findSynonyms(word))
        self.i = 0
        self.textS.insert(END, "You seem to use "+sorted(self.repWords)[self.i]+" a lot. Here are some synonyms.\n\n")
        for elem in self.wordResult[self.i]:
            self.textS.insert(END, elem)
            self.textS.insert(END, "\n")
            
    def changeWord(self, changer):
        if changer == "back":
            if self.i != 0:
                self.i -= 1
        elif changer == "next":
            if self.i < len(self.wordResult)-1:
                self.i += 1
        self.textS.delete(1.0, END)
        self.textS.insert(END, "You seem to use %s a lot. Here are some substitutions. \n\n" %sorted(self.repWords)[self.i])
        for elem in self.wordResult[self.i]:
            self.textS.insert(END, elem)
            self.textS.insert(END, "\n")
                
    def closeWordSuggestions(self):
        self.i = 0
        self.repWords = set()
        self.newRoot.destroy()
        
        
        
  