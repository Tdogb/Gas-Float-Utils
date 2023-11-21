import time, json, datetime, csv, sched
import matplotlib.pyplot as plt

file_name = "04-11-23 10-09-55motor vs engine vel data.json"#easygui.fileopenbox()
dictionary = json.load(open(file_name))
times = dictionary["data"]["times"]
motor_velocity = dictionary["data"]["motor vel"]
engine_velocity = dictionary["data"]["engine vel"]
# plt.plot(times, motor_velocity)
plt.plot(times, engine_velocity)
# plt.plot(times, dictionary["data"]["motor current"])
# plt.plot(times, [motor_velocity[i]+engine_velocity[i] for i in range(len(motor_velocity))])
plt.legend(["Motor", "Engine", "Difference"])
plt.xlabel("Time")
plt.ylabel("Pos")
plt.show()