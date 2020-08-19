#main tp file, where the run function is
from tkinter import *
from tkinter.colorchooser import *
from tkinter import filedialog
import datetime

import textboxEntryTP as tb
import optionsTP as op
import nltkTP as nltk
import pageTP as pg        
import sideMenuTP as sm
import imageTP as im
import saveTP as sav
 
'''
Text box information from http://effbot.org/tkinterbook/text.htm
Entry information from http://effbot.org/tkinterbook/entry.htm
Menu design information from http://effbot.org/tkinterbook/menu.htm
Grid/packing information from https://effbot.org/tkinterbook/grid.htm
Colors from https://material.io/tools/color/#!/?view.left=0&view.right=0
'''

#from 112 course notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)
    
def init(data):
    data.start = True
    data.categoryButt = op.Options(data.width/2-75, data.height-100, data.width/2+75, data.height-50, rgbString(219, 206, 140), "create categories!")
    data.ownCatDict = dict()
    data.createCat = False
    data.categories = [] #for nltk
    
    
    data.textBoxDims = []
    data.textBoxes = []
    
    data.buttHeight = 75
    data.buttWidth = 150
    data.buttMarg = 5
    data.numButts = 9
    data.buttSpace = (data.height - (data.numButts * data.buttHeight + 2*data.buttMarg + 115))/(data.numButts-1)
    data.buttMenu = data.width-(data.buttMarg*2 + data.buttWidth)
    
    data.drawTextBox = False
    
    data.leftPage = None
    data.rightPage = None
    
    data.optColor = rgbString(255, 244, 191)
    data.optPressedColor = rgbString(219, 206, 140)
    data.menuBack = rgbString(255, 244, 191)
    data.menuButton = rgbString(219, 206, 140)
    
    data.options = [] #list of button options
    data.optText = ["insert text box", "resize/delete", "draw", "organize", "analyze", "search", "insert image", "skip page", "create category"]
    for i in range(data.numButts): #make option buttons
        startX = data.width-data.buttMarg-data.buttWidth
        endX = data.width-data.buttMarg
        startY = data.buttMarg+data.buttHeight*i+data.buttSpace*i
        endY = data.buttMarg+data.buttHeight*(i+1)+data.buttSpace*i
        data.options.append(op.Options(startX, startY, endX, endY, data.optColor, data.optText[i]))

        
    #nltk stuff
    data.sort = None #objects
    data.sortText = []
    
    data.leftArrow = op.HalfBox(data.width-data.buttMarg-data.buttWidth, data.height-50, data.width-data.buttMarg-data.buttWidth/2, data.height-5, data.optColor, "back")
    data.rightArrow = op.HalfBox(data.width-data.buttMarg-data.buttWidth/2, data.height-50, data.width-data.buttMarg, data.height-5, data.optColor, "forward")

    data.home = op.Options(data.width-data.buttMarg-data.buttWidth, data.height-112, data.width-data.buttMarg, data.height-57, data.optColor, "home")
    
    data.page = [pg.Page(1, 2)]
    data.presetPage = []
    data.presetPage2d = []
    data.linedPages = []
    data.dottedPages = []
    
#Datetime information from https://docs.python.org/2/library/datetime.html
    data.today = str(datetime.date.today())[-2:]
    if data.today[-2] == "0":
        data.today = data.today[-1]
    data.month = str(datetime.date.today())[5:7]
    if data.month[-2] == "0":
        data.month = str(int(data.month[-1])-1)
    else:
        data.month = str(int(data.month)-1)
    
    data.resize = False
    data.focusBox = None
    data.focusImage = None
    
    data.tOC = sm.SideMenu(Tk()) #table of contents
    
    data.images = []
    
    data.draw = False
    data.oldXY = []
    
    data.skipToPage = None
    
