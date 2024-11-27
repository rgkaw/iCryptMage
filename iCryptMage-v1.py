
from tkinter import CENTER, Frame, filedialog, Tk,END, Button, Text,Label,Entry,Canvas
from tkinter import messagebox
# import numpy as npss
from numpy import ubyte,bitwise_xor
from cv2 import imread,imwrite,hconcat,vconcat,resize,INTER_AREA,split,merge
from PIL import Image, ImageTk
from keyStream import keyStream
from os import getcwd
from time import time


win = Tk()
win.title("iCryptMage - Aplikasi Enkripsi-Dekripsi Gambar")
win.resizable(False,False)
win.configure(bg='#ffffff')
win.attributes('-alpha', 0.98)
win.iconbitmap("icon.ico")
size=[565,420]
win.geometry(str(size[0])+"x"+str(size[1]))
fileSelected=False

classicStyle=Frame(win)
mainMenu=Frame(win)
howtoMenu=Frame(win)
aboutMenu=Frame(win)

def select_file():
    classicStyle.task.config(text='Loading Image')
    filetypes=(
        ('image files', '*.jpeg *.jpg *.png'),
        ('All files','*.*')
    )
    filename = filedialog.askopenfilename(
        title ="Open file",
        initialdir=getcwd(),
        filetypes=filetypes
    )
    if filename!="":
        dim=imread(filename).shape[:2]
        if dim[0]<256 or dim[1]<256:
            messagebox.showerror(title="Open file error",message="File must bigger than 256x256 pixel in width and height")
            return
        if dim[0]>1080 or dim[1]>1920:
            messagebox.showerror(title="Open file error",message="File must smaller than 1920x1080 pixel in width and height")
            return
        classicStyle.filePath.delete('1.0',END)
        classicStyle.filePath.insert(END,filename)
        loadImage("input",filename)
    classicStyle.task.config(text='Idle')
def save_file():
    classicStyle.task.config(text='Saving Image')
    f=filedialog.asksaveasfile(mode='w',defaultextension='.png',filetypes=[('PNG','*.png'),('JPEG','*.jpg')])
    if f is None:
        return
    imwrite(f.name,b)
    classicStyle.task.config(text='Idle')
def encrypt():

    classicStyle.task.config(text='Encrypting Image')
    classicStyle.update()
    start=time()
    if fileSelected==False:
        classicStyle.task.config(text='Idle')
        return
    path=fileLoc
    img=imread(path)
    img=ubyte(img)
    global key1,key2,limit1,limit2,height,width,channel,b
    height,width,channel=img.shape
    key1,key2,limit1,limit2=keyStream(classicStyle.passwordEntry.get(),height,width)
    b=img
    b=cipher(key1,b)
    b=block_swap(key2,b)
    end=time()
    with open('00-3-iCryptMage-total-time.txt','a') as file:
        file.write(str(end-start)+'\n')
    loadImage("output",b)
    classicStyle.spd.config(text=str(float("{0:.3f}".format(end-start)))+" s")
    classicStyle.task.config(text='Idle')
def decrypt():
    classicStyle.task.config(text='Decrypting Image')
    classicStyle.update()
    start=time()
    if fileSelected==False:
        classicStyle.task.config(text='Idle')
        return
    path=fileLoc
    img=imread(path)
    img=ubyte(img)
    global key1,key2,limit1,limit2,height,width,channel,b
    height,width,channel=img.shape
    key1,key2,limit1,limit2=keyStream(classicStyle.passwordEntry.get(),height,width)
    b=img
    b=block_deswap(key2,b)
    b=cipher(key1,b)
    end=time()
    loadImage("output",b)
    classicStyle.spd.config(text=str(float("{0:.3f}".format(end-start)))+" s")
    classicStyle.task.config(text='Idle')


def cipher(keystream,b):
    start=time()
    b=bitwise_xor(b,keystream)
    end=time()
    return b
def block_swap(keystream,b):
    start=time()
    color_map=keystream
    for i in range(len(keystream)):
        while(keystream[i]>=(limit1*limit2)):
            keystream[i]=keystream[i]-(limit1*limit2)
    blocks=[]
    side=b[0:limit1*8,limit2*8:]
    down=b[limit1*8:,0:width]
    for i in range(0,limit1):
        for j in range(0,limit2):
            blocks.append(b[i*8:(i+1)*8,j*8:(j+1)*8])
    for i in range(0,limit1*limit2):
        r=keystream[i]
        g=keystream[r]
        b=keystream[g]
        block_color=ubyte([color_map[r],color_map[g],color_map[b]])
        blocks[i]=blocks[i]+block_color
        blocks[i],blocks[r+g+b+keystream[b]]=blocks[r+g+b+keystream[b]],blocks[i]
    v_image=[]
    for i in range(0,limit1*limit2,limit2):
        h_image=hconcat(blocks[i:i+limit2])
        v_image.append(h_image)
        
    final_image=vconcat(v_image)
    h_final=[final_image,side]
    final_image=hconcat(h_final)
    v_final=[final_image,down]
    final_image=vconcat(v_final)
    end=time()
    return final_image
