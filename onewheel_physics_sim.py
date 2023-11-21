import math

#assume rigid human
human_mass = 68.0
weight_dist = 0.4
resultant_force = 9.81 * abs(human_mass*weight_dist - human_mass*(1-weight_dist))
stance_distance = 0.6096
torque_wheel = stance_distance * 0.5 * resultant_force
gear_ratio = 0.11
rpm_wheel = 278
rpm_engine = rpm_wheel/gear_ratio
torque_engine = torque_wheel * gear_ratio
rads_engine = rpm_engine * 0.104719755

power = torque_engine * rads_engine
print("Engine power ", power)
print("Engine torque ", torque_engine)

board_angle = 0.5 #degree
human_com_height = 0.56 * 6 * 12 * 0.0254
distance = human_com_height * math.sin(board_angle * math.pi/180)
torque_wheel = distance * human_mass * 9.81
torque_engine = torque_wheel * gear_ratio
print(torque_engine)


# engine_rpm = 6000
# engine_rads = engine_rpm * 0.104719755
# engine_power = 750
# engine_torque = engine_power/engine_rads
# print(engine_torque)

# dt = 5 #s
# ah_t0 = 0.0851
# ah_t5 = 0.0947
# V = 53
# rots_t5 = 311.0
# rots_t0 = 297.0

dt = 2 #s
ah_t0 = 0.1571
ah_t5 = 0.1667
V = 53
rots_t5 = 586
rots_t0 = 574

ah_delta = ah_t5-ah_t0
a_delta = ah_delta/(dt/(60^2))
power = a_delta * V
print("Empirical electrical power ", power)


revs_delta = (rots_t5-rots_t0)/dt
rads_delta = 2*math.pi*revs_delta
r_wheel = 5.5*0.0254
v = r_wheel*rads_delta
ke = 0.5*human_mass*(v**2)
print("Empirical mechanical power", ke/dt)