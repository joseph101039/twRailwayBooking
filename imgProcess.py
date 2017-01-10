from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from time import sleep
import os.path
############## 2. Sice the image into 5 or 6 pieces ###############

def read_image(img_path, try_count = 10):
	for i in xrange(try_count):
		if os.path.isfile(img_path):
			img = Image.open(img_path)
			return img
		sleep(0.07)
	return None


def slice_img_into_six_pieces(img, reWid = 17, reHei = 30):
	top = 0
	bottom = 60
	img = img.convert('L')			#convert into gray-scale
	img = img.filter(ImageFilter.MedianFilter(3)) 	# use median filter to de-noise
	enhancer = ImageEnhance.Contrast(img)	#increase contrast
	img = enhancer.enhance(2)
	enhancer = ImageEnhance.Sharpness(img) 	#sharpness
	img = enhancer.enhance(2)
	enhancer = ImageEnhance.Brightness(img) 	#increase lightness
	img = enhancer.enhance(2)
	img1 = img.crop((0, top, 36, bottom)).resize((reWid, reHei), Image.BILINEAR)	#crop((left, top, right, bottom))
	img2 = img.crop((36, top, 67, bottom)).resize((reWid, reHei), Image.BILINEAR)
	img3 = img.crop((67, top, 97, bottom)).resize((reWid, reHei), Image.BILINEAR)
	img4 = img.crop((97, top, 128, bottom)).resize((reWid, reHei), Image.BILINEAR)
	img5 = img.crop((128, top, 160, bottom)).resize((reWid, reHei), Image.BILINEAR)
	img6 = img.crop((160, top, 193, bottom)).resize((reWid, reHei), Image.BILINEAR)
	return [img1, img2, img3, img4, img5, img6]



	# 5 slices for 5 digits
def slice_img_into_five_pieces(img, reWid = 17, reHei = 30):
	top = 0
	bottom = 60
	img = img.convert('L')			#convert into gray-scale
	img = img.filter(ImageFilter.MedianFilter(3)) 	# use median filter to de-noise
	enhancer = ImageEnhance.Contrast(img)	#increase contrast
	img = enhancer.enhance(2)
	enhancer = ImageEnhance.Sharpness(img) 	#sharpness
	img = enhancer.enhance(2)
	enhancer = ImageEnhance.Brightness(img) 	#increase lightness
	img = enhancer.enhance(2)
	img1 = img.crop((0, top, 40, bottom)).resize((reWid, reHei), Image.BILINEAR)	#crop((left, top, right, bottom))
	img2 = img.crop((40, top, 80, bottom)).resize((reWid, reHei), Image.BILINEAR)
	img3 = img.crop((80, top, 117, bottom)).resize((reWid, reHei), Image.BILINEAR)
	img4 = img.crop((117, top, 156, bottom)).resize((reWid, reHei), Image.BILINEAR)
	img5 = img.crop((156, top, 196, bottom)).resize((reWid, reHei), Image.BILINEAR)
	return [img1, img2, img3, img4, img5]

# larger slice image is 30 * 50
def slice_training_img(reWid = 17, reHei = 30, ans_path = "/home/joseph/Captcha/ImageOut_value.txt", img_src = "/home/joseph/Captcha/tmp/", img_dest = "/home/joseph/Captcha/tmp_slice/"):
	#start = 0, end = 3000
	img_value = []
	with open(ans_path , 'r') as vr:
		content = vr.read().splitlines() #[img_index, img_vlaue] for every element
		content = [c.split(',') for c in content]

	for i in xrange(len(content)):
		img_index = content[i][0]
		img_value = content[i][1]
		img = Image.open(img_src + 'img' + img_index + '.jpg')

		if len(img_value) == 5:
			img_arr = slice_img_into_five_pieces(img, reWid, reHei)
			for j in xrange(5):
				img_arr[j].save(img_dest + 'img' + img_index + '_' + str(j + 1) + '.jpg')

		elif len(img_value) == 6:
			img_arr = slice_img_into_six_pieces(img, reWid, reHei)
			for j in xrange(6):
				img_arr[j].save(img_dest + 'img' + img_index + '_' + str(j + 1) + '.jpg')
		else:
			print "Image value error: img "+  str(i) + ".jpg length is wrong!"
