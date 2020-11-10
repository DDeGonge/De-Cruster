__version__ = '0.1.0'

import Config as cfg
import os
import time
import math


class BottyMcBotFace(object):
    def __init__(self, serial_device):
        self.serial_device = serial_device

        self.configure_feather()

        self.x_target = 0
        self.y_target = 0
        self.z_target = 0
        

    """ Motion stuff """

    def configure_feather(self):
        self.set_steps_per_mm(cfg.x_step_per_mm, cfg.y_step_per_mm, cfg.z_step_per_mm)
        self.set_accelerations(cfg.x_default_accel_radps2, cfg.y_default_accel_radps2, cfg.z_default_accel_radps2)
        self.set_velocities(cfg.x_default_vel_radps, cfg.y_default_vel_radps, cfg.z_default_vel_radps)

    def set_steps_per_mm(self, x_spm, y_spm, z_spm):
        self.serial_device.command('M92 X{} Y{} Z{}'.format(x_spm, y_spm, z_spm))

    def set_accelerations(self, xaccel, yaccel, zaccel):
        self.serial_device.command('M201 X{} Y{} Z{}'.format(xaccel, yaccel, zaccel))

    def set_velocities(self, xvel, yvel, zvel):
        self.serial_device.command('C0 X{} Y{} Z{}'.format(xvel, yvel, zvel))

    def home_x(self):
        self.serial_device.command('G28 X')

    def home_y(self):
        self.serial_device.command('G28 Y')

    def home_z(self):
        self.serial_device.command('G28 Z')

    def home(self):
        self.serial_device.command('G28 Z')
        self.serial_device.command('G28 X')
        self.serial_device.command('G92 Y0')

    def zero(self):
        self.serial_device.command('G92 X0 Y0 Z0')

    def enable(self):
        self.serial_device.command('M17')

    def disable(self):
        self.serial_device.command('M84')

    def absolute_move(self, x = None, y = None, z = None, velocity_mmps=None):
        """ I move da motorz """
        # Send gcode
        if x is not None:
            self.x_target = x
        if y is not None:
            self.y_target = y
        if z is not None:
            self.z_target = z

        command = 'G1 X{} Y{} Z{}'.format(self.x_target, self.y_target, self.z_target)
        if velocity_mmps is not None:
            command += ' F{}'.format(velocity_mmps * 60)
        print(command)
        self.serial_device.command(command)

    def relative_move(self, x = 0, y = 0, z = 0, velocity_mmps = None):
        self.absolute_move(self.x_target + x, self.y_target + y, self.z_target + z, velocity_mmps)

    def get_current_pos(self):
        """ Returns current position array [x, y, z] """
        ret = self.serial_device.command('M114')
        return [float(i) for i in ret.split(',')]
