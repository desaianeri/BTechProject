# imports
import weka.core.jvm as jvm
import weka.core.converters as conv
from weka.classifiers import Evaluation, Classifier
from weka.core.classes import Random
import weka.plot.classifiers as plcls  # NB: matplotlib is required
import os

data_dir="/home/suruchi/Desktop/BTECH Pro/new/click_prediction/"

jvm.start(packages=True)
from weka.core.converters import Loader
loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file(data_dir + "click_prediction.arff")
data.class_is_last()

#print(data)

cls = Classifier(classname="weka.classifiers.bayes.NaiveBayes")

evl = Evaluation(data)
evl.crossvalidate_model(cls, data, 2, Random(5))

print(evl.summary("=== NaiveBayes on click prediction (stats) ===",False))
print(evl.matrix("=== NaiveBayes on click prediction(confusion matrix) ==="))
#plcls.plot_classifier_errors(evl.predictions, absolute=False,wait = True)
plcls.plot_roc(evl, class_index=[0,1], wait=True)
print("areaUnderROC/1: " + str(evl.area_under_roc(1)))

jvm.stop()
