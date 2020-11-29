# from gpiozero import Button, LED
import time
import Config as cfg
import numpy as np
import math
import cv2


def rotatePoint(point, angle_rads):
    cos = math.cos(angle_rads)
    sin = math.sin(angle_rads)
    (x, y) = point
    new_x = x*cos - y*sin
    new_y = x*sin + y*cos
    return (new_x, new_y)


def decrust_mode(bot, c, s, sammy_mode = False, n_pieces = 0):
    """ Waits for sammich then cuts off the crust and plays a snarky tune """
    c.save_empty_scene()
    c.wait_for_object()
    x_center, y_center, x_len, y_len, rot = c.locate_object()

    # Prepare rotations to perform
    rotations = [-rot, math.pi/2, math.pi/2, math.pi/2]
    center_offsets = [x_len / 2, y_len / 2, x_len / 2, y_len / 2]
    r_total = 0

    extra_cuts = [[],[],[],[]]

    if sammy_mode:
        cuts = int(n_pieces/2) - 1
        spacing = (x_len - 2 * cfg.crust_thickness_mm) / (cuts + 1)
        cuts0 = int(cuts/2)
        cuts2 = cuts - cuts0
        extra_cuts[0] = [spacing * (i + 1) for i in range(cuts0)]
        extra_cuts[2] = [spacing * (i + 1) for i in range(cuts2)]
        extra_cuts[3] = [(y_len / 2) - cfg.crust_thickness_mm]

        s.play_tea()

    for this_rot, this_offset, moar_cuts in zip(rotations, center_offsets, extra_cuts):
        r_total += this_rot
        # Calculate where sammy center is after rotation
        (new_x, new_y) = rotatePoint((x_center, y_center), r_total)

        # Line up the knife, aaaannnnddd
        cutline_x = cfg.knife_zero_offset_mm + new_x - this_offset + cfg.crust_thickness_mm
        bot.absolute_move(x=cutline_x, y=r_total)

        # CHOP!
        bot.bread_cut()

        # cut extra ones if needed
        for mc in moar_cuts:
            bot.absolute_move(x=cutline_x + mc)
            bot.bread_cut()

    # To ensure fair evaluation.
    s.play_scorereq()
    score = input("Enter score: ")
    s.play_thanks()
    if int(score) < 10:
        bot.home()
        while True:
            xloc = c.find_first_move() + cfg.knife_zero_offset_mm
            bot.absolute_move(x=xloc)
            bot.chop()
            s.play_sarcasm()
            bot.absolute_move(z=0)
            bot.absolute_move(x=0)


def chop_mode(bot, c, s, width_mm):
    """ Locates object and chops it up """
    c.save_empty_scene()
    c.wait_for_object()
    x_center, y_center, x_len, y_len, rot = c.locate_object()

    # Rotate scene
    r_total = -rot
    (new_x, new_y) = rotatePoint((x_center, y_center), r_total)
    if x_len > y_len:
        fulllen = x_len
    else:
        fulllen = y_len
        r_total += (math.pi / 2)
    (new_x, new_y) = rotatePoint((x_center, y_center), r_total)

    # If center of object is far away, spin 180
    if new_x > 0:
        r_total -= math.pi
        (new_x, new_y) = rotatePoint((x_center, y_center), r_total)

    bot.absolute_move(y=r_total)

    # Chop it up
    c_pos = cfg.knife_zero_offset_mm + new_x - (fulllen / 2) + width_mm
    c_end = c_pos + fulllen
    while c_pos < c_end:
        bot.absolute_move(x=c_pos)
        bot.chop()
        c_pos += width_mm

    s.play_chop()

def dice_mode(bot, c, s, width_mm):
    """ Locates object and chops it up """
    c.save_empty_scene()
    c.wait_for_object()
    x_center, y_center, x_len, y_len, rot = c.locate_object()

    # Rotate scene
    r_total = -rot
    (new_x, new_y) = rotatePoint((x_center, y_center), r_total)
    if new_x > 0:
        r_total += math.pi
        (new_x, new_y) = rotatePoint((x_center, y_center), r_total)
    bot.absolute_move(y=r_total)

    # Chop it up
    c_pos = cfg.knife_zero_offset_mm + new_x - (x_len / 2) + width_mm
    c_end = c_pos + x_len
    while c_pos < c_end:
        bot.absolute_move(x=c_pos)
        s.play_thud()
        bot.chop()
        c_pos += width_mm

    # Rotate again
    r_total += math.pi/2
    (new_x, new_y) = rotatePoint((x_center, y_center), r_total)
    bot.absolute_move(y=r_total)

    # Chop again
    c_pos = cfg.knife_zero_offset_mm + new_x - (y_len / 2) + width_mm
    c_end = c_pos + y_len
    while c_pos < c_end:
        bot.absolute_move(x=c_pos)
        s.play_thud()
        bot.chop()
        c_pos += width_mm

def safety_mode(bot, c, s):
    s.play_safety_start()

    while True:
        # Enter reddit patrol loop
        if c.is_reddit_there():
            bot.absolute_move(x=60)
            bot.absolute_move(z=80)
            bot.absolute_move(z=60)
            bot.absolute_move(z=80)
            bot.absolute_move(z=0)
            s.play_safety_end()
            s.wait_for_sound_to_end()
            return
