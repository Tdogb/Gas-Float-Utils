import random, time, datetime, csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from multiprocessing import Process, Manager
import odrive
from odrive.enums import *
from collections import deque
import numpy as np

numRolls = 300
running = True
odrv = None
max_data_points = 40
x_data = None
y_data = None
line = None

logging_hz = 200
control_hz = 1000
time_window = 4
def animate_plot(times, engine_pos, engine_vel, motor_pos, motor_vel, motor_current):
    fig = plt.figure(figsize=(10,6))
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    plt.subplots_adjust(top=0.93, bottom=0.07, hspace=0.3)
    ax1.clear()
    l1, = ax1.plot(engine_vel, lw=1)

    ax2.clear()
    l2, = ax2.plot(motor_vel, lw=1)

    ax3.clear()
    l3, = ax3.plot([motor_vel[i] - engine_vel[i] for i in range(len(motor_vel))], lw=1)

    ax4.clear()
    l4, = ax4.plot(motor_current, lw=1)

    def animate(i):
        # l1.set_data(range(len(engine_vel)),engine_vel)
        # l2.set_data(range(len(motor_vel)),motor_vel)
        # l3.set_data(range(len(motor_vel)),[motor_vel[i] - engine_vel[i] for i in range(len(motor_vel))])
        # l4.set_data(range(len(motor_current)),motor_current)
        ax1.clear()
        l1, = ax1.plot(engine_vel, lw=1)

        ax2.clear()
        l2, = ax2.plot(motor_vel, lw=1)

        ax3.clear()
        l3, = ax3.plot([motor_pos[i] - engine_pos[i] for i in range(len(motor_pos))], lw=1)

        ax4.clear()
        l4, = ax4.plot(motor_current, lw=1)
        ax1.set_title("Engine Velocity")
        ax2.set_title("Motor Velocity")
        ax3.set_title("Motor-Engine Pos")
        ax4.set_title("Max Current")

    ani = animation.FuncAnimation(fig, animate, frames=numRolls, interval=50, repeat=False)
    plt.show()

def update_data(times, engine_pos, engine_vel, motor_pos, motor_vel, motor_current):
    desired_vel = 0
    average_engine_vel = []
    average_motor_vel = []
    average_motor_current = []
    print("finding an odrive...")
    odrv0 = odrive.find_any()
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    print("motor enabled")
    last_log_loop_time = time.time_ns()
    last_loop_time = time.time_ns()
    while running:
        if 1e-9*(time.time_ns()-last_loop_time) >= 1/control_hz:
            pos_engine = (18/64)*odrv0.axis1.encoder.pos_estimate
            pos_motor = odrv0.axis0.encoder.pos_estimate
            vel_engine = (18/64)*odrv0.axis1.encoder.vel_estimate
            vel_motor = odrv0.axis0.encoder.vel_estimate
            odrv0.axis0.controller.input_vel = -(vel_engine + desired_vel)
            average_engine_vel.append(vel_engine)
            average_motor_vel.append(vel_motor)
            average_motor_current.append(odrv0.axis0.motor.I_bus)
            time_now = time.time_ns()
            if 1e-9*(time_now-last_log_loop_time) > 1/logging_hz:
                last_log_loop_time = time_now
                times.append(time_now*1e-9)
                engine_pos.append(pos_engine)
                engine_vel.append(np.mean(average_engine_vel))
                motor_pos.append(pos_motor)
                motor_vel.append(np.mean(average_motor_vel))
                motor_current.append(np.max(average_motor_current))
                average_engine_vel = []
                average_motor_vel = []
                average_motor_current = []
                times.pop(0)
                engine_pos.pop(0)
                engine_vel.pop(0)
                motor_pos.pop(0)
                motor_vel.pop(0)
                motor_current.pop(0)
            last_loop_time = time_now
            loop_on_time = False
            continue
        else:
            loop_on_time = True
        if not loop_on_time:
            print("LOOP BEHIND by: " + str(1e-9*(time.time_ns()-last_loop_time)))

if __name__ == "__main__":
    with Manager() as manager:
        times = manager.list([0]*time_window*logging_hz)
        engine_pos = manager.list([0]*time_window*logging_hz)
        engine_vel = manager.list([0]*time_window*logging_hz)
        motor_pos = manager.list([0]*time_window*logging_hz)
        motor_vel = manager.list([0]*time_window*logging_hz)
        motor_current = manager.list([0]*time_window*logging_hz)

        plot_process = Process(target=animate_plot, args=(times, engine_pos, engine_vel, motor_pos, motor_vel, motor_current))
        data_process = Process(target=update_data, args=(times, engine_pos, engine_vel, motor_pos, motor_vel, motor_current))
        try:
            plot_process.start()
            data_process.start()

            plot_process.join()
            data_process.join()
        finally:
            name = input("Type name to log data")
            if not (name.lower() == ""):
                with open(name + " - " + datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S") + ".csv", 'w') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["Time", "Motor Vel", "Engine Vel", "Motor-Engine Vel", "Current"])
                    for i,t in enumerate(times):
                        try:
                            writer.writerow([t,motor_vel[i], engine_vel[i], motor_vel[i]-engine_vel[i], motor_current[i]])
                        except :
                            pass