__version__ = '0.1.0'

import Config as cfg
import os
import time
import math


class BottyMcBotFace(object):
    def __init__(self, serial_device):
        self.serial_device = serial_device

        self.configure_feather()
        

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

    def zero(self):
        self.serial_device.command('G92 X0 Y0')

    def enable(self):
        self.serial_device.command('M17')

    def disable(self):
        self.serial_device.command('M84')

    def absolute_move(self, xpos_mm, ypos_mm, zpos_mm, velocity_mmps=None):
        """ I move da motorz """
        # Send gcode
        self.x_target = xpos_mm
        self.y_target = ypos_mm
        self.z_target = zpos_mm
        command = 'G1 X{} Y{} Z{}'.format(self.x_target, self.y_target, self.z_target)
        if velocity_mmps is not None:
            command += ' F{}'.format(velocity_mmps * 60)
        self.serial_device.command(command)

    def relative_move(self, xpos_mm = 0, ypos_mm = 0, zpos_mm = 0, velocity_mmps = None):
        self.x_target += xpos_mm
        self.y_target += ypos_mm
        self.z_target += zpos_mm
        self.absolute_move(self.x_target, self.y_target, self.z_target, velocity_mmps)

    def get_current_pos():
        """ Returns current position array [x, y, z] """
        ret = self.serial_device.command('M114')
        return [float(i) for i in ret.split(',')]
