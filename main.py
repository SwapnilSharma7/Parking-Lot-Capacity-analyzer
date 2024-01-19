import cv2
import numpy as np
import cvzone
import pickle
# Video feed
cap = cv2.VideoCapture('C:/Users/lenovo/Downloads/CarParkProject/carPark.mp4')
width,height = 107,48
# now getting the position from the marked one in images.
with open ('carParkPos','rb') as f: # rb read permission.
            posList = pickle.load(f) # no need to try and expect as we already know the pos excists

def CheckParkingSpace(imgPro):
      spacecounter = 0
      for pos in posList:
            x,y = pos
            imgCrop = imgPro[y:y+height,x:x+width]
            # cv2.imshow(str(x*y),imgCrop)\
            count = cv2.countNonZero(imgCrop)
            if count<900: # score below 800 will be considered as the empty parking lot.
                  color = (0,255,0)
                  thickness = 5
                  spacecounter+=1 # empty slot add 1.
            else :
                  color = (0,0,255)
                  thickness = 2
                  # spacecounter-=1 # occupied add 1
            cv2.rectangle (img,pos,(pos[0]+width,pos[1]+height),color,thickness)
            cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset = 0,colorR=color) # to count the number of white pixels.
      cvzone.putTextRect(img,f'Free: {spacecounter}/ {len(posList)}',(100,50),scale=3,thickness=5,offset = 20,colorR=(0,200,0))
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT): # if the current frame is equal to the number of frames or the last frame
        cap.set(cv2.CAP_PROP_POS_FRAMES,0) # setting the frame back to zero to loop the video
    success,img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)# converting the image to gray scale.
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1) # Blurring the image. To reduce the image noise and detail. Here we have used the
    # 3X3 gaussian kernel and standard deviation of 1 in X direction.
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,25,16) # converting into black and white pixels image.
    # black and white pixel image is like white outline on black background.
    # to remove white dots here and there.Using Median Bluring. Please check for different types of blurring.
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1) # to dilate the image or increasing the number of pixels. Increasing the number of white pixels.
    CheckParkingSpace(imgDilate)
    cv2.imshow("Image",img)
    cv2.waitKey(10)