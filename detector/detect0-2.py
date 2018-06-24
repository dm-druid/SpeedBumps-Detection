import cv2
import numpy as np
import math
from keras.models import model_from_json
import json
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

def computeLineFun(p1, p2):
    k = (p1[1] - p2[1]) / (p1[0] - p2[0])
    b = p1[1] - k*p1[0]
    return (k,b)

def distance2CameraXqq(leftp, rightp):
    p1 = pointInBirdsEyeView([leftp[0],leftp[1],1])
    p2 = pointInBirdsEyeView([rightp[0],rightp[1],1])
    line = computeLineFun(p1, p2)
    print(line)
    x = 273.5925925925924
    y = 672.148148148148
    return -(line[0] * x + line[1] - y) / math.sqrt(line[0] ** 2 + 1)

json_string = ""
with open("model.json",'r') as json_file:
    json_string = json_file.read()

model = model_from_json(json_string)
model.load_weights('weights.h5')

def predict(img):
    img = cv2.resize(img,(100,100))
    res = model.predict(np.array([img]))
    res = np.where(res == np.max(res))[1][0]
    return res

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

        x_min = max(0,(int(x - w/2)))
        x_max = min(im.shape[1]-1,int(x + w/2))
        y_min = max(0,int(y - h/2))
        y_max = min(im.shape[1]-1,int(y + h/2))

        bbox = im[y_min:y_max,x_min:x_max,:]
        res = predict(bbox)
        # lefe-top -> right-bottom
        if color == red:
            if res == 0:
                distance = distance2CameraXqq([x_min,y_min],[x_max,y_max])
            else:
                distance = distance2CameraXqq([x_min,y_max],[x_max,y_min])
        else:
            distance = distance2Camera([x,y+h/2])

        distance = math.floor(distance)
        distance /= 100
        if distance < 1:
            distance = ""
        im = cv2.rectangle(im, (x_min,y_min), (x_max,y_max), color, 2)
        im = cv2.putText(im, str(distance), (x_min,y_min-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,cv2.LINE_AA)
    return im



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="image path to detect")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
im2 = detect_and_draw(img)
cv2.imwrite(str(int(time.time())) + '.png', im2)

