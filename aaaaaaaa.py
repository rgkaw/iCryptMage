import tkinter

win = tkinter.Tk()
win.title("iCryptMage - Aplikasi Enkripsi-Dekripsi Gambar")
win.resizable(False,False)
win.configure(bg='#ffffff')
win.attributes('-alpha', 0.98)
size=[565,420]
win.geometry(str(size[0])+"x"+str(size[1]))

frame=tkinter.Frame(win)
lab = tkinter.Label(frame, text="hiiii")
lab.place(x=20,y=20)
frame.pack(fill="both", expand=True)
win.mainloop()