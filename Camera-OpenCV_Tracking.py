# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 19:45:56 2020

@author: Angus
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

Scene1Cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
Scene1Cap.set(cv2.CAP_PROP_FPS, 30.0)
Scene1Cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
Scene1Cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
Scene1Cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
Scene1Cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

Scene2Cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
Scene2Cap.set(cv2.CAP_PROP_FPS, 30.0)
Scene2Cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m','j','p','g'))
Scene2Cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
Scene2Cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
Scene2Cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

ret, Scene1Frame1 = Scene1Cap.read()
ret, Scene1Frame2 = Scene1Cap.read()
print(Scene1Frame1.shape)
ret, Scene2Frame1 = Scene2Cap.read()
ret, Scene2Frame2 = Scene2Cap.read()
print(Scene2Frame1.shape)

x, y, z = np.indices((15, 15, 15))
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter([0], [0], [0], color="k", s=1)
ax.scatter([1080], [1080], [1080], color="k", s=1)

Point1 = ax.scatter([0], [0], [0], color="b", s=25)
Point2 = ax.scatter([0], [0], [0], color="b", s=25)
Point3 = ax.scatter([0], [0], [0], color="b", s=25)

while Scene1Cap.isOpened():
    
    #----------------Scene 1 Differential----------------
    Scene1Diff = cv2.absdiff(Scene1Frame1, Scene1Frame2)
    Scene1Gray = cv2.cvtColor(Scene1Diff, cv2.COLOR_BGR2GRAY)
    Scene1Blur = cv2.GaussianBlur(Scene1Gray, (5,5), 0)
    Scene1_, Scene1Thresh = cv2.threshold(Scene1Blur, 50, 255, cv2.THRESH_BINARY)
    Scene1Dilated = cv2.dilate(Scene1Thresh, None, iterations=3)
    Scene1Contours, Scene1_ = cv2.findContours(Scene1Dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #----------------Scene 2 Differential----------------
    Scene2Diff = cv2.absdiff(Scene2Frame1, Scene2Frame2)
    Scene2Gray = cv2.cvtColor(Scene2Diff, cv2.COLOR_BGR2GRAY)
    Scene2Blur = cv2.GaussianBlur(Scene2Gray, (5,5), 0)
    Scene2_, Scene2Thresh = cv2.threshold(Scene2Blur, 50, 255, cv2.THRESH_BINARY)
    Scene2Dilated = cv2.dilate(Scene2Thresh, None, iterations=3)
    Scene2Contours, Scene2_ = cv2.findContours(Scene2Dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    #----------------Scene Frame Marking----------------
    for Scene1Contour in Scene1Contours:
        if cv2.contourArea(Scene1Contour) < 100 or cv2.contourArea(Scene1Contour) > 1000:
            continue
        (Scene1x, Scene1y, Scene1w, Scene1w) = cv2.boundingRect(Scene1Contour)
        Point1.remove()
        Point1 = ax.scatter(0, Scene1y, Scene1x, color="g", s=25)
        cv2.rectangle(Scene1Frame1, (Scene1x, Scene1y), (Scene1x+Scene1w, Scene1y+Scene1w), (0, 255, 0), 2)
        cv2.putText(Scene1Frame1, str(int(Scene1x))+","+str(int(Scene1y)), (Scene1x, Scene1y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    for Scene2Contour in Scene2Contours:
        if cv2.contourArea(Scene2Contour) < 100 or cv2.contourArea(Scene2Contour) > 1000:
            continue
        (Scene2x, Scene2y, Scene2w, Scene2w) = cv2.boundingRect(Scene2Contour)
        Point2.remove()
        Point3.remove()
        Point2 = ax.scatter(Scene2x, Scene2y, 0, color="r", s=25)
        Point3 = ax.scatter(Scene2x, ((Scene1y+Scene2y)/2), Scene1x, color="b", s=25)
        cv2.rectangle(Scene2Frame2, (Scene2x, Scene2y), (Scene2x+Scene2w, Scene2y+Scene2w), (0, 255, 0), 2)
        cv2.putText(Scene2Frame2, str(int(Scene2x))+","+str(int(Scene2y)), (Scene2x, Scene2y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    
    #----------------Scene Display----------------
    cv2.namedWindow("Scene1Feed",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Scene1Feed", 960,540)
    cv2.imshow("Scene1Feed", Scene1Frame1)
    
    cv2.namedWindow("Scene2Feed",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Scene2Feed", 960,540)
    cv2.imshow("Scene2Feed", Scene2Frame2)
    
    
    Scene1Frame1 = Scene1Frame2
    ret, Scene1Frame2 = Scene1Cap.read()
    Scene2Frame1 = Scene2Frame2
    ret, Scene2Frame2 = Scene2Cap.read()
    
    Scene1Kill = cv2.waitKey(1) & 0xff
    if Scene1Kill == 27 :
        break
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    
    plt.draw()

Scene1Cap.release()
Scene2Cap.release()  
cv2.destroyAllWindows()