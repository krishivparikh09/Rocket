import numpy as np
import matplotlib.pyplot as plt
import time


#### thrust curve data ###############################
def thrust_curve(t):
    return np.piecewise(t, [t < .282, (t >= .282) & (t < .442),
                            (t >= .442) & (t < 1.59),
                            (t >= 1.59) & (t < 1.65),
                            (t < 0) | (t > 1.65)],
                        [lambda t: (-0.01503072514 * 0.4952901992 + 130.9674842 * (t ** 1.521212725)) / (
                                0.4952901992 + (t ** 1.521212725)),
                         lambda t: (-4335.31377 * (t ** 3)) + (5893.833958 * (t ** 2)) + (
                                 -2658.372049 * (t ** 1)) + 408.8257738,
                         lambda t: -2.397345294 * t + -4.078077251 / t + 1.374421189 / (t ** 2) + 14.05347312,
                         lambda t: (-14790.86129 + 8964.157926 * t) / (1 + 321.0381981 * t + -227.9574159 * (t ** 2)),
                         lambda t: 0])


# Numerical integration of thrust curve
def integral_thrust_curve():
    t_values = np.linspace(0, 1.65, 1000)
    thrust_values = thrust_curve(t_values)
    integral_value = np.trapz(thrust_values, t_values)
    return integral_value




def mass_loss_curve(t):
    #k = delta mass / definite integral of thrust curve
    k = .022 / 16.7528
    return thrust_curve(t) * k


def mass_loss_test(initial_mass, dt):
    current_mass = initial_mass
    runtime = 2
    cur_time = 0
    while cur_time < runtime:
        current_mass -= mass_loss_curve(cur_time) * dt
        cur_time += dt
        # debugging purposes
        print(f"Time: {cur_time :.5f}, Mass {current_mass :.5f} ")
    #return current_mass


def print_thrust_curve():
    # Generate a range of t values
    t_values = np.linspace(0, 2, 400)

    # Calculate the corresponding thrust values
    thrust_values = thrust_curve(t_values)

    # Plot the piecewise function
    plt.plot(t_values, thrust_values, label='Thrust Curve')
    plt.xlabel('Time (s)')
    plt.ylabel('Thrust (N)')
    plt.title('Thrust vs. Time')
    plt.legend()
    plt.grid(True)
    plt.show()

