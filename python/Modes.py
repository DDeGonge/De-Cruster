# from gpiozero import Button, LED
import time
import Config as cfg
import math
import cv2


def rotatePoint(point, angle_rads):
    cos = math.cos(angle_rads)
    sin = math.sin(angle_rads)
    (x, y) = point
    new_x = x*cos - y*sin
    new_y = x*sin + y*cos
    return (new_x, new_y)


def decrust_mode(bot, c, loser_mode=False):
    """ Waits for sammich then cuts off the crust and plays a snarky tune """
    c.save_empty_scene()
    c.wait_for_object()
    x_center, y_center, x_len, y_len, rot = c.locate_object()

    # Prepare rotations to perform
    rotations = [-rot, math.pi/2, math.pi/2, math.pi/2]
    center_offsets = [x_len / 2, y_len / 2, x_len / 2, y_len / 2]

    for this_rot, this_offset in zip(rotations, center_offsets):
        # Calculate where sammy center is after rotation
        (new_x, new_y) = rotatePoint((x_center, y_center), this_rot)

        # Line up the knife, aaaannnnddd
        cutline_x = new_x - this_offset
        bot.absolute_move(x=knife_zero_offset_mm - cutline_x, y=this_rot)

        # CHOP!
        print("CHOP")

        # Rotate all points for sanity checking
        # boxpts = cv2.boxPoints(((x_center, y_center), (x_len, y_len), rot * 180 / math.pi))
        # print("PREROT", boxpts)
        # newpts = [rotatePoint(p, -rot) for p in boxpts]
        # print("NEWPTS", newpts)
