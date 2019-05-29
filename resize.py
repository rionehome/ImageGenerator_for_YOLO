#Python3で実行
import os
import glob
import sys
try:
	sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
	pass
import cv2
abspath = os.path.dirname(os.path.abspath(__name__))

#リサイズしたい解像度を指定
width = 300
height = 300

#リサイズしたい画像をしたのディレクトリに格納
path = "./resize"
files = glob.glob(path + '/*.png')#画像の形式


print(files)
for i ,f in enumerate(files):
	print(f)
	img = cv2.imread(str(f), cv2.IMREAD_UNCHANGED)
	nimg = cv2.resize(img, (width, height))
	cv2.imwrite(str(f), nimg)

