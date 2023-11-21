import odrive
from odrive.enums import *
import time, csv
'''
The plan:
- When at load, we try to keep engine rpms up and motor rpms down to use mostly gas
- Use odrive as dyno
- Start with two electric motors, make sure code works
- float_thd is the main loop in float.c
- float package is pid controller on the angle vs setpoint, and the output of the controller goes to the torque command. Line 1863
'''

ratio_motor = 1
ratio_engine = 1
initilize_odrive()
[pos,vel] = calculate_pos_vel(engine_sign=1,motor_sign=1)
setpoint_vel = calculate_setpoint_from_vesc()
[motor_rpm_setpoint, engine_rpm_setpoint] = decide_motor_engine_mix(setpoint_vel)

def motor_feedforward():
    command_latency = 1 #ms
    ...

def decide_motor_engine_mix(setpoint_vel):
    engine_min_rpm = 1500
    ratio = constrain(M*setpoint_vel+b,0,1)
    if ratio < 0:
        ratio = 1 #all motor
    return ratio

def control_motor_rpm(vel_command):
    odrv0.axis0.vel_setpoint = vel_command

def control_engine_rpm(vel_command):
    rpm = odrv0.axis1.encoder.vel_estimate
    e = vel_command-rpm
    feedforward = M*rpm + b
    output = PID(e) + feedforward
    #run PID at low update rate
    servo.set_angle(output)

def calculate_setpoint_from_vesc():
    return 1

def differential_equation_with_ratio(motor,engine):
    return ratio_motor*motor - ratio_engine*engine

def calculate_pos_vel(engine_sign, motor_sign):
    pos_M = odrv0.axis0.encoder.pos_estimate
    pos_E = odrv0.axis1.encoder.pos_estimate
    vel_M = odrv0.axis0.encoder.vel_estimate
    vel_E = odrv0.axis1.encoder.vel_estimate
    _pos = differential_equation_with_ratio(pos_M, pos_E)
    _vel = differential_equation_with_ratio(vel_M, vel_E)
    return [_pos, _vel]

def initilize_odrive():
    print("finding an odrive...")
    odrv0 = odrive.find_any()
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    print("motor enabled")