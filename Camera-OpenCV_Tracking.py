# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 19:45:56 2020

@author: Angus
"""
import os 
import cv2
import matplotlib.pyplot as plt
import numpy as np

Scene1Cap = cv2.VideoCapture(os.getcwd()+"/TrainingData/slowdot.mov")
Scene2Cap = cv2.VideoCapture(os.getcwd()+"/TrainingData/slowdotrev.mov")

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
ax.scatter([14], [14], [14], color="k", s=1)

Point1 = ax.scatter([0], [0], [0], color="b", s=25)
Point2 = ax.scatter([0], [0], [0], color="b", s=25)
Point3 = ax.scatter([0], [0], [0], color="b", s=25)

while Scene1Cap.isOpened():
    Scene1Ok, Scene1FrameCheck = Scene1Cap.read()
    Scene2Ok, Scene2FrameCheck = Scene2Cap.read()

    if not Scene1Ok or not Scene2Ok:
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


    #----------------Scene Frame Marking----------------
    for Scene1Contour, Scene2Contour in zip(Scene1Contours,Scene2Contours): 
        (Scene1x, Scene1y, Scene1w, Scene1w) = cv2.boundingRect(Scene1Contour)
        (Scene2x, Scene2y, Scene2w, Scene2w) = cv2.boundingRect(Scene2Contour)
        Point1.remove()
        Point2.remove()
        Point3.remove()
        #Dumb offsets because input video isn't real
        Scene1x = Scene1x/100
        Scene1y = 14-(Scene1y/100)
        Scene2x = 14-(Scene2x/100)
        Scene2y = Scene2y/100
        #Delete above
        Point1 = ax.scatter(0, Scene1y, Scene1x, color="g", s=25)
        Point2 = ax.scatter(Scene2x, Scene2y, 0, color="r", s=25)
        Point3 = ax.scatter(Scene2x, ((Scene1y+Scene2y)/2), Scene1x, color="b", s=25)
    #----------------Scene Display----------------
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