import odrive
from odrive.enums import *
import time, csv

print("finding an odrive...")
odrv0 = odrive.find_any()
time_setpoints = []
vel_setpoints = []
vel_real = []
with open('vel_time_series_rippin.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        time_setpoints.append(float(row[0]))
        vel_setpoints.append(float(row[1]))
print(vel_setpoints)
dt = (time_setpoints[len(time_setpoints)-1] - time_setpoints[0]) / len(time_setpoints)
print(dt)
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
print("motor enabled")
time.sleep(0.2)
for i in range(len(time_setpoints)):
    odrv0.axis0.controller.input_vel = vel_setpoints[i]
    vel_real.append(odrv0.axis0.encoder.vel_estimate)
    time.sleep(1e-9 * dt)
print("Writing csv")
with open('vel_motor_vs_engine.csv', 'w', newline='') as csvfile:
     writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
     for i in range(len(vel_real)):
         writer.writerow([time_setpoints[i], vel_setpoints[i], vel_real[i], vel_setpoints[i]-vel_real[i]])
odrv0.axis0.requested_state = AXIS_STATE_IDLE