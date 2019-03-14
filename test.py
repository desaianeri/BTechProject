# imports
import weka.core.jvm as jvm
import weka.core.converters as conv
from weka.classifiers import Evaluation, Classifier
from weka.core.classes import Random
import weka.plot.classifiers as plcls  # NB: matplotlib is required
import os

data_dir="/home/desais/BTech Project/"

jvm.start(packages=True)
from weka.core.converters import Loader
loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file(data_dir + "sonar.arff")
data.class_is_last()

#print(data)

cls = Classifier(classname="weka.classifiers.bayes.NaiveBayes")

evl = Evaluation(data)
evl.crossvalidate_model(cls, data, 10, Random(1))

print(evl.summary("=== NaiveBayes on sonar (stats) ===",False))
print(evl.matrix("=== NaiveBayes on sonar(confusion matrix) ==="))
#plcls.plot_classifier_errors(evl.predictions, absolute=False,wait = True)
plcls.plot_roc(evl, class_index=[0,1], wait=True)
print("areaUnderROC/1: " + str(evl.area_under_roc(1)))

jvm.stop()
