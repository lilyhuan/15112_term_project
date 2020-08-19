#file for image editing and all things image insertion related
from tkinter import *
from PIL import Image, ImageTk

#image information from https://www.kaggle.com/saxinou/nlp-02-categorizing-and-tagging-words
#resizing information from https://stackoverflow.com/questions/4066202/resizing-pictures-in-pil-in-tkinter
#debug help with images from https://stackoverflow.com/questions/13148975/tkinter-label-does-not-show-image
#more image information https://pillow.readthedocs.io/en/5.1.x/reference/ImageTk.html

class ImageInsert(object):
    def __init__(self, path, pageNum):
        self.image = Image.open(path)
        self.tkImage = ImageTk.PhotoImage(image=self.image)
        self.pageNum = pageNum
        self.x = 500
        self.y = 400
        self.width = self.tkImage.width()
        self.height = self.tkImage.height()
        self.x0 = self.x - self.width/2
        self.y0 = self.y - self.height/2
        self.x1 = self.x + self.width/2
        self.y1 = self.y + self.height/2

    def draw(self, canvas, data):
        canvas.create_image(self.x, self.y, image=self.tkImage)

    def inImage(self, x, y):
        if x < self.x1 and x > self.x0 and y < self.y1 and y > self.y0:
            return True
        return False

    def moveImagePress(self, x, y):
        if self.inImage(x, y):
            self.moveImageX = x
            self.moveImageY = y

    def moveImage(self, x, y):
        if self.inImage(x, y):
            dx = self.moveImageX - self.x0
            self.x0 = x - dx
            self.x1 = self.x0 + self.width
            self.x = (self.x0 + self.x1)/2

            dy = self.moveImageY - self.y0
            self.y0 = y - dy
            self.y1 = self.y0 + self.height
            self.y = (self.y0 + self.y1)/2

            self.moveImageX = x
            self.moveImageY = y

    def resizeImage(self, dx, dy):
        self.tkImage = ImageTk.PhotoImage(image=self.image.resize((self.width+dx, self.height+dy)))
        self.width = self.tkImage.width()
        self.height = self.tkImage.height()

        self.x0 = self.x - self.width/2
        self.y0 = self.y - self.height/2
        self.x1 = self.x + self.width/2
        self.y1 = self.y + self.height/2
