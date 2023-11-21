import odrive
from odrive.enums import *
import time, csv
import matplotlib.pyplot as plt

print("finding an odrive...")
odrv0 = odrive.find_any()
times = []
data = []
data1 = []
start_ns = time.time_ns()
start_s = time.time()
print("running")
while time.time()-start_s < 10:
    times.append(time.time_ns()-start_ns)
    data.append(odrv0.axis0.encoder.vel_estimate) #PUT VARIABLE TO LOG HERE
    data1.append(odrv0.axis1.encoder.vel_estimate) #PUT VARIABLE TO LOG HERE
    time.sleep(1/1000)
plt.plot(times,data)
plt.plot(times,data1)
plt.legend(["Axis 0", "Axis 1"])
plt.show()
# with open('vel_time_series.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     for i in range(len(times)):
#         writer.writerow([times[i],data[i]])