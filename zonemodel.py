"""
@author: rory
"""
import matplotlib.pyplot as plt
import math

#some housekeeping for the plots
plt.close('all')
plt.rcParams["font.family"] = "helvetica"
plt.rcParams["font.size"] = 12

#define some compartment geometry
comp_Height=10
comp_Width=10
comp_Length=10
comp_Area = comp_Width*comp_Length

# define the fire growth rates
# alpha=0.003 #slow
alpha=0.012 #medium
# alpha=0.047 #fast
# alpha=0.188 #ultra fast

#in theory one could add this
Extraction_rate=0

#constants for the smoke
cp_air =1.005
R = 8.314
MW_air = 28.8
P_amb = 101325

#initial temperature
T_i = 290		

#timestep and max number of iterations
delta_t = 2
n_iterations=200

#set up the variables
time = [0]
Q_fire = [0]
z = [comp_Height]
m_u = [0]
T_u = [T_i]
rho_u = [P_amb*MW_air/(R*T_i*1000)]
V_u = [0]
m_e = [0]
T_s = [T_i]
delta_z = [0]

#start the loop
for count in range(1,n_iterations):
    
    if z[count-1] < 0: #to stop the code before it blows up
            break
    
    if count==1 or count==2: #this is needed to make sure that z is calcuated correctly
        z.append(comp_Height)
    else:
        z.append(comp_Height-delta_z[count-1])
        
    #now calculate the variables at each timestep    
    time.append(delta_t*count) #make a time vector    
    Q_fire.append(alpha*time[count]**2)
    # Q_fire.append(200)
    m_e.append(0.076*Q_fire[count]**(1/3)*z[count]**(5/3))
    T_s.append(T_i + Q_fire[count]/(m_e[count]*cp_air))
    m_u.append(m_u[count-1] + m_e[count]*delta_t)
    T_u.append((m_u[count-1]*T_u[count-1] + m_e[count]*T_s[count]*delta_t)/m_u[count])
    rho_u.append(P_amb*MW_air/(R*T_u[count]*1000))
    V_u.append(m_u[count]/rho_u[count])
    delta_z.append((V_u[count]/comp_Area))
    
#plot the variables of interest    
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
# ax1.plot(time, Q_fire, '--', color='gray', label='Fire size, kW')
ax1.plot(time, z, '-', color='gray', label='Smoke layer height')
ax1.plot(time, m_e, '--', color='black', label='Mass in the plume')
ax2.plot(time, T_u, '-', color='red', label='Upper layer temperature')
# ax1.plot(time, T_s)
# ax1.plot(time, m_u)
# ax1.plot(time, rho_u)
# ax1.plot(time, V_u)
# ax1.plot(time, delta_z)
ax1.set_xlabel('Time, s')
ax1.set_ylabel('Smoke layer height, m \n Mass in plume, kg/s')
ax2.set_ylabel('Temperature, °C')
#make the legend all in one box
fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
plt.savefig('/Users/rory/Library/CloudStorage/OneDrive-UniversityofEdinburgh/_Teaching/Fire Science and Engineering 2/2022/zone_model_output.png',  dpi=300)
