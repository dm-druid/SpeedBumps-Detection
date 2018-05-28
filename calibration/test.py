# -*- coding:utf-8 -*-
# python 2.7
import cv2
import numpy as np

# 畸变参数
dist = np.array([-0.347049837762688,
				  0.165398310868444,
				                  0,
				                  0,
				-0.0444392622226221])

# 内参矩阵
mtx = np.array([[366.8414,        0, 337.4132],
				[       0, 366.1242, 182.8138],
				[       0,        0,   1.0000]])

img = cv2.imread("test.jpg")
h, w = img.shape[:2]  
dst = cv2.undistort(img,mtx,dist,None,None)
cv2.imwrite("test-output.jpg",dst)