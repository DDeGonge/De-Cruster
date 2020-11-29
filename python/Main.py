__version__ = '0.1.0'

import time
import argparse
import Config as cfg
from SerialDevice import *
from MotorDriver import BottyMcBotFace
from CameraDriver import *
from SpeakerDriver import *
from Modes import *


def main():
    parser = argparse.ArgumentParser(description='HOLY HECK I made a robot that chops stuff.')
    parser.add_argument('-m', type=int, default=0, help='Operational Mode - 0: De-Crust, 1: Chop, 2: Dice, 3: Finger Sammy, 4: Safety Keyboard')
    parser.add_argument('-n', type=int, default=8, help='Number of finger sammys to cut. Must be even')
    parser.add_argument('-w', type=float, default=3, help='Slicing thickness in mm')
    args = parser.parse_args()

    # try:
    s = Speaker()
    c = Camera()
    c.start()

    sd = SerialDevice()
    bot = BottyMcBotFace(sd)

    # Enter operational mode
    if cfg.DEBUG_MODE:
        print('Starting...')
        
    bot.home()

    if args.m == 0:
        decrust_mode(bot, c, s)
    elif args.m == 1:
        chop_mode(bot, c, s, args.w)
    elif args.m == 2:
        dice_mode(bot, c, s, args.w)
    elif args.m == 3:
        decrust_mode(bot, c, s, sammy_mode=True, n_pieces=args.n)
    elif args.m == 4:
        safety_mode(bot, c, s)

    bot.home()

                
    # except Exception as e:
    #     c.stop()
    #     bot.disable()
    #     raise e

    # finally:
    #     c.stop()
    #     bot.disable()

def motors():
    sd = SerialDevice()
    bot = BottyMcBotFace(sd)
    bot.home()

    move = 70
    bot.relative_move(x=10)
    for i in range(100, 600, 50):
        bot.relative_move(x=move, velocity_mmps=i)
        move *= -1

def fastmoves():
    sd = SerialDevice()
    bot = BottyMcBotFace(sd)
    bot.home()

    time.sleep(3)
    bot.relative_move(x=30, y=0.3)

def speakers():
    s = Speaker()
    s.play_tea()
    time.sleep(10)

def find_center():
    from math import pi
    sd = SerialDevice()
    bot = BottyMcBotFace(sd)
    bot.home()
    bot.absolute_move(x=70)

def test_chop():
    sd = SerialDevice()
    bot = BottyMcBotFace(sd)
    bot.home()

    c_pos = 10
    c_inc = 2
    while True:
        bot.absolute_move(x=c_pos)
        bot.chop()
        c_pos += c_inc
        c_inc *= 0.8


if __name__=='__main__':
    main()
    # find_center()
    # test_chop()
    # motors()
    # fastmoves()
