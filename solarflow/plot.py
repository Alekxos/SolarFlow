import numpy as np
from matplotlib import pyplot as plt

def get_color_cycler():
    """
    Return a color cycler.
    """
    color_list = ['#007BA7', '#9B111e', '#009E60', '#FA8072']
    return plt.cycler(color=color_list)

def set_plotting_defaults(single_color=False):
    plt.rcParams['lines.linewidth'] = 2.2
    plt.rcParams["xtick.major.size"] = 5
    plt.rcParams["xtick.major.width"] = 1.2
    plt.rcParams["ytick.major.size"] = 5
    plt.rcParams["ytick.major.width"] = 1.2
    plt.rcParams["axes.titlesize"] = 20
    plt.rcParams["font.size"] = 10
    plt.rcParams['xtick.labelsize'] = 15
    plt.rcParams['ytick.labelsize'] = 15
    color_list = ['#007BA7', '#9B111e', '#009E60', '#FA8072']
    if single_color:
        color_list = ['#007BA7', ]
    plt.rcParams['axes.prop_cycle'] = get_color_cycler()

def plot_impedance_by_frequency(frequencies, impedance_data_real, impedance_data_im, axis=None):
    """
    Plot impedance data by frequency.
    """
    axis.axis('equal')
    axis.set_prop_cycle(get_color_cycler())
    for frequency in frequencies:
        axis.plot(impedance_data_real[frequency], impedance_data_im[frequency], '.', label=f"{int(frequency // 1e3)} kHz")
    axis.title.set_text("Impedance Response by Frequency")
    axis.set_xlabel("Z' (Ohm)", fontsize=18)
    axis.set_ylabel("Z'' (Ohm)", fontsize=18)
    axis.legend(loc='lower right')

def plot_circle_fit(circle_fits, axis, plot_centers = False):
    """
    Plot circle fit.
    """
    axis.set_prop_cycle(get_color_cycler())
    for frequency, (xc, yc, r) in circle_fits.items():
        circle = plt.Circle((xc, yc), r, color='#36454F', fill=False)
        axis.add_artist(circle)
        if plot_centers:
            axis.plot(xc, yc, marker = '*')

        # Recompute limits and autoscale
        axis.relim()
        axis.autoscale_view()

def plot_theta_vs_voltage(frequencies, theta_data, voltage_data, axis):
    """
    Plot theta vs voltage.
    """
    axis.set_prop_cycle(get_color_cycler())
    for frequency in frequencies:
        axis.plot(voltage_data[frequency], theta_data[frequency], '.', label=f"{int(frequency // 1e3)} kHz")
    axis.title.set_text(r"Angle $\Theta$ Relative to Center vs. Voltage")
    axis.set_xlabel("Voltage (V)", fontsize=18)
    axis.set_ylabel(r"$\Theta$ (rad)", fontsize=18)
    axis.legend(loc='lower right')

def plot_omega_vs_radius(frequencies, circle_fits, axis):
    r = [circle_fits[freq][2] for freq in frequencies]
    axis.plot(np.array(frequencies) // 1e3, r, 'o', color='#9B111e')
    axis.title.set_text("Circle Fit Radius vs. Frequency")
    axis.set_xlabel("Frequency (kHz)", fontsize=18)
    axis.set_ylabel("Radius (Ohm)", fontsize=18)