import odrive
from odrive.enums import *
import time, json, datetime, csv, sched
import easygui
import matplotlib.pyplot as plt
'''
The plan:
- When at load, we try to keep engine rpms up and motor rpms down to use mostly gas
- 
'''

ratio_motor = 1
ratio_engine = 1

def main():
    # choice = easygui.choicebox("am","title",["run", "plot"])
    choice = "run"
    if choice == "run":
        print("finding an odrive...")
        odrv0 = odrive.find_any()
        odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        odrv0.axis0.motor.config.torque_constant = 82.27/270
        print("motor enabled")
        desired_vel = 0
        vels_motor = []
        vels_engine = []
        times = []
        currents = []
        try:
            start_time = time.time_ns()
            last_loop_time = start_time
            while True:
                vel_engine = odrv0.axis1.encoder.vel_estimate
                vel_motor = odrv0.axis0.encoder.vel_estimate
                odrv0.axis0.controller.input_vel = -(vel_engine + desired_vel)
                if 1e-9*(time.time_ns()-last_loop_time) > 1/40:
                    times.append(time.time_ns()-start_time)
                    vels_engine.append(vel_engine)
                    currents.append(odrv0.axis0.motor.I_bus)
                    vels_motor.append(vel_motor)
                    last_loop_time = time.time_ns()
                    # print("Engine: " + str(round(vel_engine,5)) + " Motor: " + str(round(vel_motor,5)))
                time.sleep(1/1000)
        finally:
            odrv0.axis0.requested_state = AXIS_STATE_IDLE
            dictionary = {
                "test time": datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S"),
                "data": {
                    "velocity setpoint": desired_vel,
                    "motor vel": vels_motor,
                    "engine vel": vels_engine,
                    "times": times,
                    "motor current": currents,
                },
            }
            json_out = json.dumps(dictionary, indent=4)
            with open(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S") + "motor vs engine vel data.json", 'w') as outfile:
                outfile.write(json_out)
            print("Json written")
            with open(datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S") + "motor vs engine vel data.csv", 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i,t in enumerate(times):
                    try:
                        writer.writerow([t,vels_motor[i], vel_engine[i], vels_motor[i]-vels_engine[i], currents[i]])
                    except:
                        pass
            print("csv written")
    else:
        file_name = "not holding pos03-11-23 21-11-23motor vs engine pos data.json"#easygui.fileopenbox()
        dictionary = json.load(open(file_name))
        print(dictionary["data"]["times"])
        times = dictionary["data"]["times"]
        motor_velocity = dictionary["data"]["motor pos"]
        engine_velocity = dictionary["data"]["engine pos"]
        plt.plot(times, motor_velocity)
        plt.plot(times, engine_velocity)
        print(dictionary["data"]["pos setpoint"])
        plt.legend(["Motor", "Engine"])
        plt.xlabel("Time")
        plt.ylabel("Pos")
        plt.show()
# [pos,vel] = calculate_pos_vel(engine_sign=1,motor_sign=1)
# setpoint_vel = calculate_velocity_setpoint()
# error = setpoint_vel-vel
# odrv0.axis0.controller.input_vel = 
# odrv0.axis0.requested_state = AXIS_STATE_IDLE

# def calculate_velocity_setpoint():
#     return 1

# def differential_equation_with_ratio(motor,engine):
#     return ratio_motor*motor - ratio_engine*engine

# def calculate_pos_vel(engine_sign, motor_sign):
#     pos_M = odrv0.axis0.encoder.pos_estimate
#     pos_E = odrv0.axis1.encoder.pos_estimate
#     vel_M = odrv0.axis0.encoder.vel_estimate
#     vel_E = odrv0.axis1.encoder.vel_estimate
#     _pos = differential_equation_with_ratio(pos_M, pos_E)
#     _vel = differential_equation_with_ratio(vel_M, vel_E)
#     return [_pos, _vel]

def initilize_odrive():
    print("finding an odrive...")
    odrv0 = odrive.find_any()
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    print("motor enabled")

if __name__ == "__main__":
    main()