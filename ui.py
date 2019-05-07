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
import matplotlib.pyplot as plt

#Declaration of global variables

final_algo = []
final_data_list = []
algo_list = []

root=tk.Tk()
#Fullscreen window
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

#Run button click action

#def show_terminal():
#    os.system("gnome-terminal -e 'python execute.py'")

#RUN action
avg_list = []
def execute():

#        print("-----final_algo----" + str(final_algo))
#        print("-----_algo_list----" + str(algo_list))
#        print("-----final_data_list----" + str(final_data_list))

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

        global avg_list

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
        #decide_post_hoc(total_num_datasets, ff_10cv, avg_rank_list_10cv, avg_rank_list_Hov,avg_rank_list_5x2cv )

	rank_Hov = rank(sorted_Hov, total_num_datasets)

	final_rank_Hov = final_rank(rank_Hov, index_Hov)
	print("---final rank list Hov -----" + str(final_rank_Hov))

	avg_rank_list_Hov = avg_rank(total_num_datasets, final_rank_Hov)
	print("--avg rank Hov::" + str(avg_rank_list_Hov))

	friedman_Hov = friedman(avg_rank_list_Hov, total_num_datasets)
	print("---friedman  Hov---" + str(friedman_Hov))

	ff_Hov = f_distribution(friedman_Hov, total_num_datasets)
	print("---f distribution  Hov---" + str(ff_Hov))

	#decide_post_hoc(total_num_datasets, ff_Hov, avg_rank_list_10cv, avg_rank_list_Hov,avg_rank_list_5x2cv )
    
        rank_5x2cv = rank(sorted_5x2cv, total_num_datasets)
	#calculating avergage rank list for a given rank matrix

	final_rank_5x2cv = final_rank(rank_5x2cv, index_5x2cv)
	print("---final rank list 5x2cv -----" + str(final_rank_5x2cv))

	avg_rank_list_5x2cv = avg_rank(total_num_datasets, final_rank_5x2cv)
	print("--avg rank 5x2cv::" + str(avg_rank_list_5x2cv))

	friedman_5x2cv = friedman(avg_rank_list_5x2cv, total_num_datasets)
	print("---friedman  5x2cv---" + str(friedman_5x2cv))

	ff_5x2cv = f_distribution(friedman_5x2cv, total_num_datasets)
	print("---f distribution  5x2cv---" + str(ff_5x2cv))

        avg_list.append(avg_rank_list_10cv)
        avg_list.append(avg_rank_list_Hov)
        avg_list.append(avg_rank_list_5x2cv)

	#decide_post_hoc(total_num_datasets, ff_10cv, ff_5x2cv,ff_hov, avg_rank_list_10cv, avg_rank_list_Hov,avg_rank_list_5x2cv )
	decide_post_hoc(total_num_datasets, ff_10cv, ff_5x2cv, ff_Hov, avg_list)
    

def dbox_no_posthoc(values):
        no_validation = []
        i = 0
        while(i < 3):
            if(values[i] == 0):
                no_validation.append(match_validation_name(i))
            i = i + 1
           
        print"---no validation---" + str(no_validation)

        if  no_validation:
            tkMessageBox.showinfo("Hello there :)", "Post hoc cannot be performed for these validations : " + str(no_validation))
        
        final_algo = []
        final_data_list = []
        algo_list = []

#Decide whether or not to perform post hoc tests

def decide_post_hoc(num_datasets, Ff_10cv,Ff_5x2cv, Ff_hov, avg_list):
    print "in decide post hoc---avg list---" + str(avg_list)
    values = [0,0,0]
    degree_of_freedom = (len(final_algo) - 1) * (num_datasets - 1)
    f_critical =  scipy.stats.f.ppf(q=1-0.05, dfn = (len(final_algo) - 1) , dfd = degree_of_freedom)

    values = [1,1,1]
    nemenyi(num_datasets, avg_list, values)

    if(f_critical < Ff_10cv):
        #reject null hypothesis and perform post hoc
        values[0]  = 1

    else:
        values[0]  = 0

    if(f_critical < Ff_5x2cv):
        #reject null hypothesis and perform post hoc
        values[1]  = 1

    else:
        values[1]  = 0

    if(f_critical < Ff_hov):
        #reject null hypothesis and perform post hoc
        values[2]  = 1

    else:
        values[2]  = 0

    dbox_no_posthoc(values)
'''
    i = 0
    while(i < 3):
        if(values[i] == 1):
            nemenyi(num_datasets, avg_list, values)
            break
        i = i + 1
'''

