
from tkinter import filedialog, Tk,END, Button, Text,Label,Entry,Canvas
from tkinter import messagebox
# import numpy as npss
from numpy import ubyte,bitwise_xor
from cv2 import imread,imwrite,hconcat,vconcat,resize,INTER_AREA,split,merge
from PIL import Image, ImageTk
from keyStream import keyStream
from os import getcwd
from time import time


win = Tk()
win.title("CryptMage - Aplikasi Enkripsi-Dekripsi Gambar")
win.resizable(False,False)
win.configure(bg='#ffffff')
win.attributes('-alpha', 0.98)
win.iconbitmap("icon.png")
size=[565,420]
win.geometry(str(size[0])+"x"+str(size[1]))
fileSelected=False


#opening file
def select_file():
    task.config(text='Loading Image')
    filetypes=(
        ('image files', '*.jpeg *.jpg *.png'),
        ('All files','*.*')
    )
    filename = filedialog.askopenfilename(
        title ="Open file",
        initialdir=getcwd(),
        filetypes=filetypes
    )
    print(type(filename))
    if filename!="":
        dim=imread(filename).shape[:2]
        if dim[0]<256 or dim[1]<256:
            messagebox.showerror(title="Open file error",message="File must bigger than 256x256 pixel in width and height")
            return
        if dim[0]>1080 or dim[1]>1920:
            messagebox.showerror(title="Open file error",message="File must smaller than 1920x1080 pixel in width and height")
            return
        filePath.delete('1.0',END)
        filePath.insert(END,filename)
        loadImage("input",filename)
        global fileLoc
        fileLoc=filename
        global fileSelected
        fileSelected=True
    task.config(text='Idle')
def save_file():
    task.config(text='Saving Image')
    f=filedialog.asksaveasfile(mode='w',defaultextension='.png',filetypes=[('PNG','*.png'),('JPEG','*.jpg')])
    if f is None:
        return
    imwrite(f.name,b)
    task.config(text='Idle')
def encrypt():
    task.config(text='Encrypting Image')
    win.update()
    start=time()
    if fileSelected==False:
        task.config(text='Idle')
        return
    path=fileLoc
    #path.encode('unicode_escape')
    img=imread(path)
    img=ubyte(img)
    global key1,key2,limit1,limit2,height,width,channel,b
    height,width,channel=img.shape
    key1,key2,limit1,limit2=keyStream(passwordEntry.get(),height,width)
    b=img
    b=cipher(key1,b)
    b=block_swap(key2,b)
    end=time()
    print(end-start)
    loadImage("output",b)
    spd.config(text=str(float("{0:.3f}".format(end-start)))+" s")
    task.config(text='Idle')
def decrypt():
    task.config(text='Decrypting Image')
    win.update()
    start=time()
    if fileSelected==False:
        task.config(text='Idle')
        return
    path=fileLoc
    #path.encode('unicode_escape')
    img=imread(path)
    img=ubyte(img)
    global key1,key2,limit1,limit2,height,width,channel,b
    height,width,channel=img.shape
    key1,key2,limit1,limit2=keyStream(passwordEntry.get(),height,width)
    b=img
    b=block_deswap(key2,b)
    b=cipher(key1,b)
    end=time()
    loadImage("output",b)
    spd.config(text=str(float("{0:.3f}".format(end-start)))+" s")
    task.config(text='Idle')


def cipher(keystream,b):
    start=time()
    b=bitwise_xor(b,keystream)
    end=time()
    print('cipher: ',end-start)
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
        inputImageLabel.configure(image=inputImage)
        inputImageLabel.image=inputImage
    if param==("output"):
        im=param2
        if im.shape[:2]!=(256,256):
            im=resizeImage(im)
        b,g,r=split(im)
        img=merge((r,g,b))
        img=Image.fromarray(img)
        outputImage= ImageTk.PhotoImage(img)
        outputImageLabel.configure(image=outputImage)
        outputImageLabel.configure()
        outputImageLabel.image=outputImage
    

def clearField():
    passwordEntry.delete('1.0',END)       
        
pwd=getcwd()


openButton = Button(win, text='Open File', command=select_file)
encryptButton = Button(win, text='Encrypt', command=encrypt)
decryptButton = Button(win,text='Decrypt', command=decrypt)
saveButton=Button(win,text='Save file',command=save_file)
clearButton=Button(win,text='Clear pass',command=clearField)
img=Image.open('blank.png')
inputImage= ImageTk.PhotoImage(img.resize((256,256)))
img2=Image.open('blank.png')
outputImage= ImageTk.PhotoImage(img2.resize((256,256)))


filePath=Text(win,height=1,width=30,borderwidth=2)
passwordEntry=Entry(win,show='●',width=25,borderwidth=2)
directoryLabel = Label(win,text="File Directory",bg='white')
passwordlabel = Label(win,text='Password',bg='white')
inputImageLabel=Label(win,image=inputImage)
inputImageTextLabel=Label(win,text="gambar input",bg='white')
outputImageLabel=Label(win,image=outputImage)
outputImageTextLabel=Label(win,text="gambar output",bg='white')
cprLabel=Label(win,text="Rgkaw - 2022",bg='white')

inputImageTextLabel.place(x=int((10+256)/2)-30,y=size[1]-304)
inputImageLabel.place(in_=inputImageTextLabel,rely=0.5, x=-94,y=10)
outputImageTextLabel.place(x=int((10+256)/2)+286-30,y=size[1]-304)
outputImageLabel.place(in_=outputImageTextLabel,rely=0.5, x=-94,y=10)
outputImageLabel.lift()
clearButton.place(in_=openButton,x=-7,y=30)

directoryLabel.place(x=110,y=10)
filePath.place(in_=directoryLabel,x=100,)
passwordlabel.place(in_=directoryLabel,y=30,x=-2)
passwordEntry.place(in_=passwordlabel,x=100)
openButton.place(x=490,y=7)
encryptButton.place(x=110,y=80)
decryptButton.place(in_=encryptButton,x=60,y=-4)
saveButton.place(in_=clearButton,x=2,y=30)
cprLabel.place(x=size[0]-90,y=size[1]-24)
task=Label(win,text='Idle',bg='white')
task.place(y=size[1]-24,x=10)

spdLabel=Label(win,text='Speed :',bg='white')
spdLabel.place(x=150,y=size[1]-24)
spd=Label(win,text='0  s',bg='white')
spd.place(in_=spdLabel,x=45,y=-2)
logo=Image.open("icon.png")
logo_image= ImageTk.PhotoImage(logo.resize((100,100)))
logoLabel=Label(win,image=logo_image,bg='white')
logoLabel.place(x=5,y=15)

win.mainloop()