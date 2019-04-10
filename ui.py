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
import scipy.stats
import tkMessageBox
import math

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

#	print (MatHov[0])
        index_10cv , sorted_10cv =  perform_sort(Mat10cv)

#       added - confirm once
        index_Hov, sorted_Hov = perform_sort(MatHov)
        index_5x2cv, sorted_5x2cv = perform_sort(Mat5x2cv)

	#Rank matrix generation

	rank_10cv = rank(sorted_10cv, total_num_datasets)

        #Caluculate final rank with index and sorted rank values

        final_rank_10cv = final_rank(rank_10cv, index_10cv)

        print("---final rank list -----" + str(final_rank_10cv))

	avg_rank_list_10cv = avg_rank(total_num_datasets, final_rank_10cv)

        print("--avg rank ::" + str(avg_rank_list_10cv))

        #Perform friedman test
        friedman_10cv = friedman(avg_rank_list_10cv, total_num_datasets)
    
        print("---friedman  10 cv---" + str(friedman_10cv))

        #Calculate f-distribution
        ff_10cv = f_distribution(friedman_10cv, total_num_datasets)

        print("---f distribution  10 cv---" + str(ff_10cv))

        #decide whether or not to perform post hoc tests
        decide_post_hoc(total_num_datasets, ff_10cv)

	rank_Hov = rank(sorted_Hov, total_num_datasets)
	final_rank_Hov = final_rank(rank_Hov, index_Hov)
	print("---final rank list Hov -----" + str(final_rank_Hov))

	avg_rank_list_Hov = avg_rank(total_num_datasets, final_rank_Hov)
	print("--avg rank Hov::" + str(avg_rank_list_Hov))

	friedman_Hov = friedman(avg_rank_list_Hov, total_num_datasets)
	print("---friedman  Hov---" + str(friedman_Hov))

	ff_Hov = f_distribution(friedman_Hov, total_num_datasets)
	print("---f distribution  Hov---" + str(ff_Hov))

	decide_post_hoc(total_num_datasets, ff_Hov)
    

        rank_5x2cv = rank(sorted_5x2cv, total_num_datasets)
	#calculating avergage rank list for a given rank matrix

        avg_rank_list_5x2cv = avg_rank(total_num_datasets, rank_5x2cv)

def dbox_no_posthoc():
	tkMessageBox.showinfo("Post Hoc", "Sorry, cannot perform post-hoc test :( Critical value is greater than calculated value. click ok to proceed")

#Decide whether or not to perform post hoc tests

def decide_post_hoc(num_datasets, Ff):

    degree_of_freedom = (len(final_algo) - 1) * (num_datasets - 1)
    f_critical =  scipy.stats.f.ppf(q=1-0.05, dfn = (len(final_algo) - 1) , dfd = degree_of_freedom)

    nemenyi(num_datasets)

    if(f_critical < Ff):
        #reject null hypothesis and perform post hoc
        print "perform post hoc"
        nemenyi(num_datasets)
    else:
        #display dialog box and inform that post hoc cannot be performed
	dbox_no_posthoc()
        print "don't perform post hoc"

#Perform post hoc (Nemenyi test)

def nemenyi(num_datasets):
   
    critical_diff = 0.0
    critical_diff = calculate_critical_difference(num_datasets)    

#    print "critical difference---" + str(critical_diff)

#Calculates critical difference

def calculate_critical_difference(num_datasets):

    critical_diff = 0.0
    qAlpha = 0.0
    tmp= 0.0

    qAlpha_values = [1.960, 2.343, 2.569, 2.728, 2.850, 2.949, 3.031, 3.102, 3.164]
    qAlpha = qAlpha_values[len(final_algo) - 2]

    tmp =  (float(len(final_algo)) * (len(final_algo) + 1)) / (6 * num_datasets)
    critical_diff = float(qAlpha) * math.sqrt(tmp)

    return critical_diff

#Calculate f-distribution vlues

def f_distribution(friedman, num_datasets):

    ff = 0.0
    ff = (float((num_datasets - 1)) * friedman) / ((num_datasets * (len(final_algo)  - 1)) - friedman)

    return ff

#Perfrom firedman test

def friedman(rank_list, num_datasets):

    result = 0.0
    sum_ranks = 0.0

    tmp1 = (12 * float(num_datasets))/(len(final_algo)*(len(final_algo) + 1))
    
    for i in rank_list:
        sum_ranks  = float(sum_ranks) + (i * i)
        
    tmp2 = float(sum_ranks) - ((len(final_algo) * pow((len(final_algo) + 1), 2)) / 4)

    result = tmp1 * tmp2

    return result

