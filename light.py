import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def contrast_img(img1, c, b):
    rows, cols, channels = img1.shape

    blank = np.zeros([rows, cols, channels], img1.dtype)
    dst = cv2.addWeighted(img1, c, blank, 1-c, b)
    return dst

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', required=True)

args = parser.parse_args()
dataset = args.dataset

for number in os.listdir(dataset):
	num_path = os.path.join(dataset, number)
	print("Processing dataset: '%s'" %num_path)

	for filename in os.listdir(num_path):
		last = filename.split('.')[-1]
		if last != 'png':
			continue
		filepath = os.path.join(num_path, filename)
		print(filepath)
		img = cv2.imread(filepath)
		img_ = contrast_img(img, 10, 3)
		cv2.rectangle(img_, (160, 160), (560, 560), (0, 255, 0), 2)
		new_filename = "new-" + filename
		new_filepath = os.path.join(num_path, new_filename)
		cv2.imwrite(new_filepath, img_)