def mousePressed(event, data):
    if data.start == True: #start page
        if event.x < (data.width/2+100) and event.x > (data.width/2-100):
            if event.y < (data.height*2/3+50) and event.y > (data.height*2/3-50):
                data.start = False
                data.leftPage = 1
                data.rightPage = 2
        if data.categoryButt.inButton(data, event.x, event.y):
            data.categoryButt.createCategories(data)
                
                
    else: #not start page        
        if data.options[0].inButton(data, event.x, event.y) == True:
            data.drawTextBox = True
            data.options[0].color = data.optPressedColor
            
        if data.options[1].inButton(data, event.x, event.y) == True: #resize/delete
            data.resize = not data.resize
            if data.options[1].color == data.optPressedColor:
                data.options[1].color = data.optColor
                data.focusBox = None
                data.focusImage = None
            else:
                data.options[1].color = data.optPressedColor
                
        if data.options[2].inButton(data, event.x, event.y) == True: #draw
            data.draw = not data.draw
            if data.options[2].color == data.optPressedColor:
                data.options[2].color = data.optColor
            else:
                data.options[2].color = data.optPressedColor
            
            
        if data.options[3].inButton(data, event.x, event.y) == True: #sort text button
            data.sort = op.OrgText(Tk(), data)
            
        if data.options[4].inButton(data, event.x, event.y) == True: #analyze
            journalEntries = []
            for i in range(len(data.textBoxes)):
                if data.textBoxes[i].journal == True:
                    journalEntries.append(data.textBoxes[i].typedText)
            if len(journalEntries) != 0:
                nltk.graphAll(journalEntries)
                
        if data.options[5].inButton(data, event.x, event.y) == True:
            op.SearchForWord(data)
            
        # dialog box information from https://www.youtube.com/watch?v=UxSeMIBCKP0 and 
        # http://effbot.org/tkinterbook/tkinter-file-dialogs.htm
        if data.options[6].inButton(data, event.x, event.y) == True: #insert image
            picName = filedialog.askopenfilename()
            data.images.append(im.ImageInsert(picName, data.leftPage))
            
        if data.options[7].inButton(data, event.x, event.y) == True: #skip pages
            op.SkipPage(data)

        if data.options[8].inButton(data, event.x, event.y) == True:
            op.CreateCategory(data)

        if data.home.inButton(data, event.x, event.y) == True:
            data.start = True
            data.leftPage = None
            data.rightPage = None

        if data.leftArrow.inButton(data, event.x, event.y) == True:
            if data.leftPage == 1:
                data.start = True
                data.leftPage -= 2
                data.rightPage -= 2
            else:
                data.leftPage -= 2
                data.rightPage -= 2
        if data.rightArrow.inButton(data, event.x, event.y) == True:
            data.leftPage += 2
            data.rightPage += 2
            if pg.Page(data.leftPage, data.rightPage) not in data.page:
                data.page.append(pg.Page(data.leftPage, data.rightPage))  
                              
        if data.drawTextBox == True and event.x < data.buttMenu:
            data.textBoxDims.append([event.x, event.y])
            
        if data.resize == True and event.x < data.buttMenu:
            for i in range(len(data.textBoxes)):
                if data.textBoxes[i].page == data.leftPage and data.textBoxes[i].inBox(event.x, event.y):
                    data.focusBox = i
                    data.focusImage = None
            for i in range(len(data.images)):
                if data.images[i].pageNum == data.leftPage and data.images[i].inImage(event.x, event.y):
                    data.focusImage = i
                    data.focusBox = None

        if data.draw == True and event.x < data.buttMenu:
            data.oldXY.append([event.x, event.y, data.leftPage])
        
        for i in range(len(data.textBoxes)):
            if data.textBoxes[i].page == data.leftPage:
                data.textBoxes[i].moveBoxPress(event.x, event.y)
        for i in range(len(data.images)):
            if data.images[i].pageNum == data.leftPage:
                data.images[i].moveImagePress(event.x, event.y)

 
