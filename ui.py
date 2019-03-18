import Tkinter as tk
from PIL import ImageTk, Image

#Fullscreen window

root=tk.Tk()
root.title("ART")
root.attributes('-zoomed', True)

#generic code to center a window
def center(win):
        """
        centers a tkinter window
        :param win: the root or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()


def selectalgo():
        print "click!"
        master = tk.Toplevel(root)
        center(master)
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry('%sx%s' % (width/4, height/4))

        def var_states():

                algo_list = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get()]
                l = len(algo_list)
                print (algo_list)

                final_algo = []
                n = i = 0


                while n < l:
                        if algo_list[0] == 1 and n == 0:
                                final_algo.insert(i, "ANN")
                                i += 1
                        if algo_list[1] == 1 and n == 1:
                                final_algo.insert(i, "KNN")
                                i += 1
                        if algo_list[2] == 1 and n == 2:
                                final_algo.insert(i, "SVM")
                                i += 1
                        if algo_list[3] == 1 and n == 3:
                                final_algo.insert(i, "Randf")
                                i += 1
                        if algo_list[4] == 1 and n == 4:
                                final_algo.insert(i, "NaiveB")
                                i += 1
                        n += 1


                print(final_algo)
                master.destroy()


        label = tk.Label(master, text="Algorithms:", bg = "white").grid(row = 0, sticky = tk.W)
        var1 = tk.IntVar()
        cb1 = tk.Checkbutton(master, text = "ANN", bg = "white", variable = var1).grid(row = 1, sticky = tk.W)
        var2 = tk.IntVar()
        cb2 = tk.Checkbutton(master, text = "KNN", bg = "white", variable = var2).grid(row = 2, sticky = tk.W)
        var3 = tk.IntVar()
        cb3 = tk.Checkbutton(master, text = "SVM", bg = "white", variable = var3).grid(row = 3, sticky = tk.W)
        var4 = tk.IntVar()
        cb4 = tk.Checkbutton(master, text = "Random Forest",bg = "white", variable = var4).grid(row = 4, sticky = tk.W)
        var5 = tk.IntVar()
        cb5 = tk.Checkbutton(master, text = "Naive Bayes",bg = "white", variable = var5).grid(row = 5, sticky = tk.W)

        done = tk.Button(master, text = "Done", bg = "yellow", command = var_states).grid(row = 6, sticky = tk.W, pady = 4)
        quit = tk.Button(master, text = "Quit", bg = "red", command = master.destroy).grid(row = 7, sticky = tk.W, pady = 4)
        master["bg"] = "white"


#Background Image

background_image=ImageTk.PhotoImage(Image.open("b4.png"))
background_label = tk.Label(image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def callback():
    print "click!"

#Adding buttons

dataset = tk.Button(root, text="Choose Datasets", width = 20, height = 5, bg = "blue", command=callback)
algo = tk.Button(root, text="Choose Algorithms", width = 20, height = 5, bg = "red", command = selectalgo)
run = tk.Button(root, text="RUN", width = 20, height = 5, bg = "yellow", command=callback)
dataset.place(x = 10, y = 100)
algo.place(x = 10, y = 300)
run.place(x = 10, y =500 )

root.mainloop()
