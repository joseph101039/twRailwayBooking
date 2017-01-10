from sklearn import ensemble
import os
from PIL import Image
import numpy as np
#from rf_testing_score import testing
from math import sqrt
import cPickle
import time


#################  3. Training a digit recognizing machine ####################

def train_digit_recog_classifier(ans_path = "/home/joseph/Captcha/ImageOut_value.txt", img_src = "/home/joseph/Captcha/tmp_slice_larger/"):
	img_value = []
	with open(ans_path, 'r') as vr:
		img_value = vr.read().splitlines()

	img_num = len(img_value)
	img_value = [v.split(',')[1] for v in img_value]

	input_img = []
	target_class = []
	for i in xrange(img_num):
		if len(img_value[i]) == 5:
			for j in range(1, 6):
				target_class.append(int(img_value[i][j - 1]))
				img = Image.open(img_src +  'img' + str(i) + "_" + str(j) +".jpg")
				img = np.asarray(img)
				input_img.append(img.ravel())
		elif len(img_value[i]) == 6:
			for j in range(1, 7):
				target_class.append(int(img_value[i][j - 1]))
				img = Image.open(img_src + "img" + str(i) + "_" + str(j) +".jpg")
				img = np.asarray(img)
				input_img.append(img.ravel())

	input_img = np.asarray(input_img)
	target_class = np.asarray(target_class)

	clf = ensemble.RandomForestClassifier(n_estimators = 200, max_features = int(2 * sqrt(len(input_img))), n_jobs = 3) # <-- accu = 0.6988, 30 remove the balanced weight
	clf.fit(input_img, target_class)
	print "Training with RF training accuracy: %.4f" %clf.score(input_img, target_class)
	return clf


### save random forest model ###
def save_digit_recog_classifier(clf, filename):
	with open(filename, 'wb') as rw:
		cPickle.dump(clf, rw)


### load the svm model ###
def load_digit_recog_classifier(filename):
	with open(filename, 'rb') as rr:
		clf = cPickle.load(rr)

	return clf


###############  4. Predicting the digits ####################

def predict_captcha(clf, ans_path = "/home/joseph/Captcha/ImageOut_value_test.txt", img_src = "/home/joseph/Captcha/tmp1_slice/"):
	path =  "/home/joseph/Captcha/"
	#start = 0, end = 3000
	img_value = []
	with open(ans_path , 'r') as vr:
		content = vr.read().splitlines() #[img_index, img_vlaue] for every element
		content = [c.split(',') for c in content]

	predict_value = []
	start_time = time.time()

	for i in xrange(len(content)):
		img_index = content[i][0]
		img_value = content[i][1]
		iarr = []
		if len(img_value) == 5:		#5 digits
			for j in range(1, 6):
				img = Image.open(img_src + 'img' + img_index+ '_' + str(j) + '.jpg')
				iarr.append(np.asarray(img).ravel())
			ch = clf.predict(np.asarray(iarr))
			predict_value.append(''.join(str(c) for c in ch))

		elif len(img_value) == 6:		#6 digits
			for j in range(1, 7):
				img = Image.open(img_src + 'img' + img_index + '_' + str(j) + '.jpg')
				iarr.append(np.asarray(img).ravel())
			ch = clf.predict(np.asarray(iarr))
			predict_value.append(''.join(str(c) for c in ch))

	print("--- %s seconds for RF machine predict %d images---" % ((time.time() - start_time), len(predict_value)))
	#print the testing accuracy
	correct = 0
	for i in xrange(len(content)):
		img_value = content[i][1]
		if img_value == predict_value[i]:
			correct += 1

	accuracy  = float(correct) / len(predict_value)
	print "Testing accuracy = " + str(accuracy)
	return predict_value
