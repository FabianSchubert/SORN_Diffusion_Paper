import numpy as np
import matplotlib.pyplot as plt
from brian import *
from custom_modules.plot_setting import *

from custom_modules.lif_act_funct import *

# This script tests the accuracy of an analytic expression for the mean firing rate of a noisy/non-noisy LIF-Neuron

## Simulation scripts required to run before this script:
# None

# where to save figure
savefolder = plots_base_folder
plot_filename = "F-I_noise_dep"

# space of neural input to test
I = np.linspace(-200.,500.,4000)

# intrinsic neuron properties
V_t = -58. # threshold, mV
V_r = -70. # reset voltage, mV
E_l = -60. # resting potential, mV
tau_m = 0.02 # membrane time constant, seconds
sigm = np.sqrt(5.) # intrinsic membrane noise standard deviation, mV

fig = plt.figure(figsize=(default_fig_width*0.7,default_fig_width*0.7*0.7))

# plot I-f curve with and without membrane noise
plt.plot(I,phi_noise(I,V_t,V_r,E_l,tau_m,sigm,4000))
plt.plot(I,phi_noise(I,V_t,V_r,E_l,tau_m,0.0001,4000))
plt.xlabel("Synaptic Input [mV/s]")
plt.ylabel("Mean Firing Rate [Hz]")

# parameters for the full simulation of a LIF-neuron (using BRIAN)

# neuron parameters (see above)
E_l=-60 * mV
V_r=-70 * mV
V_t = -58 * mV
tau = 20 * ms
sigm1 = sqrt(5.) * mV
sigm2 = 0. * mV

# run time from which to collect spiketimes
t_run = 50. * second

# equations for noisy/non-noisy neuron

eqs1='''
dV / dt = - (V - E_l) / tau + J + xi * sigm1 / (tau **.5): volt
J: volt / second
'''

eqs2='''
dV / dt = - (V - E_l) / tau + J + xi * sigm2 / (tau **.5): volt
J: volt / second
'''
# number of neurons (each one representing a "test neuron" for some amount of neural input)
n_grid = 100

#initialize neuron groups for noise/no noise case
P1=NeuronGroup(n_grid,model=eqs1,threshold = V_t, reset=V_r)
P1.V=V_r

P2=NeuronGroup(n_grid,model=eqs2,threshold = V_t, reset=V_r)
P2.V=V_r

# Spike recorders
M1=SpikeMonitor(P1)
M2=SpikeMonitor(P2)

# input array
I_arr=np.linspace(-200.,500.,n_grid)

# set individual input of "test neurons"
for k in xrange(n_grid):
	
	P1[k].J = I_arr[k] * mV / second
	P2[k].J = I_arr[k] * mV / second
	

# run network
run(t_run,report='text')

f_noise = np.zeros(n_grid)
f_no_noise = np.zeros(n_grid)


# calculate mean rates from spikes
for k in xrange(n_grid):
	f_noise[k] = float(second * len(M1[k])/t_run)
	f_no_noise[k] = float(second * len(M2[k])/t_run)

# plot mean rates acquired from simulation
plt.plot(I_arr,f_noise,'.',c='k',fillstyle='none')
plt.plot(I_arr,f_no_noise,'s',c='k',fillstyle='none')

plt.ylim([-5.,60.])

#save figure
for f_f in file_format:
	plt.savefig(savefolder + plot_filename + f_f)

plt.show()

