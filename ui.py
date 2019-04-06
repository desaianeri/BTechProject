import Tkinter as tk
from PIL import ImageTk, Image
import tkFileDialog
from tkFileDialog  import askopenfilename
import weka.core.jvm as jvm
import weka.core.converters as conv
from weka.classifiers import Evaluation, Classifier
from weka.core.classes import Random
import weka.plot.classifiers as plcls  # NB: matplotlib is required
import os
from weka.core.converters import Loader
import numpy

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
#RUN action

def execute():

	total_num_datasets = 0
	dataset_string = []
	Mat10cv = []
	mat_list = []
	avg_rank_list_10cv = []
        rank_10cv = []

	MatHov = []
	mat_Hlist = []
	avg_rank_list_Hov = []

        Mat5x2cv = []
	mat_5x2list = []
	avg_rank_list_5x2cv = []


	#iterate over final_data_list to get total number of selected datasets
	#i is the list

	for i in final_data_list:
		total_num_datasets = total_num_datasets + len(i)
		for j in i:
			dataset_string.append(j)

	#Implementation of 10cv cross validation

	d = 0
	jvm.start(packages = True)		#Must start and stop jvm once .Else runtime error of cannot start jvm

	while(d < len(dataset_string)):

		a = 0
		mat_list =[]

                #added confirm once
                mat_Hlist = []
                mat_5x2list = []

		while(a < len(final_algo)):

			mat_list.append(CV10(str(dataset_string[d]), str(final_algo[a]), total_num_datasets))
			mat_Hlist.append(HOV(str(dataset_string[d]), str(final_algo[a]), total_num_datasets))
			mat_5x2list.append(CV5x2(str(dataset_string[d]), str(final_algo[a]), total_num_datasets))	
			a = a + 1

		Mat10cv.append(mat_list)
		MatHov.append(mat_Hlist)
		Mat5x2cv.append(mat_Hlist)
		d = d + 1

	jvm.stop()

	#Sorts the entries row wise to calculate the ranks in descending order

        index_10cv , sorted_10cv =  perform_sort(Mat10cv)

#       added - confirm once
        index_hov, sorted_hov = perform_sort(MatHov)
        index_5x2cv, sorted_5x2cv = perform_sort(Mat5x2cv)

	#Rank matrix generation

	rank_10cv = rank(sorted_10cv, total_num_datasets)

        #Caluculate final rank with index and sorted rank values

        final_rank_10cv = final_rank(rank_10cv, index_10cv)

        print("---final rank list -----" + str(final_rank_10cv))

	avg_rank_list_10cv = avg_rank(total_num_datasets, final_rank_10cv)

        print("--avg rank ::" + str(avg_rank_list_10cv))
	rank_Hov = rank(sorted_hov, total_num_datasets)

        rank_5x2cv = rank(sorted_5x2cv, total_num_datasets)
	#calculating avergage rank list for a given rank matrix

	avg_rank_list_Hov = avg_rank(total_num_datasets, rank_Hov)

        avg_rank_list_5x2cv = avg_rank(total_num_datasets, rank_5x2cv)

#Calculates final rank matrix

def final_rank(rank, index):

    row = len(rank)
    col = len(rank[0])
    final_rank_list = [[0 for x in range(col)] for y in range(row)]

#    print("---final rank rank -----" + str(rank))
#    print("---final rank index -----" + str(index))

    i = 0

    while(i < row):

        j = 0

        while(j < col):    #gives number of columns

            final_rank_list[i][index[i][j]] = rank[i][j]
            j = j + 1

        i = i + 1

#    print("---final rank list -----" + str(final_rank_list))
    return final_rank_list

#Sorts the matrix required to calculate rank and generates the index matrix

def perform_sort(mat):

    index = []
    sorted_mat = []

    for i in mat:

            sorted_mat.append((numpy.sort(i)[::-1]).tolist())   
            index.append((numpy.argsort(i)[::-1]).tolist())
            
#    print("sorted matrix---" + str(sorted_mat))            
#    print("index matrix----" + str(index))

    return index , sorted_mat

#Calculation of average rank

def avg_rank(num_datasets, rank):

	i = 0
	tmp = []

#	print("rank matrix ------" + str(rank_10cv))
	while(i < len(final_algo)):

		j = 0
		sum_ranks = 0

		while(j < num_datasets):
			sum_ranks = sum_ranks + rank[j][i]	
			j = j + 1

		tmp.append(sum_ranks / num_datasets)
		i = i + 1
		
	return tmp

#Calculates rank of a given sorted matrix

def rank(mat, num_datasets):

	i = 0
        tmp = []

	while(i < num_datasets):

	        j = 0
	        rline = []
	        r = 1

	        while (j < (len(final_algo) - 1)): 

	                if(mat[i][j] != mat[i][j + 1]):
	                        rline.append(r)
	                        r = r + 1
	                        j = j + 1
	                        if(j == (len(final_algo) - 1)):
	                                rline.append(r)
	                                continue
	                        else:
	                                continue

	                else:   #repetitions exist
	                        count = 2
	                        k = j

        	                while( j < (len(final_algo) - 2)):
        	                        if( mat[i][j + 1] == mat[i][j + 2]):    #col - 2        
        	                                count = count + 1
        	                                j = j + 1
                	                        continue
                        	        else:
                        	                break

	                        l = 0
	                        while(l < count):
	                                rline.append(r/float(count))
	                                l = l + 1
	                        r = r + 1
	                        j = k + count

        	        if(len(rline) == (len(final_algo) - 1)):
        	                rline.append(r)
	        tmp.append(rline)
	        i = i + 1
        return tmp

#Performs 10cv cross validation and stores the mean in the matrix

def CV10(dataset,  algo, num_datasets):

	#Executing 10FCV
	loader = Loader(classname="weka.core.converters.ArffLoader")
	data = loader.load_file(dataset)
	data.class_is_last()

	cls = Classifier(classname=algo)

	evl = Evaluation(data)
	evl.crossvalidate_model(cls, data, 10, Random(1))

        print(evl.summary("=== " +str(algo)+ " on" + str(dataset) + " ===",False))
#        print(evl.matrix("=== NaiveBayes on click prediction(confusion matrix) ==="))
	print("areaUnderROC/1: " + str(evl.area_under_roc(1)))
	return evl.area_under_roc(1)

def HOV(dataset,  algo, num_datasets):
	#Executing HOV \_*-*_/

	loader = Loader(classname="weka.core.converters.ArffLoader")
	data = loader.load_file(dataset)
	data.class_is_last()

	train, test = data.train_test_split(70.0, Random(10))

	cls = Classifier(classname=algo)
	cls.build_classifier(train)

	evl = Evaluation(train)
	evl.test_model(cls, test)

	return evl.area_under_roc(1)
	
def CV5x2(dataset,  algo, num_datasets):

	loader = Loader(classname="weka.core.converters.ArffLoader")
	data = loader.load_file(dataset)
	data.class_is_last()

	cls = Classifier(classname=algo)

	evl = Evaluation(data)
	evl.crossvalidate_model(cls, data, 2, Random(5))

	return evl.area_under_roc(1)

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

#Select algo

def selectalgo():
        master = tk.Toplevel(root)
        center(master)
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry('%sx%s' % (width/3, height/3))
	master.config(bg="white")

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


                algo_len = len(final_algo)

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