def block_deswap(keystream,b):
    keystream3=keystream
    for i in range(len(keystream)):
        while(keystream[i]>=(limit1*limit2)):
            keystream[i]=keystream[i]-(limit1*limit2)
    blocks=[]
    side=b[0:limit1*8,limit2*8:]
    down=b[limit1*8:,0:width]
    for i in range(0,limit1):
        for j in range(0,limit2):
            blocks.append(b[i*8:(i+1)*8,j*8:(j+1)*8])
    for i in range((limit1*limit2)-1,-1,-1):
        r=keystream[i]
        g=keystream[r]
        b=keystream[g]
        block_color=ubyte([keystream3[r],keystream3[g],keystream3[b]])
        blocks[i],blocks[r+g+b+keystream[b]]=blocks[r+g+b+keystream[b]],blocks[i]
        blocks[i]=blocks[i]-block_color
    v_image=[]
    for i in range(0,limit1*limit2,limit2):
        h_image=hconcat(blocks[i:i+limit2])
        v_image.append(h_image)
    final_image=vconcat(v_image)
    h_final=[final_image,side]
    final_image=hconcat(h_final)
    v_final=[final_image,down]
    final_image=vconcat(v_final)
    return final_image


def resizeImage(img):
    a,b=img.shape[:2]
    if a>b:
        r=a/256
        d=(int(b/r),256)
    else:
        r=b/256
        d=(256,int(a/r))
    return (resize(img,d,interpolation=INTER_AREA))
def loadImage(param,param2):
    if param==("input"):
        
        im=imread(param2)
        if im.shape[:2]!=(256,256):
            im=resizeImage(im)
        b,g,r=split(im)
        img=merge((r,g,b))
        img=Image.fromarray(img)
        inputImage= ImageTk.PhotoImage(img)
        classicStyle.inputImageLabel.configure(image=inputImage)
        classicStyle.inputImageLabel.image=inputImage
    if param==("output"):
        im=param2
        if im.shape[:2]!=(256,256):
            im=resizeImage(im)
        b,g,r=split(im)
        img=merge((r,g,b))
        img=Image.fromarray(img)
        outputImage= ImageTk.PhotoImage(img)
        classicStyle.outputImageLabel.configure(image=outputImage)
        classicStyle.outputImageLabel.configure()
        classicStyle.outputImageLabel.image=outputImage
    

def clearField():
    classicStyle.passwordEntry.delete('0',END)       


def callClassicStyle():
    mainMenu.forget()
    howtoMenu.forget()
    classicStyle.openButton = Button(classicStyle, text='Open File', command=select_file)
    classicStyle.encryptButton = Button(classicStyle, text='Encrypt', command=encrypt,height=2)
    classicStyle.decryptButton = Button(classicStyle,text='Decrypt', command=decrypt,height=2)
    classicStyle.saveButton=Button(classicStyle,text='Save file',command=save_file)
    classicStyle.clearButton=Button(classicStyle,text='Clear pass',command=clearField)
    classicStyle.img=Image.open('blank.png')
    classicStyle.inputImage= ImageTk.PhotoImage(classicStyle.img.resize((256,256)))
    classicStyle.img2=Image.open('blank.png')
    classicStyle.outputImage= ImageTk.PhotoImage(classicStyle.img2.resize((256,256)))
    classicStyle.filePath=Text(classicStyle,height=1,width=30,borderwidth=2)
    classicStyle.passwordEntry=Entry(classicStyle,show='●',width=25,borderwidth=2)
    classicStyle.directoryLabel = Label(classicStyle,text="File Directory",bg='white')
    classicStyle.passwordlabel = Label(classicStyle,text='Password',bg='white')
    classicStyle.inputImageLabel=Label(classicStyle,image=classicStyle.inputImage)
    classicStyle.inputImageTextLabel=Label(classicStyle,text="gambar input",bg='white')
    classicStyle.outputImageLabel=Label(classicStyle,image=classicStyle.outputImage)
    classicStyle.outputImageTextLabel=Label(classicStyle,text="gambar output",bg='white')
    classicStyle.cprLabel=Label(classicStyle,text="Rgkaw - 2022",bg='white')

    classicStyle.inputImageTextLabel.place(x=int((10+256)/2)-30,y=size[1]-304)
    classicStyle.inputImageLabel.place(in_=classicStyle.inputImageTextLabel,rely=0.5, x=-94,y=10)
    classicStyle.outputImageTextLabel.place(x=int((10+256)/2)+286-30,y=size[1]-304)
    classicStyle.outputImageLabel.place(in_=classicStyle.outputImageTextLabel,rely=0.5, x=-94,y=10)
    classicStyle.outputImageLabel.lift()
    classicStyle.clearButton.place(in_=classicStyle.openButton,x=-7,y=30)

    classicStyle.directoryLabel.place(x=110,y=10)
    classicStyle.filePath.place(in_=classicStyle.directoryLabel,x=100,)
    classicStyle.passwordlabel.place(in_=classicStyle.directoryLabel,y=30,x=-2)
    classicStyle.passwordEntry.place(in_=classicStyle.passwordlabel,x=100)
    classicStyle.openButton.place(x=490,y=7)
    classicStyle.encryptButton.place(x=210,y=80)
    classicStyle.decryptButton.place(in_=classicStyle.encryptButton,x=60,y=-4)
    classicStyle.saveButton.place(in_=classicStyle.clearButton,x=2,y=30)
    classicStyle.cprLabel.place(x=size[0]-90,y=size[1]-24)
    classicStyle.task=Label(classicStyle,text='Idle',bg='white')
    classicStyle.task.place(y=size[1]-24,x=10)

    classicStyle.spdLabel=Label(classicStyle,text='Speed :',bg='white')
    classicStyle.spdLabel.place(x=150,y=size[1]-24)
    classicStyle.spd=Label(classicStyle,text='0 s',bg='white')
    classicStyle.spd.place(in_=classicStyle.spdLabel,x=45,y=-2)
    classicStyle.logo=Image.open("icon.png")
    classicStyle.logo_image= ImageTk.PhotoImage(classicStyle.logo.resize((100,100)))

    classicStyle.pack(fill="both", expand=True)
    classicStyle.configure(bg='white')
    classicStyle.logoLabel=Label(classicStyle,image=classicStyle.logo_image,bg='white')
    classicStyle.logoLabel.place(x=5,y=15)
    classicStyle.but1=Button(text='Help',command=howToUse,height=2)
    classicStyle.but1.place(in_=classicStyle.decryptButton,x=50,y=-4)
    classicStyle.pack(fill='both',expand=True)
