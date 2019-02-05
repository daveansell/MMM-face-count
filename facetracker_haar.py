#!/usr/bin/env python

"""
Modified from code posted here: http://forums.pimoroni.com/t/pan-tilt-hat-repo/3402/11
"""
import numpy as np
import cv2.cv as cv
import os
import time
import sys
#from pantilthat import *

os.system('sudo modprobe bcm2835-v4l2')

cascade = cv.Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
cascade2 = cv.Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
#cascade = cv.Load('/usr/share/opencv/lbpcascades/lbpcascade_frontalface.xml')

cam_pan = 90
cam_tilt = 45
print "facetracker"
# Turn the camera to the default position
#pan(cam_pan-90)
#tilt(cam_tilt-90)
#light_mode(WS281raspbbbbbbbpython 
#def lights(r,g,b,w):
 #   for x in range(18):
 #       set_pixel_rgbw(x,r if x in [3,4] else 0,g if x in [3,4] else 0,b,w if x in [0,1,6,7] else 0)
#    show()

#lights(0,0,0,50)

min_size = (15, 15)
image_scale = 3#5
haar_scale = 1.2
min_neighbors = 2
haar_flags = cv.CV_HAAR_DO_CANNY_PRUNING

cap = cv.CreateCameraCapture(0)
#cv.NamedWindow("Tracker", 1)
 
if cap:
    frame_copy = None
frame_copy=False 
    # Capture frame-by-frame

def detectFaces():
    global frame_copy, min_size, image_scale, haar_scale, min_neighbors, haar_flags, cap, cam_pan, cam_tilt
    t0 = cv.GetTickCount()
    frame = cv.QueryFrame(cap)
    if not frame:
        cv.WaitKey(0)
        return False
    if not frame_copy:
        frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
    if frame.origin == cv.IPL_ORIGIN_TL:
        cv.Flip(frame, frame, -1)
   
    # Our operations on the frame come here
    gray = cv.CreateImage((frame.width,frame.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(frame.width / image_scale),
                   cv.Round (frame.height / image_scale)), 8, 1)
    small_img2 = cv.CreateImage((cv.Round(frame.width / image_scale),
                   cv.Round (frame.height / image_scale)), 8, 1)
    # convert color input image to grayscale
    cv.CvtColor(frame, gray, cv.CV_BGR2GRAY)
 
    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)
 
    cv.EqualizeHist(small_img, small_img)

    #flip the image for more convenient camera mounting
    cv.Flip(small_img,small_img2,-1)

    midFace = None
    t1 = cv.GetTickCount()
 
    if(cascade):
        t = cv.GetTickCount()
        # HaarDetectObjects takes 0.02s
        faces = cv.HaarDetectObjects(small_img2, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        if faces:
            #lights(50 if len(faces) == 0 else 0, 50 if len(faces) > 0 else 0,0,50)

            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
 #               cv.Rectangle(frame, pt1, pt2, cv.RGB(100, 220, 255), 1, 8, 0)
                # get the xy corner co-ords, calc the midFace location
                x1 = pt1[0]
                x2 = pt2[0]
                y1 = pt1[1]
                y2 = pt2[1]

                midFaceX = x1+((x2-x1)/2)
                midFaceY = y1+((y2-y1)/2)
                midFace = (midFaceX, midFaceY)

                offsetX = midFaceX / float(frame.width/2)
                offsetY = midFaceY / float(frame.height/2)
                offsetX -= 1
                offsetY -= 1

                cam_pan -= (offsetX * 5)
                cam_tilt += (offsetY * 5)
                cam_pan = max(0,min(180,cam_pan))
                cam_tilt = max(0,min(180,cam_tilt))

                print(offsetX, offsetY, midFace, cam_pan, cam_tilt, frame.width, frame.height)
                sys.stdout.flush()
 #               pan(int(cam_pan-90))
  #              tilt(int(cam_tilt-90))
                #break
 #   print "e"+str((t1-t0)/1000000)+"-"+str( (cv.GetTickCount()-t1)/1000000)
#    cv.ShowImage('Tracker',frame)
    if cv.WaitKey(1) & 0xFF == ord('q'):
        return False
    return True
ret=True
while(ret):
    ret=detectFaces()
  #  time.sleep(0.1)
    # Display the resulting frame

# When everything done, release the capture
#cv.DestroyWindow("Tracker")
