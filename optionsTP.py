#file for everything the options on the side do
#like searching for words, skipping pages, create categories, and drawing
#the options
from tkinter import *
from nltk.corpus import wordnet as wn
import textboxEntryTP as tb
import pageTP as pg

'''
Text box information from http://effbot.org/tkinterbook/text.htm
Entry information from http://effbot.org/tkinterbook/entry.htm
Menu design information from http://effbot.org/tkinterbook/menu.htm
Grid/packing information from https://effbot.org/tkinterbook/grid.htm
'''
#wordnet information from https://www.cs.princeton.edu/courses/archive/fall06/cos226/assignments/wordnet.html
def wordsInCategory(category):
    sets = wn.synsets(category)
    checkSet = sets[0]
    names = checkSet.hyponyms()
    nameResult = []
    for name in names:
        nameResult.append(name.name())
    result = set()
    for item in nameResult:
        stopPoint = item.index(".")
        result.add(item[:stopPoint])
    return sorted(result)

class Options(object):
    def __init__(self, x0, y0, x1, y1, color, text):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.color = color
        self.text = text
        self.cat = ""
        self.inCat = set()

    def draw(self, canvas):
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.color)
        x = (self.x0 + self.x1)/2
        y = (self.y0 + self.y1)/2
        canvas.create_text(x, y, text=self.text, font=("Trebuchet MS", 12))

    def inButton(self, data, x, y):
        if x < self.x1 and x > self.x0:
            if y < self.y1 and y > self.y0:
                return True
        return False

    def createCategories(self, data):
        self.master = Tk()
        self.textbox = Text(self.master)
        self.textbox.pack()
        str="create categories! click check to see everything in that category"
        self.textbox.insert(END, str)

        self.button = Button(self.master, text="check", command=lambda:self.checkCategories(data))
        self.button.pack(fill="both", side="left", expand="true")

        self.updateButt = Button(self.master, text="update category", command=lambda:self.updateCat(data))
        self.updateButt.pack(fill="both", side="left", expand="true")

        self.submitButt = Button(self.master, text="submit as category", command=lambda:self.submit(data))
        self.submitButt.pack(fill="both", side="right", expand="true")

        self.closeButt = Button(self.master, text="close", command=lambda:self.close(data))
        self.closeButt.pack(fill="both", side="right", expand="true")

        #self.master.mainloop()

    def updateCat(self, data):
        data.createCat = True
        text = self.textbox.get("1.0", "end-1c")
        clean = text.split("\n")
        for i in range(2, len(clean)):
            self.inCat.add(clean[i])
        self.cat = self.textbox.get("1.0", "2.0-1c")
        data.ownCatDict[data.categoryButt.cat] = data.categoryButt.inCat

    def checkCategories(self, data):
        self.cat = self.textbox.get("1.0", "2.0-1c")
        if self.cat in data.ownCatDict:
            addText = data.ownCatDict[data.categoryButt.cat]
        else:
            addText = wordsInCategory(self.cat)
        self.textbox.insert(END, "\n")
        for word in addText:
            self.textbox.insert(END, "\n"+word)

    def submit(self, data):
        data.createCat = True
        text = self.textbox.get("1.0", "end-1c")
        clean = text.split("\n")
        for i in range(2, len(clean)):
            self.inCat.add(clean[i])
        self.cat = self.textbox.get("1.0", "2.0-1c")
        if self.cat not in data.categories:
            data.categories.append(self.cat)
        data.tOC.drawWidgets(data)

    def close(self, data):
        data.createCat = False
        self.master.destroy()

class HalfBox(Options):
    def __init__(self, x0, y0, x1, y1, color, text):
        super().__init__(x0, y0, x1, y1, color, text)

import nltk as n
from nltk.corpus import wordnet as wn
#wordnet information from https://www.cs.princeton.edu/courses/archive/fall06/cos226/assignments/wordnet.html

class OrgText(object):
    def __init__(self, master, data):
        self.master = master
        self.drawWidgets(data)
        self.orgText = ""
        self.corrCateg = None
        self.corrDate = None
        self.dateStuff = ""
        self.days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December",
                        "Jan", "Feb", "Mar", "Jun", "Aug", "Sept", "Oct", "Nov", "Dec"]
        self.corrMonth = None

    def drawWidgets(self, data):
        self.entry = Entry(self.master)
        self.entry.pack()

        self.button = Button(self.master, text="submit", command=lambda:self.submitInfo(data))
        self.button.pack()

