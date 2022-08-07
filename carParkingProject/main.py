  
import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

 
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 105, 47

 
 
def checkParkingSpace(imgPro):
    
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        #  cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y + height-5),scale=1.6, thickness=2 , offset=0, colorR=(139, 81, 265)) 
         
        if count < 1200:
            color = (0, 255, 0)
            thickness = 3
            spaceCounter +=1
        else:
            color = (0, 0, 255)
            thickness = 3
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
       
                        
    cvzone.putTextRect(img, f'{spaceCounter}/{len(posList)}', (110, 45), scale=3, thickness=4, offset=25, colorR=(0, 185, 0))

while True:
    
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (1,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 139, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 23, 14)
    imgMedian = cv2.medianBlur(imgThreshold, 3)
    kernel = np.ones((1,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=3)
 
    checkParkingSpace( imgDilate)
    cv2.imshow("image", img)
    # cv2.imshow("imageBlur", imgBlur)
    # cv2.imshow("imageThres", imgMedian)
    cv2.waitKey(5)