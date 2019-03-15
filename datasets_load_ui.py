import Tkinter as tk
import tkFileDialog
from Tkinter import *
from tkFileDialog   import askopenfilename

#Fullscreen window
root=tk.Tk()
root.title("ART")
root.attributes('-zoomed', True)

#Adding buttons

def callback1():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel1 = Label(root)
    pathlabel1.pack()
    pathlabel1.config(text=filez)
    pathlabel1.place(x = 650, y = 100)
    print root.tk.splitlist(filez)

def callback2():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel2 = Label(root)
    pathlabel2.pack()
    pathlabel2.config(text=filez)
    pathlabel2.place(x = 650, y = 150)
    print root.tk.splitlist(filez)

def callback3():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel3 = Label(root)
    pathlabel3.pack()
    pathlabel3.config(text=filez)
    pathlabel3.place(x = 650, y = 200)
    print root.tk.splitlist(filez)

def callback4():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel4 = Label(root)
    pathlabel4.pack()
    pathlabel4.config(text=filez)
    pathlabel4.config(text=filez)
    pathlabel4.place(x = 650, y = 100)
    print root.tk.splitlist(filez)

def callback5():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel5 = Label(root)
    pathlabel5.pack()
    pathlabel5.config(text=filez)
    pathlabel5.config(text=filez)
    pathlabel5.place(x = 650, y = 100)
    print root.tk.splitlist(filez)

def callback6():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel6 = Label(root)
    pathlabel6.pack()
    pathlabel6.config(text=filez)    
    pathlabel6.config(text=filez)
    pathlabel6.place(x = 650, y = 100)
    print root.tk.splitlist(filez)

def callback7():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel7 = Label(root)
    pathlabel7.pack()
    pathlabel7.config(text=filez)
    pathlabel7.config(text=filez)
    pathlabel7.place(x = 650, y = 100)
    print root.tk.splitlist(filez)

def callback8():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel8 = Label(root)
    pathlabel8.pack()
    pathlabel8.config(text=filez)
    pathlabel8.config(text=filez)
    pathlabel8.place(x = 650, y = 100)
    print root.tk.splitlist(filez)

def callback9():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel9 = Label(root)
    pathlabel9.pack()
    pathlabel9.config(text=filez)
    pathlabel9.config(text=filez)
    pathlabel9.place(x = 650, y = 100)
    print root.tk.splitlist(filez)

def callback10():
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel10 = Label(root)
    pathlabel10.pack()
    pathlabel10.config(text=filez)
    pathlabel10.config(text=filez)
    pathlabel10.place(x = 650, y = 100)
    print root.tk.splitlist(filez)



def display():
    d1 = tk.Button(root, text="Add dataset 1", width = 10, height = 2, bg = "blue", command=callback1)
    d1.pack()
    d1.place(x = 500, y = 100)
    d1 = tk.Button(root, text="Add dataset 2", width = 10, height = 2, bg = "blue", command=callback2)
    d1.pack()
    d1.place(x = 500, y = 150)
    d1 = tk.Button(root, text="Add dataset 3", width = 10, height = 2, bg = "blue", command=callback3)
    d1.pack()
    d1.place(x = 500, y = 200)
    d1 = tk.Button(root, text="Add dataset 4", width = 10, height = 2, bg = "blue", command=callback4)
    d1.pack()
    d1.place(x = 500, y = 250)
    d1 = tk.Button(root, text="Add dataset 5", width = 10, height = 2, bg = "blue", command=callback5)
    d1.pack()
    d1.place(x = 500, y = 300)
    d1 = tk.Button(root, text="Add dataset 6", width = 10, height = 2, bg = "blue", command=callback6)
    d1.pack()
    d1.place(x = 500, y = 350)
    d1 = tk.Button(root, text="Add dataset 7", width = 10, height = 2, bg = "blue", command=callback7)
    d1.pack()
    d1.place(x = 500, y = 400)
    d1 = tk.Button(root, text="Add dataset 8", width = 10, height = 2, bg = "blue", command=callback8)
    d1.pack()
    d1.place(x = 500, y = 450)
    d1 = tk.Button(root, text="Add dataset 9", width = 10, height = 2, bg = "blue", command=callback9)
    d1.pack()
    d1.place(x = 500, y = 500)
    d1 = tk.Button(root, text="Add dataset 10", width = 10, height = 2, bg = "blue", command=callback10)
    d1.pack()
    d1.place(x = 500, y = 550)
    


dataset = tk.Button(root, text="Choose Datasets", width = 20, height = 5, bg = "blue", command=display)
dataset.pack()
pathlabel = Label(root)
pathlabel.pack()

algo = tk.Button(root, text="Choose Algorithms", width = 20, height = 5, bg = "red", command=callback3)
run = tk.Button(root, text="RUN", width = 20, height = 5, bg = "yellow", command=callback2)
dataset.place(x = 10, y = 100)
algo.place(x = 10, y = 300)
run.place(x = 10, y =500 )

#Background Color
root["bg"] = "black"


root.mainloop()
