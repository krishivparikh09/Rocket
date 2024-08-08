##import files
import time
import data
import rocketTime
import simulation
import golden_zone

##import libraries
import numpy as np
import matplotlib.pyplot as plt

### initialize the arrays used to store trajectories if motor 2 was never to be turned on
accel_trajectory_array = np.array([])
vel_trajectory_array = np.array([])
position_trajectory_array = np.array([])
time_trajectory_array = np.array([])

### store the golden_array
accel_golden_array = np.array([])
vel_golden_array = np.array([])
position_golden_array = np.array([])
time_golden_array = np.array([])

######### variables ###########################
## stores the current mass of the rocket
current_rocket_mass = .537

### start timer ##### dont change
rocketTime.start_timer()

########################################################################################################################
########################### building and show trajectory array #########################################################
## building trajectory array
time_trajectory_array, position_trajectory_array, vel_trajectory_array, accel_trajectory_array, current_rocket_mass = simulation.determine_initial_rocket_trajectory(
    current_rocket_mass, 6, 0.001, time_trajectory_array, position_trajectory_array, vel_trajectory_array,
    accel_trajectory_array)

##show initial rocket trajectory graph
simulation.show_rocket_trajectory_graph(time_trajectory_array, position_trajectory_array, vel_trajectory_array,
                                        accel_trajectory_array)

########################################################################################################################
############################ deciding when motor turns on ##############################################################

## checks for golden_zone and puts golden trajectory in an array
time_golden_array, position_golden_array, vel_golden_array, accel_golden_array = golden_zone.build_golden_array(
    current_rocket_mass, 1, -.75, time_trajectory_array, position_trajectory_array, vel_trajectory_array,
    accel_trajectory_array, .01, 3, .3)

## show the golden array
simulation.show_rocket_trajectory_graph(time_golden_array, position_golden_array, vel_golden_array, accel_golden_array)

print(f"\nProgram runtime:{rocketTime.get_time(): .2f}s")
