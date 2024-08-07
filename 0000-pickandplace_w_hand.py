#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: this is just an example template
    1. Instantiate XArmAPI and specify do_not_open to be true
    2. Registration error callback function
    3. Connect
    4. Enable motion
    5. Setting mode
    6. Setting state
"""

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################


def hangle_err_warn_changed(item):
    print('ErrorCode: {}, WarnCode: {}'.format(item['error_code'], item['warn_code']))
    # TODO：Do different processing according to the error code


arm = XArmAPI(ip, do_not_open=True)
arm.register_error_warn_changed_callback(hangle_err_warn_changed)
arm.connect()

# enable motion
arm.motion_enable(enable=True)
# set mode: position control mode
arm.set_mode(0)
# set state: sport state
arm.set_state(state=0)

## Pieza 1

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)


# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Pick
arm.set_position(x=-62.5, y=305.3, z=-51.2, roll=-178.9, pitch=-0.1, yaw=-167.2, speed=30, wait=True)

arm.set_cgpio_digital(5, 1, delay_sec=0)

# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)

# Place
arm.set_position(x=322.3, y=-49.2, z=-88.8, roll=-176.2, pitch=0.6, yaw=89.6, speed=30, wait=True)
arm.set_cgpio_digital(5, 0, delay_sec=0)


## Pieza 2

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)


# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Pick
arm.set_position(x=-62.5, y=305.3, z=-51.2, roll=-178.9, pitch=-0.1, yaw=-167.2, speed=30, wait=True)

arm.set_cgpio_digital(5, 1, delay_sec=0)

# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)

# Relativo
arm.set_position(y=-80.2, relative=True, wait=True)

# Relativo place
arm.set_position(z=-70.3, relative=True, wait=True)
arm.set_cgpio_digital(5, 0, delay_sec=0)
arm.set_position(z=70.3, relative=True, wait=True)


## Pieza 3

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)


# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Pick
arm.set_position(x=-62.5, y=305.3, z=-51.2, roll=-178.9, pitch=-0.1, yaw=-167.2, speed=30, wait=True)

arm.set_cgpio_digital(5, 1, delay_sec=0)

# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)

# Relativo
arm.set_position(x=-80.2, relative=True, wait=True)

# Relativo place
arm.set_position(z=-70.3, relative=True, wait=True)
arm.set_cgpio_digital(5, 0, delay_sec=0)
arm.set_position(z=70.3, relative=True, wait=True)

## Pieza 4

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)


# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Pick
arm.set_position(x=-62.5, y=305.3, z=-51.2, roll=-178.9, pitch=-0.1, yaw=-167.2, speed=30, wait=True)

arm.set_cgpio_digital(5, 1, delay_sec=0)

# Above Pick
arm.set_servo_angle(angle=[101.5, -21.8, -23.5, 0.1, 46.4, 268.6], speed=30, mvacc=500, wait=True)

# Home
arm.set_servo_angle(angle=[-8.6, -19.6, -18.5, -0.1, 34.2, 261.8], speed=30, mvacc=500, wait=True)

# Relativo
arm.set_position(x=-80.2, y=-80.2, relative=True, wait=True)

# Relativo place
arm.set_position(z=-70.3, relative=True, wait=True)
arm.set_cgpio_digital(5, 0, delay_sec=0)
arm.set_position(z=70.3, relative=True, wait=True)


time.sleep(5)

arm.disconnect()
