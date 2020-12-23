# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 19:45:56 2020

@author: Angus
"""
import cv2

Scene1Cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
Scene1Cap.set(cv2.CAP_PROP_FPS, 30.0)
Scene1Cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
Scene1Cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
Scene1Cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
Scene1Cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

ret, Scene1Frame1 = Scene1Cap.read()
ret, Scene1Frame2 = Scene1Cap.read()
print(Scene1Frame1.shape)

while Scene1Cap.isOpened():
    ok, Scene1FrameCheck = Scene1Cap.read()
    if not ok:
        break
    

    #----------------Scene 1 Differential----------------
    Scene1Diff = cv2.absdiff(Scene1Frame1, Scene1Frame2)
    Scene1Gray = cv2.cvtColor(Scene1Diff, cv2.COLOR_BGR2GRAY)
    Scene1Blur = cv2.GaussianBlur(Scene1Gray, (5,5), 0)
    Scene1_, Scene1Thresh = cv2.threshold(Scene1Blur, 50, 255, cv2.THRESH_BINARY)
    Scene1Dilated = cv2.dilate(Scene1Thresh, None, iterations=3)
    Scene1Contours, Scene1_ = cv2.findContours(Scene1Dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #----------------Scene 1 Frame Marking----------------
    for Scene1Contour in Scene1Contours:
        (Scene1x, Scene1y, Scene1w, Scene1w) = cv2.boundingRect(Scene1Contour)
        if cv2.contourArea(Scene1Contour) < 100 or cv2.contourArea(Scene1Contour) > 500:
            continue
        cv2.rectangle(Scene1Frame1, (Scene1x, Scene1y), (Scene1x+Scene1w, Scene1y+Scene1w), (0, 255, 0), 2)
        cv2.putText(Scene1Frame1, str(int(Scene1x))+","+str(int(Scene1y)), (Scene1x, Scene1y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    #----------------Scene 1 Feed----------------
    cv2.namedWindow("Scene1Feed",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Scene1Feed", 960,540)
    cv2.imshow("Scene1Feed", Scene1Frame1)
    Scene1Frame1 = Scene1Frame2
    ret, Scene1Frame2 = Scene1Cap.read()

    
    Scene1Kill = cv2.waitKey(1) & 0xff
    if Scene1Kill == 27 :
        break
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

Scene1Cap.release()
cv2.destroyAllWindows()