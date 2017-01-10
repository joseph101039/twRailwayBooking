from sklearn import svm
from sklearn import ensemble
from PIL import Image
import numpy as np
import cPickle

### save the svm model  ###
def save_num_of_digit_classifier(clf, filename):
	with open(filename, 'wb') as sw:
		cPickle.dump(clf, sw)

### load the svm model ###
def load_num_of_digit_classifier(filename):
	with open(filename, 'rb') as sr:
		clf = cPickle.load(sr)

	return clf


### predicting the unknown photos ###
def predict_num_of_digit(image, clf):
	im = image.convert('L')		#convert into gray-scale
	predict_array = np.reshape(np.asarray(im), (1, -1))
	predict_result = clf.predict(predict_array)	#0: 5 digits; 1: 6 digits
	return predict_result


########## 1. Training SVM for recognize 5 or 6 digits ##########
path = "/home/joseph/Captcha/"
start = 0
end = 3000

def train_num_of_digit_svm_classifier(path=path):
	img_value = []
	with open(path + "ImageOut_value.txt", 'r') as vr:
		img_value = vr.read().splitlines()

	img_value = [v.split(',')[1] for v in img_value]

	input_array = []
	target_array = []
	for i in xrange(start, end):	#<---img0 ~ img1100
		image = Image.open(path + 'tmp/img' + str(i) + '.jpg')
		im = image.convert('L')		#convert into gray-scale
		parr = np.asarray(im)
		input_array.append(parr.ravel())
		if len(img_value[i]) == 5:
			target_array.append(0)
		elif len(img_value[i]) == 6:
			target_array.append(1)


	input_array = np.asarray(input_array)
	target_array = np.asarray(target_array)

	### Training with SVM ###
	print "Start to train 5 or 6-digits classifier"

	clf = svm.SVC(kernel='linear', decision_function_shape = 'ovo')		#clf = svm.SVC(kernel='linear')
	clf.fit(input_array, target_array)
	return clf
