import odrive
from odrive.enums import *
import time, json, datetime, csv, sched
import easygui
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")  # Use the TkAgg backend for thread-safe updates
import multiprocessing
from collections import deque
import numpy as np

running = True
odrv = None
max_data_points = 40
x_data = None
y_data = None
line = None
engine_pos = deque([])
engine_vel = deque([])
motor_pos = deque([])
motor_vel = deque([])
motor_current = deque([])
fig, ax = plt.subplots()

logging_hz = 40
control_hz = 1000

def liveplot():
    while True:
        line.set_ydata(list(engine_vel))
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.1)

def main():
    desired_vel = 0
    average_engine_vel = []
    average_motor_vel = []
    average_motor_current = []
    while running:
        loop_on_time = False
        if 1e-9*(time.time_ns()-last_loop_time) > 1/1000:
            pos_engine = odrv0.axis1.encoder.pos_estimate
            pos_motor = odrv0.axis0.encoder.pos_estimate
            vel_engine = odrv0.axis1.encoder.vel_estimate
            vel_motor = odrv0.axis0.encoder.vel_estimate
            odrv0.axis0.controller.input_vel = -(vel_engine + desired_vel)
            average_engine_vel.append(vel_engine)
            average_motor_vel.append(vel_motor)
            average_motor_current.append(odrv0.axis0.motor.I_bus)
            if 1e-9*(time.time_ns()-last_log_loop_time) > 1/40:
                last_log_loop_time = time.time_ns()
                engine_pos.append(pos_engine)
                engine_vel.append(np.mean(average_engine_vel))
                motor_pos.append(pos_motor)
                motor_vel.append(np.mean(average_motor_vel))
                motor_current.append(np.mean(average_motor_current))
                average_engine_vel = []
                average_motor_vel = []
                average_motor_current = []
            last_loop_time = time.time_ns()
        else:
            loop_on_time = True
        if not loop_on_time:
            print("LOOP BEHIND")

if __name__ == "__main__":
    max_data_points = logging_hz * 2
    engine_pos = deque(maxlen=max_data_points)
    engine_vel = deque(maxlen=max_data_points)
    motor_pos = deque(maxlen=max_data_points)
    motor_vel = deque(maxlen=max_data_points)
    motor_current = deque(maxlen=max_data_points)
    x_data = list(range(max_data_points))
    y_data = [0] * max_data_points
    line, = ax.plot(x_data, y_data)
    print("finding an odrive...")
    odrv0 = odrive.find_any()
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    print("motor enabled")
    graph_process = multiprocessing.Process(target=liveplot)
    main_process = multiprocessing.Process(target=main)
    main_process.start()
    graph_process.start()
    plt.show()