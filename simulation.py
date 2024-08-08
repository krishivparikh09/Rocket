import numpy as np
import matplotlib.pyplot as plt
import time
import data

#### functions #####
def calc_accel(mass, my_time, accel_i):
    thrust = data.thrust_curve(my_time)
    accel = ((thrust - (mass * 9.8)) / mass) + accel_i
    return accel

def calc_accel_test(mass, my_time, accel_i):
    thrust = data.thrust_curve(my_time) * 1
    accel = ((thrust - (mass * 9.8)) / mass) + accel_i
    return accel


def calc_vel(accel, initial_vel, dt):
    return initial_vel + (accel * dt)


def calc_position(accel, initial_vel, dt):
    return initial_vel * dt + 0.5 * accel * (dt ** 2)

def update_accel_vel_position(mass, position_initial, elastic_constant, dt, cur_time, vel_initial, time_array,
                              position_array, vel_array, accel_array):
    ### calc accel
    accel = calc_accel(mass, cur_time, 0)
    accel_array = np.append(accel_array, accel)

    ### calc velocity
    vel_cur = calc_vel(accel, vel_initial, dt)

    ### calc position
    position_cur = position_initial + calc_position(accel, vel_initial, dt)

    ### Check for collision with ground
    if position_cur <= 0:
        position_cur = 0
        vel_cur = -vel_cur * elastic_constant  # Reverse velocity and apply COR

    ### Append values after checking for collision
    vel_array = np.append(vel_array, vel_cur)
    position_array = np.append(position_array, position_cur)
    time_array = np.append(time_array, cur_time)

    ### Print statements for debugging
    # print(f"Time: {cur_time:.2f}, Position: {position_cur:.2f}, Velocity: {vel_cur:.2f}, Acceleration: {accel:.2f}")

    ### updated initial velocity and position to current
    return vel_cur, position_cur, time_array, position_array, vel_array, accel_array

### uses mass loss and thrust curve to determine the initial_rocket_trajectory
def determine_initial_rocket_trajectory(mass, runtime, dt, time_array, position_array, vel_array, accel_array):
    ## code for run time
    cur_time = 0
    cur_mass = mass
    ## starting constants
    position_initial = 0
    vel_i = 0
    elastic_constant = 0.35

    while cur_time < runtime:
        ### add dt to current time
        cur_mass -= data.mass_loss_curve(cur_time) * dt

        ## append the time, position, accel, and velocity array.
        # updates old cur position and velocity to initial to find the next area
        vel_i, position_initial, time_array, position_array, vel_array, accel_array = update_accel_vel_position(
            cur_mass, position_initial, elastic_constant, dt, cur_time, vel_i, time_array, position_array,
            vel_array, accel_array)

        cur_time += dt

    return time_array, position_array, vel_array, accel_array, cur_mass


def show_rocket_trajectory_graph(time_array, position_array, velocity_array, accel_array):
    plt.plot(time_array, position_array, marker='o', markersize=1, color='blue', label='Position')
    plt.plot(time_array, velocity_array, marker='o', markersize=1, color='green', label='Velocity')
    plt.plot(time_array, accel_array, marker='o', markersize=1, color='red', label='Acceleration')
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m), Velocity (m/s), Acceleration (m/s^2)')
    plt.title('Position, Acceleration, Velocity Vs. Time')
    plt.grid(True, which='major', linestyle='-')
    plt.minorticks_on()
    plt.grid(True, which='minor', linestyle=':', linewidth='0.5')
    plt.legend()
    plt.show()