def rightMousePressed(event, data):
    if event.x < data.buttMenu:
        for i in range(len(data.textBoxes)):
            if data.textBoxes[i].page == data.leftPage:
                data.textBoxes[i].editText(event.x, event.y, data.textBoxes[i].typedText, i, data) 
        for i in range(len(data.presetPage)):
            if data.leftPage == data.presetPage[i].pNL:
                data.presetPage[i].editText(event.x, event.y, data.presetPage[i].typedText, i, data)


def keyPressed(event, data):
    if data.resize == True:
        if event.keysym == "Right":
            if data.focusBox != None:
                data.textBoxes[data.focusBox].x1 += 5
            if data.focusImage != None:
                data.images[data.focusImage].resizeImage(5, 0)
                
        if event.keysym == "Left":
            if data.focusBox != None:
                data.textBoxes[data.focusBox].x1 -= 5
            if data.focusImage != None:
                data.images[data.focusImage].resizeImage(-5, 0)
                
        if event.keysym == "Up":
            if data.focusBox != None:
                data.textBoxes[data.focusBox].y1 -= 5
            if data.focusImage != None:
                data.images[data.focusImage].resizeImage(0, -5)
                
        if event.keysym == "Down":
            if data.focusBox != None:
                data.textBoxes[data.focusBox].y1 += 5
            if data.focusImage != None:
                data.images[data.focusImage].resizeImage(0, 5)
                
        if event.keysym == "BackSpace":
            if data.focusBox != None:
                data.textBoxes.pop(data.focusBox)
            if data.focusImage != None:
                data.images.pop(data.focusImage)

    
def mouseMoved(event, data):
    for i in range(len(data.textBoxes)):
        if data.textBoxes[i].page == data.leftPage:
            data.textBoxes[i].moveTextBox(event.x, event.y)
    for i in range(len(data.images)):
        if data.images[i].pageNum == data.leftPage:
            data.images[i].moveImage(event.x, event.y)
            
    if data.draw == True and event.x < data.buttMenu:
        data.oldXY.append([event.x, event.y, data.leftPage])
            
def mouseReleased(event, data):
    if data.start == False:
        if event.x < data.width-(data.buttMarg + data.buttWidth):
            if len(data.textBoxDims) > 0 and data.drawTextBox == True and len(data.textBoxDims[-1]) == 2:
                data.textBoxDims[-1].extend([event.x, event.y])
                data.textBoxes.append(tb.TextBox(data.textBoxDims[-1], data))
                data.drawTextBox = False
                data.options[0].color = data.optColor
        if data.draw == True and event.x < data.buttMenu:
            data.oldXY.append(["", ""])


def timerFired(data):
    pass


