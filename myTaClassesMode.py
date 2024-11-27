from ctypes import alignment
from email import message
from fileinput import filename
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import cv2
from PIL import Image, ImageTk
import xxhash
import sys
from keyStream import keyStream
from os import getcwd



#opening file
class App(Tk):
    size=[565,400]
    def __init__(self):
        super().__init__()
        self.title("judul program")
        self.resizable(False,False)
        size=[565,400]
        self.geometry(str(size[0])+"x"+str(size[1]))
        self.title("judul program")
        self.resizable(False,False)
        self.geometry(str(size[0])+"x"+str(size[1]))
        self.openButton = Button(self, text='Open File', command=self.select_file)
        self.encryptButton = Button(self, text='Encrypt', command=self.encrypt)
        self.decryptButton = Button(self,text='Decrypt', command=self.decrypt)
        self.saveButton=Button(self,text='Save file',command=self.save_file)
        self.img=Image.open('blank.png')
        self.inputImage= ImageTk.PhotoImage(self.img.resize((256,256)))
        self.img2=Image.open('blank.png')
        self.outputImage= ImageTk.PhotoImage(self.img2.resize((256,256)))


        self.filePath=Text(self,height=1,width=45,)
        self.passwordEntry=Entry(self,show='*',width=25)
        self.directoryLabel = Label(self,text="File Directory")
        self.passwordlabel = Label(self,text='Password')
        self.inputImageLabel=Label(self,image=self.inputImage)
        self.inputImageTextLabel=Label(self,text="gambar input")
        self.outputImageLabel=Label(self,image=self.outputImage)
        self.outputImageTextLabel=Label(self,text="gambar output")

        self.inputImageTextLabel.place(x=int((10+256)/2)-30,y=size[1]-286)
        self.inputImageLabel.place(in_=self.inputImageTextLabel,rely=0.5, x=-94,y=10)

        self.outputImageTextLabel.place(x=int((10+256)/2)+286-30,y=size[1]-286)
        self.outputImageLabel.place(in_=self.outputImageTextLabel,rely=0.5, x=-94,y=10)

        self.directoryLabel.place(x=10,y=10)
        self.filePath.place(x=120,y=10)
        self.passwordlabel.place(x=10,y=40)
        self.passwordEntry.place(x=120,y=40)
        self.openButton.place(x=490,y=7)
        self.encryptButton.place(x=10,y=70)
        self.decryptButton.place(x=70,y=70)
        self.saveButton.place(in_=self.decryptButton,relx=1.0,x=380,y=-5)
        self.canvas=Canvas(self,bg="blue",height=300,width=300)
        self.passwordEntryyy=Entry(self.canvas,show='*',width=10)

    def select_file(self):
        filetypes=(
            ('image files', '*.jpg *.png'),
            ('All files','*.*')
        )
        filename = filedialog.askopenfilename(
            title ="Open file",
            initialdir=getcwd(),
            filetypes=filetypes
        )
        print(type(filename))
        if filename!="":
            self.filePath.insert(END,filename)
            self.loadImage("input",filename)
            global fileLoc
            fileLoc=filename
    def save_file(self):
        f=filedialog.asksaveasfile(mode='w',defaultextension='.png',filetypes=[('Image files','*.png *jpg')])
        print(f)
        print(f.name)
        if f is None:
            return
        cv2.imwrite(f.name,b)
    def encrypt(self):
        path=fileLoc
        #path.encode('unicode_escape')
        img=cv2.imread(path)
        img=np.ubyte(img)
        global key1,key2,limit1,limit2,height,width,channel,b
        height,width,channel=img.shape
        key1,key2,limit1,limit2=keyStream(self.passwordEntry.get(),height,width)
        b=img
        print(b)
        self.cipher(key1,b)
        b=self.block_swap(key2,b)
        self.loadImage("output",b)
    def decrypt(self):
        path=fileLoc
        #path.encode('unicode_escape')
        img=cv2.imread(path)
        img=np.ubyte(img)
        global key1,key2,limit1,limit2,height,width,channel,b
        height,width,channel=img.shape
        key1,key2,limit1,limit2=keyStream(self.passwordEntry.get(),height,width)
        b=img
        b=self.block_deswap(key2,b)
        self.cipher(key1,b)
        self.loadImage("output",b)



    def cipher(keystream,b,self):
        for i in range(height):
            for j in range(width):
                    b[i,j]=b[i,j]^keystream[i][j]
    def block_swap(keystream,b,self):
        color_map=keystream
        for i in range(len(keystream)):
            while(keystream[i]>=(limit1*limit2)):
                keystream[i]=keystream[i]-(limit1*limit2)
        print("dividing image")
        blocks=[]
        side=b[0:limit1*16,limit2*16:]
        down=b[limit1*16:,0:width]
        for i in range(0,limit1):
            for j in range(0,limit2):
                blocks.append(b[i*16:(i+1)*16,j*16:(j+1)*16])
        print("scrambling image")
        for i in range(0,limit1*limit2):
            r=keystream[i]
            g=keystream[r]
            b=keystream[g]
            block_color=np.ubyte([color_map[r],color_map[g],color_map[b]])
            blocks[i]=blocks[i]+block_color
            blocks[i],blocks[keystream[i]]=blocks[keystream[i]],blocks[i]
        v_image=[]
        print("rearranging image")
        for i in range(0,limit1*limit2,limit2):
            h_image=cv2.hconcat(blocks[i:i+limit2])
            v_image.append(h_image)
            
        final_image=cv2.vconcat(v_image)
        h_final=[final_image,side]
        final_image=cv2.hconcat(h_final)
        v_final=[final_image,down]
        final_image=cv2.vconcat(v_final)
        return final_image
    def block_deswap(keystream,b):
        keystream3=keystream
        for i in range(len(keystream)):
            while(keystream[i]>=(limit1*limit2)):
                keystream[i]=keystream[i]-(limit1*limit2)
        print("dividing image")
        blocks=[]
        side=b[0:limit1*16,limit2*16:]
        down=b[limit1*16:,0:width]
        for i in range(0,limit1):
            for j in range(0,limit2):
                blocks.append(b[i*16:(i+1)*16,j*16:(j+1)*16])
        print("scrambling image")
        for i in range((limit1*limit2)-1,-1,-1):
            r=keystream[i]
            g=keystream[r]
            b=keystream[g]
            block_color=np.ubyte([keystream3[r],keystream3[g],keystream3[b]])
            blocks[i],blocks[keystream[i]]=blocks[keystream[i]],blocks[i]
            blocks[i]=blocks[i]-block_color
        v_image=[]
        print("rearranging image")
        for i in range(0,limit1*limit2,limit2):
            h_image=cv2.hconcat(blocks[i:i+limit2])
            v_image.append(h_image)
        final_image=cv2.vconcat(v_image)
        h_final=[final_image,side]
        final_image=cv2.hconcat(h_final)
        v_final=[final_image,down]
        final_image=cv2.vconcat(v_final)
        return final_image


    def resizeImage(img):
        a,b=img.shape[:2]
        if a>b:
            r=a/256
            d=(int(b/r),256)
        else:
            r=b/256
            d=(256,int(a/r))
        return (cv2.resize(img,d,interpolation=cv2.INTER_AREA))
    def loadImage(param,param2,self):
        if param==("input"):
            im=cv2.imread(param2)
            if im.shape[:2]!=(256,256):
                im=self.resizeImage(im)
            b,g,r=cv2.split(im)
            img=cv2.merge((r,g,b))
            img=Image.fromarray(img)
            inputImage= ImageTk.PhotoImage(img)
            self.inputImageLabel.configure(image=inputImage)
            self.inputImageLabel.image=inputImage
        if param==("output"):
            im=param2
            if im.shape[:2]!=(256,256):
                im=self.resizeImage(im)
            b,g,r=cv2.split(im)
            img=cv2.merge((r,g,b))
            img=Image.fromarray(img)
            outputImage= ImageTk.PhotoImage(img)
            self.outputImageLabel.configure(image=outputImage)
            self.outputImageLabel.image=outputImage

        
        

#open_button.pack(expand=True)

# im=Image.fromarray(img)
# Imgtk=ImageTk.PhotoImage(image=im)
# Label(self,image=imgtk).pack()
win=App()
win.mainloop()