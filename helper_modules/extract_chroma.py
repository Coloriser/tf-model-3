import numpy as np
import skimage.color as color
import skimage.io as io
from PIL import Image

def extract_a_channel(image_path):
	img_test = Image.open(image_path)
	img_rgb = io.imread(image_path)
	if(img_test.mode != 'L' ):
		img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
		img_l = img_lab[:,:,1] # pull out A channel	
		return img_l
	else:
		print("Image already in L")
		return


def extract_b_channel(image_path):
	img_test = Image.open(image_path)
	img_rgb = io.imread(image_path)
	if(img_test.mode != 'L' ):
		img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
		img_l = img_lab[:,:,2] # pull out B channel	
		return img_l
	else:
		print("Image already in L")
		return	

def extract_l_channel(image_path):
	img_test = Image.open(image_path)
	img_rgb = io.imread(image_path)
	if(img_test.mode != 'L' ):
		img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
		img_l = img_lab[:,:,0] # pull out L channel	
	else:
		print("Image already in L")
		img_l = img_rgb
	return img_l