#Calculates final rank matrix

def final_rank(rank, index):

    row = len(rank)
    col = len(rank[0])

    final_rank_list = [[0 for x in range(col)] for y in range(row)]

    i = 0

    while(i < row):

        j = 0

        while(j < col):    #gives number of columns

            final_rank_list[i][index[i][j]] = rank[i][j]
            j = j + 1

        i = i + 1

    return final_rank_list

#Sorts the matrix required to calculate rank and generates the index matrix

def perform_sort(mat):

    index = []
    sorted_mat = []

    for i in mat:

            sorted_mat.append((numpy.sort(i)[::-1]).tolist())   
            index.append((numpy.argsort(i)[::-1]).tolist())
            
    return index , sorted_mat

#Calculation of average rank

def avg_rank(num_datasets, rank):

	i = 0
	tmp = []

	while(i < len(final_algo)):

		j = 0
		sum_ranks = 0

		while(j < num_datasets):
			sum_ranks = sum_ranks + float(rank[j][i])	
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

#        print(evl.summary("=== " +str(algo)+ " on" + str(dataset) + " ===",False))
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
#    pathlabel2 = tk.Label(root)
#    pathlabel2.pack()
#    pathlabel2.config(text=filez)
#    m = 650
#    pathlabel2.place(x = m ,y = n)
#    n = n + 100
    dataset_list = root.tk.splitlist(filez)
    final_data_list.append(dataset_list)

#Select algo

def selectalgo():
        master = tk.Toplevel(root)
        center(master)
        width = master.winfo_screenwidth()
        height = master.winfo_screenheight()
        master.geometry('%sx%s' % (width/3, height/3))
	master.config(bg="blanched almond")
	master.resizable(False, False)

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
        label = tk.Label(master, image = algo_pic, text="Algorithms:", bg = "blanched almond").grid(row = 0, sticky = tk.W, pady = 1)
        var1 = tk.IntVar()
        cb1 = tk.Checkbutton(master, text = "ANN", bg = "salmon", variable = var1).grid(row = 2, sticky = tk.W)
        var2 = tk.IntVar()
        cb2 = tk.Checkbutton(master, text = "KNN", bg = "indian red", variable = var2).grid(row = 3, sticky = tk.W)
        var3 = tk.IntVar()
        cb3 = tk.Checkbutton(master, text = "SVM", bg = "salmon", variable = var3).grid(row = 4, sticky = tk.W)
        var4 = tk.IntVar()
        cb4 = tk.Checkbutton(master, text = "Random Forest",bg = "indian red", variable = var4).grid(row = 5, sticky = tk.W)
        var5 = tk.IntVar()
        cb5 = tk.Checkbutton(master, text = "Naive Bayes",bg = "salmon", variable = var5).grid(row = 6, sticky = tk.W)

	dphoto = ImageTk.PhotoImage(Image.open("dd4.png"))
        done = tk.Button(master, text = "done",image = dphoto, bg = "indian red", command = var_states).grid(row = 7, sticky = tk.W, pady = 4)
	qphoto = ImageTk.PhotoImage(Image.open("dd5.png"))
        quit = tk.Button(master, text = "quit",image = qphoto, bg = "indian red", command = master.destroy).grid(row = 7, column = 2, sticky = tk.W, pady = 4)
	
   	master.mainloop()

#Background Image

background_image=ImageTk.PhotoImage(Image.open("b4.png"))
background_label = tk.Label(image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#Adding buttons

dataset = tk.Button(root, text="Choose Datasets")
photo = ImageTk.PhotoImage(Image.open("dataset.png"))
dataset.config(image=photo,width ="130",height = "70", activebackground="black", bg = "brown", command = filechoose)

algo = tk.Button(root, text="Choose Algorithms", foreground = 'red')
photo1 = ImageTk.PhotoImage(Image.open("algo.png"))
algo.config(image=photo1,width ="140",height = "60", activebackground="black", bg = "red", command = selectalgo)

run = tk.Button(root, text="RUN")
photo2 = ImageTk.PhotoImage(Image.open("run.png"))
run.config(image=photo2,width ="160",height = "130", activebackground="blue",bg="black", command = execute)

dataset.place(x = 1100, y = 350)
algo.place(x = 1100, y = 180)
run.place(x = 1100, y = 535 )

root.mainloop()