def redrawAll(canvas, data):
    if data.start == True: #front page
        canvas.create_rectangle(0,0,data.width,data.height, fill=data.menuBack, width=0)
        canvas.create_text(data.width/2, data.height/3, text="MY JOURNAL", font=("Segoe Script", 50, "bold"))#font="Segoe Script " + str(50) + " bold")
        canvas.create_text(data.width/2, data.height/2, text="press open to begin!", font=("Segoe Script", 25))
        canvas.create_rectangle(data.width/2-100, data.height*2/3-50, data.width/2+100, data.height*2/3+50, fill=data.menuButton)
        canvas.create_text(data.width/2, data.height*2/3, text="OPEN :)", font=("Segoe Script", 30))
        
        data.categoryButt.draw(canvas)
        
        
        
    if data.start == False:
        startX = data.width-data.buttMarg-data.buttWidth
        endX = data.width-data.buttMarg
        canvas.create_line(startX-data.buttMarg, 0, startX-data.buttMarg, data.height)
        canvas.create_rectangle(data.buttMenu, 0, data.width, data.height, fill="#e5db4b")
        
        for i in range(len(data.linedPages)):
            for j in range(len(data.linedPages[i])):
                if data.linedPages[i][j][4] == data.leftPage:
                    x0 = data.linedPages[i][j][0]
                    y0 = data.linedPages[i][j][1]
                    x1 = data.linedPages[i][j][2]
                    y1 = data.linedPages[i][j][3]
                    canvas.create_line(x0, y0, x1, y1)       
        
        for i in range(len(data.dottedPages)):
            for j in range(len(data.dottedPages[i])):
                if data.dottedPages[i][j][4] == data.leftPage:
                    x0 = data.dottedPages[i][j][0]
                    y0 = data.dottedPages[i][j][1]
                    x1 = data.dottedPages[i][j][2]
                    y1 = data.dottedPages[i][j][3]
                    canvas.create_oval(x0, y0, x1, y1, fill="black")    
        
        for i in range(len(data.options)):
            data.options[i].draw(canvas)
            
        
        
        data.leftArrow.draw(canvas)
        data.rightArrow.draw(canvas)
        data.home.draw(canvas)
 
        

        for page in data.page:
            if page.pNL == data.leftPage:
                page.draw(canvas, data)                
                
    for i in range(len(data.textBoxes)):
        if data.textBoxes[i].page == data.leftPage:
            elem = data.textBoxDims[i]
            if len(data.textBoxDims[i]) == 4:
                data.textBoxes[i].draw(canvas, data)

        if len(data.textBoxDims[i]) == 4:
            if data.sort != None:
                if data.textBoxes[i].categoryName == data.sort.corrCateg:
                    data.textBoxes[i].typedText += ("\n" + data.sort.orgText)
                    if data.sort.corrDate == None:
                        data.sort = None
                    
    for i in range(len(data.presetPage)):
        if data.leftPage == data.presetPage[i].pNL:
            if data.sort != None and data.presetPage[i].typedText == data.sort.corrDate and data.presetPage[i].month == data.sort.corrMonth:
                data.presetPage[i].typedText += ("\n" + data.sort.dateStuff)
                data.sort = None
            if data.presetPage[i].presetText == data.today and data.presetPage[i].month == data.month:
                data.presetPage[i].boxColor = (None, data.optColor)
            if data.sort != None and data.sort.corrCateg == data.presetPage[i].categoryName:
                data.presetPage[i].typedText += ("\n" + data.sort.orgText)
                data.sort = None
            data.presetPage[i].draw(canvas, data)
            
    for i in range(len(data.images)):
        if data.leftPage == data.images[i].pageNum:
            data.images[i].draw(canvas, data)
            
    if len(data.oldXY) >= 2:
        for i in range(1, len(data.oldXY)):
            if data.oldXY[i] == ["", ""] or data.oldXY[i-1] == ["", ""]:
                continue
            if data.oldXY[i][2] == data.leftPage and data.oldXY[i-1][2] == data.leftPage:
                canvas.create_line(data.oldXY[i-1][0], data.oldXY[i-1][1], data.oldXY[i][0], data.oldXY[i][1], width=5, capstyle=ROUND, smooth=True)
                    

