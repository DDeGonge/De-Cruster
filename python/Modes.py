# from gpiozero import Button, LED
import time
import Config as cfg


def decrust_mode(bot, c, loser_mode=False):
    """ Waits for sammich then cuts off the crust and plays a snarky tune """
    c.save_empty_scene()
    c.wait_for_object()
    x_center, y_center, x_len, y_len, rot = c.locate_object()
    
    # Rotate so edge is aligned with knife. Transform corner points to follow
    