text1="Welcome to iCryptMage!! click 'Encrypt' button to start encrypting/decrypting!"
def about():
    messagebox.showinfo(message='Aplikasi Enkripsi-Dekripsi Gambar iCrypt-Mage \nRGKAW - 2022',title='About')
def changeToMainMenu():
    None
def howToUse():
    classicStyle.forget()
    mainMenu.forget()
    howtoMenu.configure(bg='white')
    howtoMenu.lab1=Label(howtoMenu,text="1. open 'Encrypt!' menu",bg='white').pack(ipady=10)
    howtoMenu.lab2=Label(howtoMenu,text="2. open image with 'open file' button",bg='white').pack(ipady=10)
    howtoMenu.lab3=Label(howtoMenu,text="3. insert password to encrypt image",bg='white').pack(ipady=10)
    howtoMenu.lab4=Label(howtoMenu,text="4. click 'Encrypt' to encrypt, or 'Decrypt' to decrypt image",bg='white').pack(ipady=10)
    howtoMenu.lab5=Label(howtoMenu,text="5. click 'save file' to save the result",bg='white').pack(ipady=10)
    howtoMenu.but1=Button(howtoMenu,text='Menu',command=callMainMenu,width=25,height=4).pack(ipady=10)
    howtoMenu.but2=Button(howtoMenu,text='Encrypt!',command=callClassicStyle,width=25,height=4,bg='green').pack(ipady=10)
    howtoMenu.pack(fill='y',expand=True)
def callMainMenu():
    howtoMenu.forget()
    classicStyle.forget()
    mainMenu.configure(bg='white')
    mainMenu.logo=Image.open("icon.png")
    mainMenu.logo_image= ImageTk.PhotoImage(mainMenu.logo.resize((128,128)))
    mainMenu.labi=Label(mainMenu,image=mainMenu.logo_image,bg='white')
    mainMenu.cred=Label(mainMenu,text='by : Rgkaw',anchor='e',justify=CENTER,font=(20),bg='white')
    mainMenu.lab1=Label(mainMenu,text=text1,anchor='e',justify=CENTER,font=(20),bg='white')
    mainMenu.but1=Button(mainMenu,text='Encrypt/Decrypt!',command=callClassicStyle,font=('lucida 12 bold'),borderwidth=2,bg='green')
    mainMenu.but2=Button(mainMenu,text='How to Use',command=howToUse,font=('lucida 12 bold'),borderwidth=2,bg='cyan')
    mainMenu.but3=Button(mainMenu,text='About',command=about,font=('lucida 12 bold'),borderwidth=2,bg='yellow')
    mainMenu.but4=Button(mainMenu,text='Exit',command=win.destroy,font=('lucida 12 bold'),borderwidth=2,bg='red')
    mainMenu.but1.configure(width=23,height=3)
    mainMenu.but2.configure(width=23,height=3)
    mainMenu.but3.configure(width=23,height=3)
    mainMenu.but4.configure(width=23,height=3)
    mainMenu.cred.place(x=225,y=150)
    mainMenu.labi.place(x=200,y=10)
    mainMenu.lab1.place(x=17,y=180)
    mainMenu.but1.place(x=40,y=210)
    mainMenu.but2.place(x=288,y=210)
    #mainMenu.but3.place(x=164,y=300)
    mainMenu.but3.place(x=40,y=300)
    mainMenu.but4.place(x=288,y=300)
    mainMenu.pack(fill='both',expand=True)


#main menu


#main loop
callMainMenu()
win.mainloop()