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

#目標画像を以下のディレクトリに格納
path = "./rename"
files = glob.glob(path + '/*.png')
print(files)
#class-0000.pngの形式になるように設定
#例：11-0001.png,クラス:11
for i, f in enumerate(files):
	os.rename(f, os.path.join(path,'testdata' + '{0:04d}'.format(i) + ".png"))


				

