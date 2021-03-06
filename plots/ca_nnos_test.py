import numpy as np
import matplotlib.pyplot as plt
from custom_modules.plot_setting import *

mpl.rcParams['lines.linewidth'] = 1.

####
#This script simulates NO synthesis dynamics under poisson spiking and compares it
#to the approximate solution derived in the thesis.
####

## Simulation scripts required to run before this script:
# None

# Calcium and nNOS parameters
tau_ca = 0.01
tau_nNOS = 0.1
Ca_sp = 1.

# where to save data
savefolder = plots_base_folder
plot_filename = "nNOS_approx"

# Range-Kutta integration step
def step(phi,func,dt):
	phi1=func(phi)
	phi2=func(phi+phi1*dt/2)
	phi3=func(phi+phi2*dt/2)
	phi4=func(phi+phi3*dt)
	return phi+(phi1+2*phi2+2*phi3+phi4)*dt/6

# function to be integrated
def F(phi):
	
	r = np.ndarray(3)
	
	r[0] = -phi[0]/tau_ca # calcium dynamics
	r[1] = (phi[0]**3/(phi[0]**3+1.) - phi[1])/tau_nNOS # nNOS dynamics
	r[2] = -phi[2]/tau_nNOS # APPROXIMATE nNOS dynamics
	
	return r

# Poisson frequency
f = 3.

# simulation run time and time step
T = 5.
dt = 0.001

# number of sim. steps
n_t = int(T/dt)

# recording array
rec = np.ndarray((n_t,3))

# initialize dynamic variable at 0
phi = np.zeros(3)

# instantaneous jumps for Calcium dynamics and approximate nNOS dynamics
add_arr = np.array([Ca_sp,Ca_sp**3*tau_ca*np.log(2.)/(3.*tau_nNOS)])

# Flag to find first spike event (needed for plotting)
first_spike_app = False

# main sim. loop
for t in xrange(n_t):
	
	phi = step(phi,F,dt) # integration step
	
	if np.random.rand() <= f*dt: # Poisson events
		phi[[0,2]] += add_arr # add jump values
		
		if not(first_spike_app): # find the first spike event
			ind_first_spike = t
		
			first_spike_app = True
	
	rec[t,:] = phi # record simulation


t_arr = np.linspace(0,T,n_t) # x-axis for plotting

fig, ax = plt.subplots(2,1,figsize=(default_fig_width,default_fig_width*0.6))

t_window = [0.05,0.3] # [t of first spike event - t_window[0], t of first spike event + t_window[1] ] defines time window to be plotted in closeup

# plot time course of Calcium and nNOS/approx. nNOS
ax[0].plot(t_arr[ind_first_spike-int(t_window[0]/dt):ind_first_spike+int(t_window[1]/dt)],rec[ind_first_spike-int(t_window[0]/dt):ind_first_spike+int(t_window[1]/dt),[1,2]])
ax[1].plot(t_arr,rec[:,[1,2]])

# axes limits and labels
ax[0].set_xlim([dt*ind_first_spike - t_window[0],dt*ind_first_spike + t_window[1]])
ax[1].set_xlabel("t [s]")
ax[0].set_ylabel(r'nNOS [$\mathrm{s^{-1}}$]')
ax[1].set_ylabel(r'nNOS [$\mathrm{s^{-1}}$]')

y_range_0 = [0.,rec[ind_first_spike-int(t_window[0]/dt):ind_first_spike+int(t_window[1]/dt),[1,2]].max()*1.2]
y_range_1 = [0.,rec[:,[1,2]].max()*1.2]

# fix axes ticks
ax[0].set_yticks(np.arange(y_range_0[0],y_range_0[1], 0.01))
ax[1].set_yticks(np.arange(y_range_1[0],y_range_1[1], 0.02))

# save figure
for f_f in file_format:
	plt.savefig(savefolder+plot_filename+f_f)


plt.show()
#pdb.set_trace()


	
