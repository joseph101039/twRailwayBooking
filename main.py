 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from seleniumLink import *
from numOfDigitRecog import load_num_of_digit_classifier, predict_num_of_digit
from PIL import Image
from imgProcess import *
from digitRecog import load_digit_recog_classifier, predict_captcha
from time import sleep
import random
from multiprocessing import Process, Value

def decaptcha(browser, svm_clf, rf_clf, success):
	img_name = 'ImageOut' + str(int(random.uniform(0,1) * 100000000))
	print "Image Name: " + img_name
	img = get_captcha_image(browser, img_name)
	
	if (img is not None):
		c = predict_num_of_digit(img, svm_clf)[0]
		if  c == 0:		#5 digits
			img_arr = slice_img_into_five_pieces(img = img, reWid = 30, reHei = 50)
		elif c == 1:		#6 digits
			img_arr = slice_img_into_six_pieces(img = img, reWid = 30, reHei = 50)

		captcha_value = predict_captcha(img_arr, rf_clf)
		send_captcha_value(browser, captcha_value)

		if not success.value:
			submit_captcha_value(browser)
		else:
			return False
	else:
		print "Image file does not exist: " + img_name
		return False


def child_process(success, svm_clf, rf_clf, index):
	browser = init_browser()
	#sleep(10)
	link_to_web(browser = browser, url = "http://railway.hinet.net/ctno1.htm")
	#person_id: 身份證;; from_station: 起站代碼;; to_station: 到站代碼;; getin_date: 搭車日期;; train_no: 車次代碼;; order_qty_str: 訂票張數	#getin_date's format: '2016/12/28'
	input_order_data_and_submit(browser = browser, person_id = 'N123456789', from_station = '149', to_station = '100', getin_date = '2017/01/15', train_no = '114', order_qty_str = '1')

	msg_code = 0
	v = decaptcha(browser, svm_clf, rf_clf, success)
	do_recaptcha, msg_code = recaptcha(browser)
	while do_recaptcha and not success.value:
		v = decaptcha(browser, svm_clf, rf_clf, success)
		do_recaptcha, msg_code = recaptcha(browser)

	if msg_code == 2:	#車次號碼錯誤，請再次確認
		quit_browser(browser)
	elif msg_code ==3 :	#您的車票已訂到
		computerCode = browser.find_element_by_id('spanOrderCode').text
		browser.save_screenshot('screenshot' + str(index) + '.png')
		if success.value:
			cancel_order(browser)
		else:
			success.value = True
	elif msg_code == 4:	#NoSuchElementException for orange02 class title element
		quit_browser(browser)




if __name__ == "__main__":
	svm_clf = load_num_of_digit_classifier("numOfDigitSVM_3000sample.bin")
	rf_clf = load_digit_recog_classifier("digitRecogRF_3000sample_larger.bin")
	success = Value('i', False)
	proc = []
	proc_count = 2
	for i in range(proc_count):
       		proc.append(Process(target=child_process, args=(success, svm_clf, rf_clf, i)))

       	for p in proc:
       		p.start()

	for p in proc:
       		p.join()