#tagging information from http://sapir.psych.wisc.edu/programming_for_psychologists/cheat_sheets/Text-Analysis-with-NLTK-Cheatsheet.pdf
    def tagWord2(self, sentence):
        d = {"NN":"n", "VB":"v"}
        tokens = n.word_tokenize(sentence)
        tagged = n.pos_tag(tokens)
        simplePOSTag = []
        for (word, pos) in tagged:
            if pos not in d:
                simplePOS = "n"
            else:
                simplePOS = d[pos]
            simplePOSTag.append((word, simplePOS))
        return simplePOSTag

    def relatedWord(self, word, data):
        category = data.categories
        tagged = self.tagWord2(word)
        searchWords = []
        for (word, pos) in tagged:
            searchWords.append(word + "." + pos + ".01")
        for categ in category:
            synset = set(wn.synsets(categ))
            for syn in synset:
                for searchWord in searchWords:
                    try:
                        word = wn.synset(searchWord)
                        common = syn.lowest_common_hypernyms(word)
                        for i in range(len(common)):
                            if common != []:
                                if common[i].name() == syn.name():
                                    return categ
                            else:
                                break
                    except:
                        continue

    def submitInfo(self, data):
        self.orgText = self.entry.get()
        word = self.orgText

        corrCategory = self.relatedWord(word, data)
        if corrCategory == None:
            for key in data.ownCatDict: #look at user made categories
                for w in word.split(" "):
                    if w in data.ownCatDict[key]:
                        corrCategory = key
        self.corrCateg = corrCategory

        if self.corrCateg == None:
            if self.checkForDates(word) != False:
                if self.checkForDates(word) == True:
                    if self.checkForNum(word) != False:
                        self.corrDate = str(self.checkForNum(word))
                        self.dateStuff = word
                else: #if its a month
                    if self.checkForNum(word) != False:
                        self.corrDate = str(self.checkForNum(word))
                        self.dateStuff = word
                        self.corrMonth = str(self.checkForDates(word))
        self.master.destroy()

    def checkForDates(self, word):
        listOfWords = word.split(" ")
        for item in listOfWords:
            if item in self.month:
                return self.month.index(item)%12
            if item in self.days:
                return True
        return False

    def checkForNum(self, word):
        listOfWords = word.split(" ")
        for item in listOfWords:
            try:
                int(item)
                return(int(item))
            except:
                continue
        return False

class SkipPage(object):
    def __init__(self, data):
        self.drawWidgets(data)
        self.pageSkip = ""

    def drawWidgets(self, data):
        self.master = Tk()
        self.entry = Entry(self.master)
        self.entry.pack()

        self.button = Button(self.master, text="skip to this page", command=lambda:self.submit(data))
        self.button.pack()

    def submit(self, data):
        self.pageSkip = int(self.entry.get())
        self.skipPage(data, self.pageSkip)
        self.master.destroy()

    def skipPage(self, data, pageNum):
        if int(pageNum)%2 == 0:
            data.rightPage = int(pageNum)
            data.leftPage = data.rightPage-1
        else:
            data.leftPage = int(pageNum)
            data.rightPage = data.leftPage + 1
        for p in range(1, data.rightPage, 2):
            if pg.Page(p, p+1) not in data.page:
                data.page.append(pg.Page(p, p+1))

# text searching information from http://effbot.org/tkinterbook/text.htm
class SearchForWord(object):
    def __init__(self, data):
        self.drawWidgets(data)

    def drawWidgets(self, data):
        self.master = Tk()
        self.entry = Entry(self.master)
        self.entry.pack()

        self.button = Button(self.master, text="search for this word", command=lambda:self.submit(data))
        self.button.pack()

    def submit(self, data):
        self.wordSearch = self.entry.get()
        self.searchWord(data)
        self.master.destroy()

    def searchWord(self, data):
        for textBo in data.textBoxes:
            clean = self.cleanText(textBo.typedText)
            if self.wordSearch in clean:
                textBo.boxColor = (None, "#b4ffff")
                textBo.wordSearch = self.wordSearch

    def cleanText(self, string):
        clean = []
        tokens = n.word_tokenize(string)
        for elem in tokens:
            if elem.isalpha():
                clean.append(elem.lower())
        return clean

class CreateCategory(object):
    def __init__(self, data):
        self.drawWidgets(data)

    def drawWidgets(self, data):
        self.master = Tk()
        self.entry = Entry(self.master)
        self.entry.pack()

        self.button = Button(self.master, text="make this a category", command=lambda:self.submit(data))
        self.button.pack()

    def submit(self, data):
        category = self.entry.get()
        if category not in data.categories:
            data.categories.append(category)
        data.tOC.drawWidgets(data)
        self.master.destroy()