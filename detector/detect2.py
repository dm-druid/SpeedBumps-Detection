import cv2
import numpy as np
import math
from darknet2.darknet import detect_np

dist = np.array([-0.347049837762688,
		  0.165398310868444,
                  0,
                  0,
		 -0.0444392622226221])

mtx = np.array([[366.8414,        0, 337.4132],
		[       0, 366.1242, 182.8138],
		[       0,        0,   1.0000]])

mat = np.array([[-0.5115,   -1.4774,  428.8531],
                [-0.0880,   -3.6296,  847.1490],
                [-0.0001,   -0.0054,    1.0000]
               ])

def pointInBirdsEyeView(p):
    p2 = mat.dot(p)
    p2 /= p2[2]
    return p2

pLeft = pointInBirdsEyeView([0,426,1])
pRight = pointInBirdsEyeView([640,426,1])
d = 126
pix2cm = 1

# y = kx + b
k = (pLeft[1] - pRight[1])/(pLeft[0] - pRight[0])
b = pLeft[1] - k*pLeft[0]
def distance2BottomLine(p):
    # |kx+b-y| / sqrt(k^2 + 1)
    # if the distance < 0, input point is invalid
    # return unit: pix
    return (k*p[0] + b - p[1]) / math.sqrt(k**2 + 1)


def distanceOf2Points(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# cm
def distance2Camera(p):
    p = [p[0],p[1],1]
    p = pointInBirdsEyeView(p)
    ds = distance2BottomLine(p)
    if ds < 0:
        return -1
    else:
        return ds * pix2cm + d


# im: numpy array n*m*3
red = (0, 0, 255)
blue = (0,255,0)

def detect_and_draw(im):
    im = cv2.undistort(im, mtx, dist, None, None)
    res = detect_np(im)
    for item in res:
        if item[1] < 0.8:
            continue
        x = item[2][0]
        y = item[2][1]
        w = item[2][2]
        h = item[2][3]
        # print(item[0])
        if item[0] == b'bump':
            color = red
        else:
            color = blue
        distance = distance2Camera([x,y+h/2])
        distance = math.floor(distance)
        distance /= 100
        if distance < 1:
            distance = ""
        im = cv2.rectangle(im, (int(x - w/2),int(y - h/2)), (int(x + w/2),int(y + h/2)), color, 2)
        im = cv2.putText(im, str(distance), (int(x-w/2),int(y-h/2-5)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,cv2.LINE_AA)
    return im

cap = cv2.VideoCapture("bump.mov")
fps = cap.get(cv2.CAP_PROP_FPS)  
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),   
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) 

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output3.mp4',fourcc, 30.0, size)
count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
    	break
    frame = detect_and_draw(frame)
    out.write(frame)
    count += 1
    print(count)

cap.release()
out.release()