### Menu stuff
#function from 112 course notes
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
#information detailing widget capabilities from http://effbot.org/tkinterbook/menu.htmE
class MakeMenus(object):
    def __init__(self, menubar, data):
        self.menubar = menubar
        self.drawMenu(data)
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
    def drawMenu(self, data):
        fileMenu = Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label="Save", command=lambda:self.save(data))
        
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        presetMenu = Menu(self.menubar, tearoff=0)
        presetMenu.add_command(label="Daily Spread", command=lambda:self.daily(data, 1, 1, "meh"))
        
        monthMenu = Menu(self.menubar, tearoff=0)
        monthMenu.add_command(label=months[0], command=lambda:self.calendar(data, 31, 2, months[0]))
        monthMenu.add_command(label=months[1], command=lambda:self.calendar(data, 28, 5, months[1]))
        monthMenu.add_command(label=months[2], command=lambda:self.calendar(data, 31, 5, months[2]))
        monthMenu.add_command(label=months[3], command=lambda:self.calendar(data, 30, 1, months[3]))
        monthMenu.add_command(label=months[4], command=lambda:self.calendar(data, 31, 3, months[4]))
        monthMenu.add_command(label=months[5], command=lambda:self.calendar(data, 30, 6, months[5]))
        monthMenu.add_command(label=months[6], command=lambda:self.calendar(data, 31, 1, months[6]))
        monthMenu.add_command(label=months[7], command=lambda:self.calendar(data, 31, 4, months[7]))
        monthMenu.add_command(label=months[8], command=lambda:self.calendar(data, 30, 0, months[8]))
        monthMenu.add_command(label=months[9], command=lambda:self.calendar(data, 31, 2, months[9]))
        monthMenu.add_command(label=months[10], command=lambda:self.calendar(data, 30, 5, months[10]))
        monthMenu.add_command(label=months[11], command=lambda:self.calendar(data, 31, 0, months[11]))

        presetMenu.add_cascade(label="Calendar", menu=monthMenu)
        
        
        insertMenu = Menu(self.menubar, tearoff=0)
        insertMenu.add_command(label="Lined Paper", command=lambda:self.lined(data))
        insertMenu.add_command(label="Dotted Paper", command=lambda:self.dotted(data))
        insertMenu.add_command(label="Blank Paper", command=lambda:self.blank(data))
        insertMenu.add_cascade(label="Preset Design", menu=presetMenu)

        #menubar options    
        self.menubar.add_cascade(label="File", menu=fileMenu)
        self.menubar.add_cascade(label="Insert", menu=insertMenu)

    def calendar(self, data, dates, day, month):
        for elem in [pg.calendarDims(data, dates, day, month)]:
            for dim in elem:
                data.presetPage.append(pg.PresetTB(data.leftPage, data.rightPage, dim, str(self.months.index(month))))
                
    def daily(self, data, dates, day, month):
        for elem in [pg.dailyDims(data, dates, day, month)]:
            for dim in elem:
                data.presetPage.append(pg.PresetTB(data.leftPage, data.rightPage, dim, "meh"))    
    
    def lined(self, data):
        data.linedPages.append(pg.linedPages(data))

    def dotted(self, data):
        data.dottedPages.append(pg.dotPage(data))
        
    def blank(self, data):
        if data.linedPages != []:
            for i in range(len(data.linedPages)):
                for j in range(len(data.linedPages[i])):
                    if data.linedPages[i][j][4] == data.leftPage:
                        data.linedPages.remove(data.linedPages[i])
                        break
                break
        if data.dottedPages != []:
            for i in range(len(data.dottedPages)):
                for j in range(len(data.dottedPages[i])):
                    if data.dottedPages[i][j][4] == data.leftPage:
                        data.dottedPages.remove(data.dottedPages[i])
                        break
                break
                
# save file dialog information from https://pythonspot.com/tk-file-dialogs/
# saving algorithm based on https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html#undoRedoDemo               
    def save(self, data):
        s = ""
        s += sav.saveFile(data.textBoxes, 1) + "\n"
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        file.write(s)
        file.close()
        
####################################
# the bulk of this run funtion is from 112 course notes
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
        
    def mouseMovedWrapper(event, canvas, data):
        mouseMoved(event, data)
        redrawAllWrapper(canvas, data)
        
    def mouseReleasedWrapper(event, canvas, data):
        mouseReleased(event, data)
        redrawAllWrapper(canvas, data)
        
    def rightMousePressedWrapper(event, canvas, data):
        rightMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    
    # menu details/methods from http://effbot.org/tkinterbook/menu.htm
    menubar = Menu(root)
    MakeMenus(menubar, data)
    root.config(menu=menubar)
    
    
    # set up events, buttons from https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event: mouseMovedWrapper(event, canvas, data))
    root.bind("<ButtonRelease-1>", lambda event: mouseReleasedWrapper(event, canvas, data))
    root.bind("<ButtonRelease-3>", lambda event: rightMousePressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
        
    
    # and launch the app
    root.mainloop()  # blocks until window is closed
    
    print("bye!")


def start():
    run(1160, 800)
    
start()
