# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:48:40 2020

@author: Angus
"""

import numpy as np
import cv2

cap=cv2.VideoCapture('C:/Users/Angus/Downloads/opencv/sources/samples/data/flydots.avi')

old_frame = None

while True:

    ret, frame = cap.read()

    if ret == True:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if old_frame is not None:
            diff_frame = gray - old_frame
            diff_frame -= diff_frame.min()
            disp_frame = np.uint8(300.0*diff_frame/float(diff_frame.max()))
            cv2.imshow('diff_frame',disp_frame)
        old_frame = gray

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
        
        k = cv2.waitKey(1) & 0xff
        if k == 27 :
            break

    else:
        print('ERROR!')
        break

cap.release()
cv2.destroyAllWindows()