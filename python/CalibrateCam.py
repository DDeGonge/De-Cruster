__version__ = '0.1.0'

from CameraDriver import * 
import Config as cfg
import cv2

BW_THRESH = 100

minsize = 0
maxsize = 5000
dot_spacing_mm = 7.8


def calibrate():
    c = Camera()
    c.start()

    frame = c.get_frame()
    _, frame_thresh = cv2.threshold(frame, BW_THRESH, 255, cv2.THRESH_BINARY)
    frame_thresh = cv2.bitwise_not(frame_thresh)
    _, contours, _ = cv2.findContours(frame_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours_filt = [cn for cn in contours if cv2.contourArea(c) > minsize and cv2.contourArea(c) < maxsize]
    bboxes = [cv2.boundingRect(cn) for cn in contours_filt]

    centers = [(x + w/2, y + h/2) for (x, y, w, h) in bboxes]
    
    for cn in centers:
        print(cn)

    c._save_image(frame_thresh, "cal_bw.jpg")


if __name__=='__main__':
    calibrate()