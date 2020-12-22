# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 19:45:56 2020

@author: Angus
"""
import cv2

#Scene1Cap = cv2.VideoCapture("C:/Users/Angus/Downloads/opencv/sources/samples/data/flydots.avi")
#Scene1Cap = cv2.VideoCapture("C:/Users/Angus/Downloads/opencv/sources/samples/data/mouse.avi")
#Scene1Cap = cv2.VideoCapture("C:/Users/Angus/Downloads/opencv/sources/samples/data/vtest.avi")
Scene1Cap = cv2.VideoCapture("C:/Users/Angus/Downloads/opencv/sources/samples/data/slowdot.mov")
Scene2Cap = cv2.VideoCapture("C:/Users/Angus/Downloads/opencv/sources/samples/data/slowdotrev.mov")

ret, Scene1Frame1 = Scene1Cap.read()
ret, Scene1Frame2 = Scene1Cap.read()
print(Scene1Frame1.shape)

ret, Scene2Frame1 = Scene2Cap.read()
ret, Scene2Frame2 = Scene2Cap.read()
print(Scene2Frame1.shape)

while Scene1Cap.isOpened():
    ok, Scene1FrameCheck = Scene1Cap.read()
    if not ok:
        break
    
    
    #----------------Scene 1 Differential----------------
    Scene1Diff = cv2.absdiff(Scene1Frame1, Scene1Frame2)
    Scene1Gray = cv2.cvtColor(Scene1Diff, cv2.COLOR_BGR2GRAY)
    Scene1Blur = cv2.GaussianBlur(Scene1Gray, (5,5), 0)
    Scene1_, Scene1Thresh = cv2.threshold(Scene1Blur, 20, 255, cv2.THRESH_BINARY)
    Scene1Dilated = cv2.dilate(Scene1Thresh, None, iterations=3)
    Scene1Contours, Scene1_ = cv2.findContours(Scene1Dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #----------------Scene 2 Differential----------------
    Scene2Diff = cv2.absdiff(Scene2Frame1, Scene2Frame2)
    Scene2Gray = cv2.cvtColor(Scene2Diff, cv2.COLOR_BGR2GRAY)
    Scene2Blur = cv2.GaussianBlur(Scene2Gray, (5,5), 0)
    Scene2_, Scene2Thresh = cv2.threshold(Scene2Blur, 20, 255, cv2.THRESH_BINARY)
    Scene2Dilated = cv2.dilate(Scene2Thresh, None, iterations=3)
    Scene2Contours, Scene2_ = cv2.findContours(Scene2Dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    #----------------Scene 1 Frame Marking----------------
    for Scene1Contour in Scene1Contours:
        (Scene1x, Scene1y, Scene1w, Scene1w) = cv2.boundingRect(Scene1Contour)
        if cv2.contourArea(Scene1Contour) < 900:
            continue
        cv2.rectangle(Scene1Frame1, (Scene1x, Scene1y), (Scene1x+Scene1w, Scene1y+Scene1w), (0, 255, 0), 2)
        cv2.putText(Scene1Frame1, str(int(Scene1x))+","+str(int(Scene1y)), (Scene1x, Scene1y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    #----------------Scene 2 Frame Marking----------------
    for Scene2Contour in Scene2Contours:
        (Scene2x, Scene2y, Scene2w, Scene2w) = cv2.boundingRect(Scene2Contour)
        if cv2.contourArea(Scene2Contour) < 900:
            continue
        cv2.rectangle(Scene2Frame1, (Scene2x, Scene2y), (Scene2x+Scene2w, Scene2y+Scene2w), (0, 255, 0), 2)
        cv2.putText(Scene2Frame1, str(int(Scene2x))+","+str(int(Scene2y)), (Scene2x, Scene2y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    
    #----------------Scene 1 Feed----------------
    cv2.namedWindow("Scene1Feed",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Scene1Feed", 400,400)
    cv2.imshow("Scene1Feed", Scene1Frame1)
    Scene1Frame1 = Scene1Frame2
    ret, Scene1Frame2 = Scene1Cap.read()
    #----------------Scene 2 Feed----------------
    cv2.namedWindow("Scene2Feed",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Scene2Feed", 400,400)
    cv2.imshow("Scene2Feed", Scene2Frame1)
    Scene2Frame1 = Scene2Frame2
    ret, Scene2Frame2 = Scene2Cap.read()
    
    
    Scene1Kill = cv2.waitKey(1) & 0xff
    if Scene1Kill == 27 :
        break
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

Scene1Cap.release()
Scene2Cap.release()  
cv2.destroyAllWindows()