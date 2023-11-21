import odrive
from odrive.enums import *
import time, csv

print("finding an odrive...")
odrv0 = odrive.find_any()
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis0.controller.input_torque = -1.5
input()
odrv0.axis0.controller.input_torque = 0