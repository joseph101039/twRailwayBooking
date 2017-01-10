 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import subprocess
import os
from PIL import Image

class AnyEc:
	def __init__(self, *args):
		self.ecs = args
	def __call__(self, driver):
		for fn in self.ecs:
			try:
				if fn(driver): return True
			except:
				pass

def fast_select(driver, element_id, label):
	select = Select(driver.find_element_by_id(element_id))
	select.select_by_value(label)

def getin_date_select(driver, element_id, label):
	select = Select(driver.find_element_by_id(element_id))
	for option in select.options:
		value = option.get_attribute('value')
		if label in value:
			option.click()
			return True
	return False



#firefox將geckodriver 存放至 /usr/local/bin/ 路徑下即可
def init_browser():
	browser = webdriver.Chrome('/home/joseph/railwayLink/chromedriver')
	return browser

def link_to_web(browser, url):
	browser.get(url)


def input_order_data_and_submit(browser, person_id, from_station, to_station, getin_date, train_no, order_qty_str):
	browser.find_element_by_id("person_id").send_keys(person_id)
	fast_select(browser, 'from_station', from_station)
	fast_select(browser, 'to_station', to_station)
	
	getin_date_select(browser, 'getin_date', getin_date)
	browser.find_element_by_id("train_no").send_keys(train_no)
	fast_select(browser, 'order_qty_str', order_qty_str)
	
	BUTTON_XPATH = '//button[@type="submit"]'
	button = browser.find_element_by_xpath(BUTTON_XPATH)
	button.click()


def get_captcha_image(browser, img_name):
	IMG_XPATH = '//img[@id="idRandomPic"]'
	img = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, IMG_XPATH)))	#delay at most 2 seconds
	location = img.location
	size = img.size
	browser.save_screenshot("/home/joseph/下載/" + img_name + '.png') # saves screenshot of entire page
	snap = Image.open("/home/joseph/下載/" + img_name + '.png')
	left = int(location['x'])
	top = int(location['y'])
	right = int(location['x']) + size['width']
	bottom = int(location['y']) + size['height']
	#snap.save("/home/joseph/下載/" + img_name + '.jpg', "JPEG", quality=100, optimize=True, progressive=True)
	return snap.crop((int(left), int(top), int(right), int(bottom)))
	


def send_captcha_value(browser, value):
	browser.find_element_by_id("randInput").send_keys(value)


def submit_captcha_value(browser):
	button = browser.find_element_by_id("sbutton")
	button.click()

def recaptcha(browser):
	try:
		title = _find_title_text_orange02(browser = browser, delay = 5)
		if title == False:
			print "Cannot  find_title_text_orange02"
			return [False, 4]

		result_msg = title.text.encode('utf-8')
		if result_msg == "亂數驗證失敗":		#element.text is unicode type
			BUTTON_XPATH = '//input[@type="submit"]'
			button = browser.find_element_by_xpath(BUTTON_XPATH)
			button.click()
			return [True, 1]
		elif result_msg == "車次號碼錯誤，請再次確認":		#element.text is unicode type
			return [False, 2]
		elif result_msg == "您的車票已訂到":
			return [False, 3]
	except TimeoutException:
		print "TimeoutException: sec. Cannot find_title_text_orange02"
		return [False, 4]




def quit_browser(browser):
	browser.quit()

def _find_title_text_orange02(browser, delay):
	#有2類title, font class 或是 p class
	if(WebDriverWait(browser, delay).until(AnyEc(EC.presence_of_element_located((By.CLASS_NAME, 'orange02')),EC.presence_of_element_located((By.XPATH, "//font[@class='organe02']/strong"))))):
		try:
			title = browser.find_element_by_class_name('orange02')
			return title
		except:
			try:
				title = browser.find_element_by_xpath("//font[@class='orange02']/strong")
				return title
			except:
				return False
	else:
		return False


def cancel_order(browser):
	BUTTON1_XPATH = '//button/img[@src="./Images/delete02_a.jpg"]'
	button = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, BUTTON1_XPATH)))
	button.click()
	BUTTON2_XPATH = '//button/img[@src="./Images/delete03_a.jpg"]'
	button = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, BUTTON2_XPATH)))
	button.click()
	try:
		title = _find_title_text_orange02(browser, 3).text.encode('utf-8')
		result_msg = title.text.encode('utf-8')
		if result_msg == "您的車票取消成功":
			return True
		else:
			return False
	except:
		return False
