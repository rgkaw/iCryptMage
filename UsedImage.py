from PIL import Image,ImageTk
class Card:
    def __init__(self, name, imagePath, ImageType, rarity):
        self.name = name
        self.imagePath = imagePath
    def __repr__(self):
        print(self.name)
    def __str__(self):
        return self.name
    def returnImage(self):
        self.timage = Image.open(self.imagePath)
        if not self.timage.size == (212,263):
            self.timage = self.timage.resize((212,263), Image.ANTIALIAS)
        self.tphoto = ImageTk.PhotoImage(self.timage)
        return self.tphoto
    def createLabel(self, parent):
        self.timage = Image.open(self.imagePath)
        if not self.timage.size == (212,263):
            self.timage = self.timage.resize((212,263), Image.ANTIALIAS)
        self.tphoto = ImageTk.PhotoImage(self.timage)
        self.ImageLabel = self.Label(parent, image = self.tphoto)
        self.ImageLabel.image = self.tphoto
        return self.ImageLabel