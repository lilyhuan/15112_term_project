#file for the table of contents (the side window)
from tkinter import *
import pageTP as pg
import textboxEntryTP as tb
'''
Text box information from http://effbot.org/tkinterbook/text.htm
Entry information from http://effbot.org/tkinterbook/entry.htm
Menu design information from http://effbot.org/tkinterbook/menu.htm
Grid/packing information from https://effbot.org/tkinterbook/grid.htm
'''

class SideMenu():
    def __init__(self, master):
        self.master = master
        self.label = Label(self.master, text="table of contents").grid(row=0)
        self.entryList = []
        self.buttList = []
        self.oldCats = []
        self.pageList = []
        self.index = 0
        self.pageNumList = list(range(0,25))
        self.catList = []

    def drawWidgets(self, data):
        i = 1
        for elem in data.categories:
            if elem not in self.catList:
                self.catList.append(elem)
        for elem in data.categories:
            self.entry = Entry(self.master)
            self.entry.grid(row=i, column=0)
            self.entry.insert(END, elem)

            button = Button(self.master, text="skip to page", command=lambda:self.skipPage(data, pageEntry.get()))
            button.grid(row=i, column=4)

            label = Label(self.master, text="on page")
            label.grid(row=i, column=1)

            pageEntry = Entry(self.master)
            pageEntry.grid(row=i, column=2)
            pageEntry.insert(END, str(self.pageNumList[i]))

            buttonSub = Button(self.master, text="update", command=lambda:self.update(data, i))
            buttonSub.grid(row=i, column=3)

            i += 1
        self.index += 1
        self.entryList.append(self.entry)
        self.buttList.append(button)
        self.pageList.append(pageEntry)
        self.oldCats.append(self.entry.get())

        if int(pageEntry.get())%2 == 1:
            box = tb.TextBox([0,0,300,300], data)
            box.page = int(pageEntry.get())
            box.categoryName = self.entry.get()
            data.textBoxes.append(box)
            data.textBoxDims.append([0,0,300,300])
        else:
            xCo = (data.width-data.buttWidth-2*data.buttMarg)/2
            box = tb.TextBox([xCo, 0, xCo+300, 300], data)
            box.page = int(pageEntry.get()) - 1
            box.categoryName = self.entry.get()
            data.textBoxes.append(box)
            data.textBoxDims.append([xCo, 0, xCo+300, 300])

        for p in range(1, int(pageEntry.get())+1, 2):
            if pg.Page(p, p+1) not in data.page:
                data.page.append(pg.Page(p, p+1))

    def createPages(self, data):
        for i in range(self.index, len(self.pageList)):
            page = self.pageList[i].get()
            if int(page)%2 == 1:
                box = tb.TextBox([0,0,300,300], data)
                box.page = int(page)
                box.categoryName = self.entryList[i].get()
                data.textBoxes.append(box)
                data.textBoxDims.append([0,0,300,300])
            else:
                xCo = (data.width-data.buttWidth-2*data.buttMarg)/2
                box = tb.TextBox([xCo, 0, xCo+300, 300], data)
                box.page = int(page) - 1
                box.categoryName = self.entryList[i].get()
                data.textBoxes.append(box)
                data.textBoxDims.append([xCo, 0, xCo+300, 300])
            for p in range(1, int(page)+1, 2):
                if pg.Page(p, p+1) not in data.page:
                    data.page.append(pg.Page(p, p+1))

    def update(self, data, index):
        for i in range(len(self.entryList)):
            for j in range(len(data.textBoxes)):
                if data.textBoxes[j].categoryName == self.oldCats[i]:
                    data.textBoxes[j].categoryName = self.entryList[i].get()
                    pageNum = int(self.pageList[i].get())
                    self.pageNumList[i+1] = pageNum
                    if pageNum%2 == 1:
                        data.textBoxes[j].page = pageNum
                    else:
                        data.textBoxes[j].page = pageNum-1
                    data.categories[i] = self.entryList[i].get()
                    self.oldCats[i] = self.entryList[i].get()

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
