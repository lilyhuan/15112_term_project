#file for all things page related and for preset designs
from tkinter import *
from tkinter.colorchooser import *
import datetime

'''
Text box information from http://effbot.org/tkinterbook/text.htm
Entry information from http://effbot.org/tkinterbook/entry.htm
Menu design information from http://effbot.org/tkinterbook/menu.htm
Grid/packing information from https://effbot.org/tkinterbook/grid.htm
Datetime information from https://docs.python.org/2/library/datetime.html
'''

class Page(object):
    def __init__(self, pageNumLeft, pageNumRight):
        self.pNL = pageNumLeft
        self.pNR = pageNumRight

    def draw(self, canvas, data):
        canvas.create_line((data.width-data.buttWidth-2*data.buttMarg)/2, 0, (data.width-data.buttWidth-2*data.buttMarg)/2, data.height)
        if self.pNL != -1:
            canvas.create_text(7,data.height-7, text=str(self.pNL))
            canvas.create_text(data.width-data.buttWidth-2*data.buttMarg-7, data.height-7, text=str(self.pNR))

class PresetTB(Page):
    def __init__(self, pageNumLeft, pageNumRight, dims, month):
        super().__init__(pageNumLeft, pageNumRight)
        self.x0 = dims[0]
        self.y0 = dims[1]
        self.x1 = dims[2]
        self.y1 = dims[3]
        self.typedText = str(dims[4])
        self.presetText = str(dims[4])
        self.journal = False
        self.page = pageNumLeft

        self.textColor = "black"
        self.boxColor = (None, "white")
        self.font = "Times New Roman"
        self.fontSize = 12

        self.moveBoxX = 0
        self.moveBoxY = 0

        self.category = False
        self.categoryName = ""

        self.entry = False #journal entry

        self.month = month

    def draw(self, canvas, data):
        canvas.create_line((data.width-data.buttWidth-2*data.buttMarg)/2, 0, (data.width-data.buttWidth-2*data.buttMarg)/2, data.height, fill="white")
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

            #menu stuff
            menu = Menu(self.master)
            self.master.config(menu=menu)
            colormenu = Menu(menu)
            menu.add_cascade(label='Colors',menu=colormenu)
            colormenu.add_command(label='Text Color',command=self.changeTextColor)
            colormenu.add_command(label='Text Box Color',command=self.changeBoxColor)

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
        self.master.destroy()

# font commands https://stackoverflow.com/questions/39614027/list-available-font-families-in-tkinter
    def instructions(self):
        root = Tk()
        text = Text(root)
        text.pack()

        str = "To set the color, type in the name of the color in all lower case.\n\nTo setS the font, here is a list of some possible fonts:\nSegoe Script\nMS Serif\nArial\nCambria Math\nComic Sans MS\nGeorgia\nImpact\nTahoma\nTimes New Roman\nTrebuchet MS"

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

    def setCat(self, data):
        self.category = True
        self.journal = False
        if self.text.get("1.0", "2.0-1c") not in data.categories:
            data.categories.append(self.text.get("1.0", "2.0-1c"))
            self.categoryName = self.get("1.0, 2.0-1c")

    def setEnt(self):
        self.category = False
        self.journal = True

def calendarDims(data, numDates, day, month):
    result = []
    #days
    pageWidth = data.buttMenu-20
    days = ["Sunday\n"+month, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for i in range(7):
        result.append([10+i*pageWidth/7, 10, 10+(i+1)*pageWidth/7, 60, days[i]])
    startDay = days[day]
    #dates
    if (numDates+day)/7 < 5:
         rows = 5
    else:
        rows = 6
    cols = 7
    pageHeight = data.height-70
    dates = [""]*day
    dates.extend(list((range(1,numDates+1))))
    dates.extend([""]*8)
    index = 0
    for row in range(rows):
        for col in range(cols):
            result.append([10+col*pageWidth/7, 60+row*pageHeight/rows, 10+(col+1)*pageWidth/7, 60+(row+1)*pageHeight/rows, dates[index]])
            index += 1
    return result

def dailyDims(data, numDates, day, month):
    result = []
    pageWidth = data.buttMenu-20
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for i in range(7):
        result.append([10+i*pageWidth/7, 10, 10+(i+1)*pageWidth/7, 70, days[i]])
        result.append([10+i*pageWidth/7, 70, 10+(i+1)*pageWidth/7, data.height-10, ""])
    return result

def linedPages(data):
    result = []
    lines = 25
    for i in range(lines):
        result.append([0,i*data.height/lines, data.buttMenu, i*data.height/lines, data.leftPage])
    return result

def dotPage(data):
    result = []
    rows = 25
    cols = 50
    radius = 1
    for row in range(rows):
        for col in range(cols):
            x0 = col*data.buttMenu/cols
            y0 = row*data.height/rows
            x1 = (col+1)*data.buttMenu/cols
            y1 = (row+1)*data.height/rows-20
            result.append([(x0+x1)/2-radius, (y0+y1)/2-radius, (x0+x1)/2+radius, (y0+y1)/2+radius, data.leftPage])
    return result