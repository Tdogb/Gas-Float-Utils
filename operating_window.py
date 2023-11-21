import numpy as np
import matplotlib.pyplot as plt

# plt.contour()
length = 25
m_max_torque = 2
e_max_torque = 1.2

# e_torques = [1, 2, 3, 4, 5, 4.5, 4, 3.5] #example of torques that could be at X throttle
e_rpms = np.linspace(3500,7500,length)
e_torques = e_max_torque*([-x**2/3750000 + 4*x/1875 - 11/5 for x in e_rpms]/4.5)
m_rpms = np.linspace(-8000,8000,length)
# m_torques = np.ones_like(m_rpms) * m_max_torque #need to add negatives

wheel_rpms = np.linspace(-10000,19000,length)
wheel_torques = np.linspace(-2.5,5,length)

max_acheivable_wheel_rpm = e_rpms[-1]/2 + m_rpms[-1]/2
min_acheivable_wheel_rpm = e_rpms[0]/2 + m_rpms[0]/2

# max_acheivable_wheel_torque = e_torques[4] + 
z_total_generating = np.zeros((length,length))
z_total_motoring = np.zeros((length,length))

m_rpm_min = np.min(m_rpms)
m_rpm_max = np.max(m_rpms)
operating_window_max_x = []
operating_window_max_y = []
operating_window_max_z = []

for c,e_rpm in enumerate(e_rpms):
    for d,e_torque in enumerate(e_torques):
        z = np.zeros((length,length))
        for i,w_rpm in enumerate(wheel_rpms):
            for b,w_torque in enumerate(wheel_torques):
                rpm_good = False
                torque_good = False
                if (m_rpm_min/2) <= (w_rpm/2 - e_rpm/2) <= (m_rpm_max/2):
                    rpm_good = True
                if (-m_max_torque) <= (w_torque - e_torque) <= (m_max_torque):
                    torque_good = True
                if rpm_good and torque_good:
                    if np.sign(w_torque - e_torque) != np.sign(w_rpm/2 - e_rpm/2):
                        z[b][i] += 1
                        z_total_generating[d][c] += 1
                    else:
                        z[b][i] += 1
                        z_total_motoring[d][c] += 1

# ax = plt.axes(projection='3d')
        # print("e_rpm ", e_rpm, " e_torque ", e_torque)
        # plt.scatter(operating_window_max_x,operating_window_max_y)
        # plt.xlim(np.min(wheel_rpms),np.max(wheel_rpms))
        # plt.ylim(np.min(wheel_torques),np.max(wheel_torques))
# x,y = np.meshgrid(wheel_rpms,wheel_torques)
# ax.contour3D(x, y, z_total_motoring, 100, cmap='Greens')
# ax.contour3D(x, y, z_total_generating, 100, cmap='Oranges')
vmin = np.amin([np.amin(z_total_motoring),np.amin(z_total_generating)])
vmax = np.amax([np.amax(z_total_motoring),np.amax(z_total_generating)])

plt.figure(1)
x,y = np.meshgrid(wheel_rpms,wheel_torques)
plt.contourf(x,y,z)
plt.title("Wheel Operating Window") #Brighter = more states acheivable by motor with this wheel command regardless of engine state
plt.xlabel("Wheel RPMs")
plt.ylabel("Wheel Torques")

plt.figure(2)
x1,y1 = np.meshgrid(e_rpms,e_torques)
print(x1)
print(z_total_generating)
# plt.contourf(x1,y1,z_total_generating)
plt.imshow(z_total_generating,vmin=vmin,vmax=vmax)
plt.title("Engine Power Generating Operating Window") #Brighter = more states acheivable by motor with this wheel command regardless of engine state
plt.xlabel("Engine RPMs")
plt.ylabel("Engine Torques")

plt.figure(3)
# x2,y2 = np.meshgrid(e_rpms,e_torques)
# plt.contourf(x1,y1,z_total_motoring,vmin=vmin,vmax=vmax)
plt.imshow(z_total_motoring,vmin=vmin,vmax=vmax)
plt.title("Engine Power Motoring Operating Window") #Brighter = more states acheivable by motor with this wheel command regardless of engine state
plt.xlabel("Engine RPMs")
plt.ylabel("Engine Torques")

plt.figure(4)
# x3,y3 = np.meshgrid(e_rpms,e_torques)

# plt.contourf(x1,y1,np.add(z_total_generating, z_total_motoring))
plt.imshow(np.add(z_total_generating, z_total_motoring)/2,vmin=vmin,vmax=vmax)
plt.title("Engine Overall Operating Window") #Brighter = more states acheivable by motor with this wheel command regardless of engine state
plt.xlabel("Engine RPMs")
plt.ylabel("Engine Torques")

plt.show()