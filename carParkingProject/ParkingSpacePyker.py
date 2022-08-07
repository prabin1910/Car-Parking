
import cv2
import pickle

 
width, height = 105, 47
 
try:
    with open('carparkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []
 
 
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
 
    with open('carparkPos','wb') as f:
        pickle.dump(posList, f)
 
 
while True:
    img = cv2.imread('carpark.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (139, 81, 265), 2)
 
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    cv2.waitKey(1)