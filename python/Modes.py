from gpiozero import Button, LED
import time
import Config as cfg


def decrust_mode(bot, c, loser_mode=False):
    """ Waits for sammich then cuts off the crust and plays a snarky tune """
    c.wait_for_object()

    

