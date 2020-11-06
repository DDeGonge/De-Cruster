__version__ = '0.1.0'

import sys
import time
import os
import cv2
from PIL import Image
import atexit
import Config as cfg
import numpy as np
import subprocess as sp


class Camera(object):
    def __init__(self, resolution=cfg.video_resolution):
        self.cameraProcess = None
        self.resolution = resolution
        self.is_enabled = False

        self.locked_on = False
        self.tlast = 0

        # pic dump stuff
        self.frame_n = 0
        self.pic_type = ''

        # Setup stuff
        self.tracker = cv2.TrackerKCF_create()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    @staticmethod
    def _display_image(img):
        cv2.imshow("Image", img)
        cv2.waitKey(0)


    @staticmethod
    def _save_image(img, impath):
        im = Image.fromarray(img)
        im.save(os.path.join(cfg.saveimg_path, impath))


    def start(self):
        self.cap = cv2.VideoCapture(0)

        # Set resolution
        w, h = self.resolution
        self.cap.set(3,w)
        self.cap.set(4,h)
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, 40)
        # self.cap.set(cv2.CAP_PROP_FPS, 40)


    def stop(self):
        self.cap.release()


    def get_frame(self):
        _, img = self.cap.read()
        img[:,:,2] = np.zeros([img.shape[0], img.shape[1]])  # Remove red channel so laser can stay on
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        r_gray = cv2.rotate(gray, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rblur_gray = cv2.GaussianBlur(r_gray, (21, 21), 0)

        if cfg.SAVE_FRAMES:
            self.frame_n += 1
            self._save_image(rblur_gray, '{}.jpg'.format(self.frame_n))

        return rblur_gray

    def wait_for_object(self):
        """ Waits until motion is detected then stops """
        start_frame = get_frame()
        nextframe_time = time.time() + (1 / cfg.check_video_fps)

        # Wait for motion start
        while True:
            # Wait before capturing next frame
            while time.time() < nextframe_time:
                pass
            nextframe_time += (1 / cfg.check_video_fps)

            # Capture frame and compare to start frame
            next_frame = get_frame()
            diff_img = cv2.absdiff(next_frame, start_frame)
            if (np.sum(diff_img)/255) > cfg.motion_start_min_percent:
                break

        last_frame = get_frame()
        consecutive_still_frames = 0

        # Wait for motion end
        while True:
            # Wait before capturing next frame
            while time.time() < nextframe_time:
                pass
            nextframe_time += (1 / cfg.check_video_fps)

            # Capture frame and compare to previous frame
            next_frame = get_frame()
            diff_img = cv2.absdiff(next_frame, last_frame)
            last_frame = next_frame
            if (np.sum(diff_img)/255) > cfg.motion_stop_max_percent:
                consecutive_still_frames = 0
            else:
                consecutive_still_frames += 1

            if consecutive_still_frames > (cfg.check_video_fps * cfg.motion_stop_time):
                break

    def locate_sammy(self):
        img = self.get_frame()
        _, contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_sorted = sorted(contours, key=cv2.contourArea, reverse=True)

        # Convert largest contour to bounding box
        largest_bbox = cv2.minAreaRect(contours_sorted[0])
        if cfg.DEBUG_MODE:
            print(largest_bbox)
            # samich = img[y:y+h, x:x+w]
            # self._save_image(samich, 'samich_{}.jpg'.format(self.frame_n))
        return 


    def find_face(self):
        frame = self.get_frame()
        faces = self.face_cascade.detectMultiScale(frame, 1.2, 6)

        tnow = time.time()
        if cfg.DEBUG_MODE:
            print("Face Detection - {} fps".format(1 / (tnow - self.tlast)))
            self.tlast = tnow

        if len(faces) > 0:
            [a, b, c, d] = faces[0]
            return (a, b, c, d)
        return None


    def show_frame(self, frame):
        (w,h) = self.resolution
        frame.shape = (h,w) # set the correct dimensions for the numpy array
        cv2.imshow("skrrt", frame)


if __name__=='__main__':
    c = Camera()
    c.start()
    try:
        print('Camera started')
        # while True:
        #     _ = c.get_frame()

        c.lock_on()
        print('Locked on')

        while True:
            h, w = c.get_location()
    
    finally:
        c.stop()
