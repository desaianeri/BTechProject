import Tkinter as tk
from PIL import ImageTk, Image
import tkFileDialog
from tkFileDialog   import askopenfilename
import weka.core.jvm as jvm
import weka.core.converters as conv
from weka.classifiers import Evaluation, Classifier
from weka.core.classes import Random
import weka.plot.classifiers as plcls  # NB: matplotlib is required
import os
from weka.core.converters import Loader
import numpy as np


#Declaration of global variables

final_algo = []
final_data_list = []
algo_list = []


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


n = 100
	

#Rank function

def rank(matrix, algo, dataset):

	print ("marix init", matrix[0])
	temp = []
	temp1 = []
	rank_mat = []

	i = 0
	while i < dataset:
		temp = matrix[i][:]
		temp.sort()
		print (temp)
		j = 0
		while j < algo:
			k = 0
			while k < algo:
				if(temp[j] == matrix[i][k]):
					print ("inside if",temp[j])
					rank_mat[i].append(j)				
					rank_mat[i][j] = temp.index(matrix[i][k])
					print (rank[i][j])
				k += 1
			j += 1
		i += 1
	
	print (matrix[0])


#RUN action

def execute():

	total_num_datasets = 0
	dataset_string = []
	MatHov = []

	for i in range(0, len(final_algo)):
		MatHov.append([])


	#iterate over final_data_list to get total number of selected datasets
	#i is the list

	for i in final_data_list:
		total_num_datasets = total_num_datasets + len(i)
		for j in i:
			dataset_string.append(j)

	d = 0
	jvm.start(packages = True)		#Must start and stop jvm once .Else runtime error of cannot start jvm
	while(d < len(dataset_string)):

		a = 0

		while(a < len(final_algo)):

			MatHov[d].append(a)
			MatHov[d][a] = HOV(str(dataset_string[d]), str(final_algo[a]))
				
			a = a + 1

		d = d + 1

	rank(MatHov, len(final_algo), len(dataset_string))
	jvm.stop()


#Performs 10cv cross validation and stores the mean in the matrix

def CV10(dataset,  algo):
	print "inside 10cv"
	print("dataset ----" + dataset)
	print("algorithm ----" + algo)

	#Executing 10FCV

#	jvm.start(packages=True)
	loader = Loader(classname="weka.core.converters.ArffLoader")
	data = loader.load_file(dataset)
	data.class_is_last()

	#print(data)

	cls = Classifier(classname=algo)

	evl = Evaluation(data)
	evl.crossvalidate_model(cls, data, 2, Random(5))

	print("areaUnderROC/1: " + str(evl.area_under_roc(1)))

#	jvm.stop()

def HOV(dataset,  algo):
	print "inside hov"
	print("dataset ----" + dataset)
	print("algorithm ----" + algo)

	#Executing HOV \_*-*_/

#	jvm.start(packages=True)
	loader = Loader(classname="weka.core.converters.ArffLoader")
	data = loader.load_file(dataset)
	data.class_is_last()

	train, test = data.train_test_split(70.0, Random(10))

	cls = Classifier(classname=algo)
	cls.build_classifier(train)

	evl = Evaluation(train)
	evl.test_model(cls, test)

	return (str(evl.area_under_roc(1)))
	


#Adding Datasets

def filechoose():

    global n
    filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')
    pathlabel2 = tk.Label(root)
    pathlabel2.pack()
    pathlabel2.config(text=filez)
    m = 650
    pathlabel2.place(x = m ,y = n)
    n = n + 100
    dataset_list = root.tk.splitlist(filez)
    final_data_list.append(dataset_list)
#    print(final_data_list)



#Select algo
def selectalgo():
        master = tk.Toplevel(root)
	center(master)
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry('%sx%s' % (width/4, height/4))
	master.config(bg = "white")

	def var_states():

                algo_list = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get()]
                l = len(algo_list)	

                
                n = i = 0


                while n < l:
                        if algo_list[0] == 1 and n == 0:
                                final_algo.insert(i, "weka.classifiers.functions.MultilayerPerceptron")
                                i += 1
                        if algo_list[1] == 1 and n == 1:
                                final_algo.insert(i, "weka.classifiers.lazy.IBk")
                                i += 1
                        if algo_list[2] == 1 and n == 2:
                                final_algo.insert(i, "weka.classifiers.functions.SMO")
                                i += 1
                        if algo_list[3] == 1 and n == 3:
                                final_algo.insert(i, "weka.classifiers.trees.RandomForest")
                                i += 1
                        if algo_list[4] == 1 and n == 4:
                                final_algo.insert(i, "weka.classifiers.bayes.NaiveBayes")
                                i += 1
                        n += 1


                print(final_algo)	#Print algo list
		algo_len = len(final_algo)
		print ("Number of algorithms selected : " + str(algo_len))
                master.destroy()


	algo_pic = ImageTk.PhotoImage(Image.open("dd6.png"))
        label = tk.Label(master, image = algo_pic, text="Algorithms:", bg = "white").grid(row = 0, sticky = tk.W, pady = 1)
        var1 = tk.IntVar()
        cb1 = tk.Checkbutton(master, text = "ANN", bg = "white", variable = var1).grid(row = 2, sticky = tk.W)
        var2 = tk.IntVar()
        cb2 = tk.Checkbutton(master, text = "KNN", bg = "white", variable = var2).grid(row = 3, sticky = tk.W)
        var3 = tk.IntVar()
        cb3 = tk.Checkbutton(master, text = "SVM", bg = "white", variable = var3).grid(row = 4, sticky = tk.W)
        var4 = tk.IntVar()
        cb4 = tk.Checkbutton(master, text = "Random Forest",bg = "white", variable = var4).grid(row = 5, sticky = tk.W)
        var5 = tk.IntVar()
        cb5 = tk.Checkbutton(master, text = "Naive Bayes",bg = "white", variable = var5).grid(row = 6, sticky = tk.W)

	dphoto = ImageTk.PhotoImage(Image.open("dd4.png"))
        done = tk.Button(master, text = "done",image = dphoto, bg = "white", command = var_states).grid(row = 7, sticky = tk.W, pady = 4)
	qphoto = ImageTk.PhotoImage(Image.open("dd5.png"))
        quit = tk.Button(master, text = "quit",image = qphoto, bg = "white", command = master.destroy).grid(row = 7, column = 2, sticky = tk.W, pady = 4)

	
   	master.mainloop()


#Background Image

background_image=ImageTk.PhotoImage(Image.open("b4.png"))
background_label = tk.Label(image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#Adding buttons

dataset = tk.Button(root, text="Choose Datasets")
photo = ImageTk.PhotoImage(Image.open("dataset.png"))
dataset.config(image=photo,width ="130",height = "70", activebackground="black", bd=0, command = filechoose)

algo = tk.Button(root, text="Choose Algorithms", foreground = 'red')
photo1 = ImageTk.PhotoImage(Image.open("algo.png"))
algo.config(image=photo1,width ="140",height = "60", activebackground="black", bd=0, command = selectalgo)

run = tk.Button(root, text="RUN")
photo2 = ImageTk.PhotoImage(Image.open("run.png"))
run.config(image=photo2,width ="160",height = "130", activebackground="black",bg="black", command = execute)

dataset.place(x = 700, y = 585)
algo.place(x = 400, y = 600)
run.place(x = 1100, y = 535 )

root.mainloop()