#Perform post hoc (Nemenyi test)
threshold = []
def nemenyi(num_datasets, avg_list, values):
   
    critical_diff = 0.0
    global threshold
    worst_algo_list = []
    #Get the ciritcal difference value
    
    critical_diff = calculate_critical_difference(num_datasets)    
    print "critical difference---" + str(critical_diff)

    i = 0
    while(i < 3):
        #Get the threshold for all the validations

        threshold.append(get_threshold(critical_diff, avg_list[i]))

        #Get the list of algorithm who perform worse than the control algorithm

        worst_algo_list.append(get_worse_algo_list(avg_list[i], threshold[i]))
        #print("----worse_algo_list returned---" + str(worse_algo_list_10cv))

        #Plot the graph for validation
        i = i + 1
    print("-----threshold list----" + str(threshold))
    print("-----worst algo list----" + str(worst_algo_list))

    plot_graph(threshold, avg_list)


#Plots the graph for given validation
def plot_graph(threshold, avg_list):
    N = len(final_algo)
    ind = numpy.arange(N)  # the x locations for the groups
    width = 0.08       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects1 = ax.bar(ind, avg_list[0], width, color='#898585')
    rects2 = ax.bar(ind+width, avg_list[1], width, color='#070000')
    rects3 = ax.bar(ind+width*2, avg_list[2], width, color='#9FCAEF')

    ax.set_ylabel('Friedman ranking')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( get_algo_names() )
    ax.legend( (rects1[0], rects2[0], rects3[0]), ('10cv', 'Hold Out', '5x2cv') )

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.axhline(y=threshold[0], color='#898585', linestyle='-')
    plt.axhline(y=threshold[1], color='#070000', linestyle='-')
    plt.axhline(y=threshold[2], color='#070000', linestyle='-')

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

#Perform post hoc (Nemenyi test)

def match_algo_name(argument):
    switcher = {
        0: "ANN",
        1: "KNN",
        2: "SVM",
        3: "Random Forest",
        4: "Naive Bayes"
    }

    return switcher.get(argument, "nothing")

#Get validation name for no post hoc

def match_validation_name(argument):
    switcher = {
        0: "10 fold cross validation",
        1: "5x2 cross validation",
        2: "hold out"
    }

    return switcher.get(argument, "nothing")

#Returns the selected algo names

def get_algo_names():
    algo_names = []
    i = 0

    while(i < len(algo_list)):
        if(algo_list[i] == 1):
            algo_names.append(match_algo_name(i))
        
        i = i + 1

    return algo_names

#Return the list of algorithms whose performance is worse than the control algorithm

def get_worse_algo_list(avg_rank, threshold):

    worse_algo_list = []
    i = 0

    while(i < len(avg_rank)):

        print ("avg_rank----" + str(avg_rank[i]))
        if(avg_rank[i] > threshold):
            worse_algo_list.append(i)
        i = i + 1

    return worse_algo_list

#Calculates the threshold for validations

def get_threshold(critical_diff, final_rank):

    threshold = 0.0

    print("final average rank in 10cv-----" + str(final_rank))
    print("minimum of average rank in 10cv--- " + str(min(final_rank)))
    threshold = min(final_rank) + float(critical_diff)

    return threshold

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
                global algo_list
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
        
#See Result
def see_result():
    print "in result"
    window = tk.Toplevel(root)

    img = ImageTk.PhotoImage(Image.open("b4.png"))
    back_label = tk.Label( image=img)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
#Background Image

background_image=ImageTk.PhotoImage(Image.open("b4.png"))
background_label = tk.Label(image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#Adding buttons

result = tk.Button(root, text="Result")
photo3 = ImageTk.PhotoImage(Image.open("dataset.png"))
result.config(image=photo3,width ="130",height = "70", activebackground="black", bg = "brown", command = see_result)

dataset = tk.Button(root, text="Choose Datasets")
photo = ImageTk.PhotoImage(Image.open("dataset.png"))
dataset.config(image=photo,width ="130",height = "70", activebackground="black", bg = "brown", command = filechoose)

algo = tk.Button(root, text="Choose Algorithms", foreground = 'red')
photo1 = ImageTk.PhotoImage(Image.open("algo.png"))
algo.config(image=photo1,width ="140",height = "60", activebackground="black", bg = "red", command = selectalgo)

run = tk.Button(root, text="RUN")
photo2 = ImageTk.PhotoImage(Image.open("run.png"))
run.config(image=photo2,width ="160",height = "130", activebackground="blue",bg="black", command = execute)

result.place(x = 1100, y = 100)
dataset.place(x = 1100, y = 400)
algo.place(x = 1100, y = 250)
run.place(x = 1100, y = 535 )

root.mainloop()
