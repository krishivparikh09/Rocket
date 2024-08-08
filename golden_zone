##libraries
import simulation
import data
import rocket
import math
import numpy as np
import time


def detect_apogee(time_array, vel_array):
    print("Checking for apogee....")
    for i in range(len(time_array)):
        time_var = time_array[i]
        cur_vel = vel_array[i]
        if cur_vel < -.0001:
            print(f"Apogee detected at {time_var :.3f} seconds\n")
            return i


def build_golden_array(mass, constraint_position, constraint_velocity, time_array, pos_array, vel_array, accel_array,
                       dt, runtime, elastic_constant):
    ##golden_array_after_motor_goes_off
    golden_time_amgo = np.array([])
    golden_pos_amgo = np.array([])
    golden_vel_amgo = np.array([])
    golden_accel_amgo = np.array([])

    ##get apogee element
    apogee_array_element = detect_apogee(time_array, vel_array)

    ## find the perfect instance to launch the rocket
    golden_time, golden_pos, golden_vel, golden_accel, golden_instance = find_golden_zone(mass, constraint_position,
                                                                                          constraint_velocity,
                                                                                          time_array, pos_array,
                                                                                          vel_array, accel_array,
                                                                                          apogee_array_element, dt)
    ## build the array for the graph after motor 2 goes off
    ## set up vars for iterating and building the array
    vel_i = golden_vel
    pos_i = golden_pos
    cur_time = 0
    cur_mass = mass

    ##make the array run for runtime
    while cur_time < runtime:
        ## the physics for the rocket
        cur_mass -= data.mass_loss_curve(cur_time) * dt
        accel_i = simulation.calc_accel_test(cur_mass, cur_time, 0)
        vel_cur = simulation.calc_vel(accel_i, vel_i, dt)
        pos_cur = pos_i + simulation.calc_position(accel_i, vel_i, dt)
        ## make directions change if it hits the ground
        if pos_cur <= 0:
            pos_cur = 0
            vel_cur = -vel_cur * elastic_constant

        ##add the time, pos... values to an array
        golden_time_amgo = np.append(golden_time_amgo, cur_time + golden_time)
        golden_pos_amgo = np.append(golden_pos_amgo, pos_cur)
        golden_vel_amgo = np.append(golden_vel_amgo, vel_cur)
        golden_accel_amgo = np.append(golden_accel_amgo, accel_i)

        ##advancing in time
        cur_time += dt
        vel_i = vel_cur
        pos_i = pos_cur

    new_golden_time_array = np.concatenate((time_array[:golden_instance + 1], golden_time_amgo))
    new_golden_pos_array = np.concatenate((pos_array[:golden_instance + 1], golden_pos_amgo))
    new_golden_vel_array = np.concatenate((vel_array[:golden_instance + 1], golden_vel_amgo))
    new_golden_accel_array = np.concatenate((accel_array[:golden_instance + 1], golden_accel_amgo))

    #return golden_time_amgo, golden_pos_amgo, golden_vel_amgo, golden_accel_amgo
    return new_golden_time_array, new_golden_pos_array, new_golden_vel_array, new_golden_accel_array


def find_golden_zone(mass, constraint_position, constraint_velocity, time_array, pos_array, vel_array, accel_array,
                     apogee_array_element, dt):
    print("Finding golden zone...")
    # Copy the arrays to initialize the golden zone arrays
    golden_time_array = np.copy(time_array)
    golden_pos_array = np.copy(pos_array)
    golden_vel_array = np.copy(vel_array)
    golden_accel_array = np.copy(accel_array)

    time_v = 0
    pos = 0
    vel = 0
    accel = 0

    index = apogee_array_element
    close_loop = 0

    while close_loop == 0 and index <= len(golden_time_array) - 1:
        track_time = time.time()
        time_v = golden_time_array[index]
        pos = golden_pos_array[index]
        vel = golden_vel_array[index]
        accel = golden_accel_array[index]
        print(
            f"CHECKING INSTANCE: Time:{time_v: .3f}, Position:{pos: .2f}, Velocity:{vel: .2f}, Acceleration:{accel: .2f}")
        close_loop += test_instance(mass, pos, vel, accel, dt, constraint_position, constraint_velocity)
        print(f"Runtime:{time.time() - track_time: .4f}s\n\n")
        index += 1

    if close_loop == 1:
        print(
            f"Golden Zone Found\nGolden Instance: Time:{time_v: .3f}, Position:{pos: .2f}, Velocity:{vel: .2f}, Acceleration:{accel: .2f}")
        return time_v, pos, vel, accel, index
    elif close_loop == 0:
        print("Golden Zone Not Found")
        return 0, 0, 0, 0, index

    ## run a loop to check if that instance works with the desired constraints
    ## if it does break from loop and send that array over


## test the given instance of the given pos, vel, accel
## returns if that instance was successful under the constraints
def test_instance(mass, pos, vel, accel, dt, constraint_pos, constraint_vel):
    vel_i = vel
    pos_i = pos
    cur_time = 0
    cur_mass = mass

    while constraint_pos < pos_i:
        cur_mass -= data.mass_loss_curve(cur_time) * dt
        accel_i = simulation.calc_accel_test(cur_mass, cur_time, 0)
        vel_cur = simulation.calc_vel(accel_i, vel_i, dt)
        pos_cur = pos_i + simulation.calc_position(accel_i, vel_i, dt)
        cur_time += dt
        vel_i = vel_cur
        pos_i = pos_cur

    print(f"For above instance, at Pos: {pos_i: .3f}, Vel: {vel_i: .2f}, Time (after apogee):{cur_time: .2f}s")

    if abs(constraint_vel) > abs(vel_i):
        return 1
    else:
        return 0
