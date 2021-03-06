#!/usr/bin/env python
# main.py
#
# Run the ice model.
#
# Graham Stonebridge
# Department of Systems Design Engineering
# University of Waterloo
# 2015

###############################################################################
# Import Libraries
###############################################################################

import numpy as np
import profile
import sys

# Import custom classes
from world import Model, Ice, Ocean, Atmosphere
from utils import *

###############################################################################
# Main code
###############################################################################
def main():
    # Instantiate sea ice, ocean and atmosphere classes
    ice = Ice()
    ocean = Ocean()
    atm = Atmosphere()
    figure_init(ice.plot_bool)

    # You can define the initial conditions here if you have a saved state
    ice.u = np.load('u.npy')
    ice.h = np.load('h.npy')*0.3
    ice.a = np.load('a.npy')*0.5

    # Want to save hourly state
    u_hist = np.copy(ice.u)
    ua_hist = np.copy(atm.u)
    uw_hist = np.copy(ocean.u)
    a_hist = np.copy(ice.a)
    h_hist = np.copy(ice.h)

    print(ice.dx)
    # Change some parameters
    ice.growth_scaling = 0.0
    ocean.length_scale = 25000
    ocean.time_scaling = 0.05
    atm.length_scale = 10000
    atm.time_scaling = 0.1
    ice.tf = 24*3600*30
    ocean.restart()
    atm.restart()

    # March models forward in time
    t = ice.t0
    print("Beginning at time "+str(t)+" hours")
    dt = np.amin([ice.dt, ocean.dt, atm.dt])
    tp = np.copy(ice.dt)*1 # when to update plots
    while True:
        t += dt

        # Check if run is finished
        if t > ice.tf:
            break

        # March forward the relevant models
        if t % ocean.dt == 0:
            ocean.time_step()
        if t % atm.dt == 0:
            atm.time_step()
        if t % ice.dt == 0:
            print('Ice time step at t = '+str(t/3600)+' hours')
            ice.time_step(np.copy(ocean.u),np.copy(atm.u))
        if t % tp ==0:
            figure_update(ice.plot_bool,ocean.u,atm.u,ice.u,ice.a,ice.h,t)
        if t % (24*3600) == 0:
             ice.growth_scaling = np.random.uniform(-0.00,0.00)
#             ice.growth_scaling = np.random.uniform(-0.2,0.2)
             print("ice growth scaling set to "+str(ice.growth_scaling))
#        if t % (15*24*3600) == 0:
#            print('restart atmosphere', t) # Periodically restart the SW models to prevent oscillations
#            atm.restart()
#        if t % (15*24*3600) == 0:
#            print('restart ocean', t) # Periodically restart the SW models to prevent oscillations
#            ocean.restart()

    # Save state to file.
    np.save('results/u.npy', ice.u)
    np.save('results/a.npy', ice.a)
    np.save('results/h.npy', ice.h)

###############################################################################
# Run the program
###############################################################################
if __name__ == "__main__":
    main()
