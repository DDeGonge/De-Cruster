__version__ = '0.1.0'

import time
import argparse
import Config as cfg
from SerialDevice import *
from MotorDriver import BottyMcBotFace
from CameraDriver import *
from Modes import *


def main():
    parser = argparse.ArgumentParser(description='HOLY HECK I made a robot that chops stuff.')
    parser.add_argument('-m', type=int, default=0, help='Operational Mode - 0: Default, 1: TBD, 2: TBD, 3: TBD')
    args = parser.parse_args()

    # try:
    c = Camera()
    c.start()

    sd = SerialDevice()
    bot = BottyMcBotFace(sd)

    # Enter operational mode
    while True:
        if cfg.DEBUG_MODE:
            print('Starting...')
        
        # TODO setup stuff here


        if args.m == 0:
            decrust_mode(bot, c)
        elif args.m == 1:
            chop_mode()
        elif args.m == 2:
            dice_mode()
        elif args.m == 3:
            finger_mode()

                
    # except Exception as e:
    #     c.stop()
    #     bot.disable()
    #     raise e

    # finally:
    #     c.stop()
    #     bot.disable()


if __name__=='__main__':
    main()