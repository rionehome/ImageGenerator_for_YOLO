""""backgroundに背景画像，itemsに物体画像を入れてPython3で実行"""
from time import sleep
import sys
#ROSのCV2とpython3のCV2がコンフリクトする人向け
try:
	sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
	pass
import cv2
import numpy as np
import glob
from lib.image_generator import *
from lib.yolabelgenerator import *


print("loading Ri-one generator...")
#合成後のデータセットの解像度,実際の環境に合わせる(Kinect-h:480w:640)
input_width = 640 
input_height = 480


item_path = "./items/"#合成したい物体のパス
background_path = "./backgrounds/"#合成先の背景のパス
Generate_folder = "./output/"#合成後のデータセットを格納するディレクトリ
seriesname = "sample_"
#合成後のデータセットの頭に付くファイル名
#ラベルをファイルの頭に付けて分離したほうがやりやすい(0クラスなら:0data_)


# "label-"でラベルを分離する．(0-file.pngのような形式)
generator = ImageGenerator(item_path, background_path, split_class="-")

sets = 10  # セット数の指定(n_sample/sets)
n_samples = 50 #1セットに作成する画像枚数
n_items = 2 # 1画像中に合成する物体の数

#それぞれ0でそのまま
delta_hue = 0.0  #HSV空間における色相の変化量
delta_sat_scale = 0.0  #HSV空間における彩度の変化量
delta_val_scale = 0.0  #HSV空間における明度の変化量

min_item_scale = 1.0  # 物体の縮小率
max_item_scale = 1.0 # 物体の拡大率
rand_angle = 1  # 物体の回転角度
minimum_crop = 0.85
range_of_overlay = [[0, 480], [80, 415]]  #物体生成の範囲制限[[xmin,xmax],[ymin,ymax]]
generate_once = True


def restrict_value_in_image(anno, width, height):
	xmin = max(anno[0], 0)
	xmax = min(anno[1], width)
	ymin = max(anno[2], 0)
	ymax = min(anno[3], height)
	return [xmin, xmax, ymin, ymax]


def get_annotation_value(box):
	#box_x,box_y,box_w,box_hs
	x = box[1]
	y = box[2]
	w = box[3]
	h = box[4]
	xmin = int(x - w / 2)
	xmax = int((x + w / 2))
	ymin = int(y - h / 2)
	ymax = int((y + h / 2))
	return [xmin, xmax, ymin, ymax]


def get_classname(filename):
	classname = filename.split("-")[0]
	return classname


number = 1
for set in range(sets):
	# generate random sample
	x, t = generator.generate_samples(
		n_samples=n_samples,
		n_items=n_items,
		crop_width=input_width,
		crop_height=input_height,
		min_item_scale=min_item_scale,
		max_item_scale=max_item_scale,
		rand_angle=rand_angle,
		minimum_crop=minimum_crop,
		delta_hue=delta_hue,
		delta_sat_scale=delta_sat_scale,
		delta_val_scale=delta_val_scale,
		range_of_overlay=range_of_overlay,
		generate_once=generate_once
	)
	for i, image in enumerate(x):
		image = np.transpose(image, (1, 2, 0)).copy()
		dataname = seriesname + "{}".format(number)
		imagename = dataname + ".png"
		anofolder = Generate_folder + "obj/"
		TXTpath = anofolder + dataname + ".txt"  # YOLO用のラベルパスの定義
		if not os.path.isdir(anofolder):
			os.makedirs(anofolder)
		width, height, _ = image.shape
		for truth_box in t[i]:
			box_x, box_y, box_w, box_h = truth_box['x'], truth_box['y'], truth_box['w'], truth_box['h']
			classname = truth_box['classname']
			box = [classname, box_x, box_y, box_w, box_h]
			#print(box)
			anno = get_annotation_value(box)
			anno = restrict_value_in_image(anno, input_width, input_height)
			# YOLO用のラベル形式を作成
			writeyolabel(TXTpath, dataname, box)
		image = (image * 255).astype('uint8')
		Imagefolder = Generate_folder + "obj/"
		Imagepath = Imagefolder + dataname + ".png"
		if not os.path.isdir(Imagefolder):
			os.makedirs(Imagefolder)
		cv2.imwrite(Imagepath, image * 255)
		number = number + 1
	print("Set " + str(set + 1) + " Done.")
	sleep(5)#落ちるので止める
print("Generate Finished.")
