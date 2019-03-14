import Tkinter as tk

#Fullscreen window
root=tk.Tk()
root.title("ART")
root.attributes('-zoomed', True)

#Adding buttons

def callback():
    print "click!"

dataset = tk.Button(root, text="Choose Datasets", width = 20, height = 5, bg = "blue", command=callback)
algo = tk.Button(root, text="Choose Algorithms", width = 20, height = 5, bg = "red", command=callback)
run = tk.Button(root, text="RUN", width = 20, height = 5, bg = "yellow", command=callback)
dataset.place(x = 10, y = 100)
algo.place(x = 10, y = 300)
run.place(x = 10, y =500 )

#Background Color
root["bg"] = "black"


root.mainloop()
