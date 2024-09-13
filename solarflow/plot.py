import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from solarflow.fit import lorentzian
from solarflow.fit import equation_to_string

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
    plt.gca().invert_yaxis()

def ohms_to_kOhms(x, pos):
    return f'{x / 1000:.0f}'

def plot_impedance_by_frequency(frequencies, impedance_data_real, impedance_data_im, axis, add_to_legend=True):
    """
    Plot impedance data by frequency.
    """
    axis.axis('equal')
    axis.set_prop_cycle(get_color_cycler())
    for frequency in frequencies:
        label = f"{int(frequency // 1e3)} kHz" if add_to_legend else None
        axis.plot(impedance_data_real[frequency], impedance_data_im[frequency], '.', label=label)
    axis.title.set_text("Impedance Response by Frequency")
    formatter = FuncFormatter(ohms_to_kOhms)
    axis.xaxis.set_major_formatter(formatter)
    axis.yaxis.set_major_formatter(formatter)
    axis.set_xlabel("Z'", fontsize=18, loc='right')
    axis.set_ylabel("Z''", fontsize=18, loc='bottom', rotation=0)
    if add_to_legend:
        axis.legend(loc='lower right')

def plot_circle_fit(circle_fits, axis, plot_centers = False):
    """
    Plot circle fit.
    """
    axis.set_prop_cycle(get_color_cycler())
    axis.axis('equal')
    for frequency, (xc, yc, r) in circle_fits.items():
        circle = plt.Circle((xc, yc), r, color='#36454F', fill=False)
        axis.add_artist(circle)
        if plot_centers:
            axis.plot(xc, yc, marker = '*')

        # Recompute limits and autoscale
        axis.relim()
        axis.autoscale_view()

    # Find last limits and center plot
    max_limit = np.max(np.abs(np.append(np.array(axis.get_xlim()), np.array(axis.get_ylim()))))
    axis.set_xlim([-max_limit, max_limit])
    axis.set_ylim([max_limit, -max_limit])

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

def plot_omega_vs_radius(frequencies, circle_fits, axis, x_scale=1e3, y_scale=1):
    r = np.array([circle_fits[freq][2] for freq in frequencies])
    axis.plot(np.array(frequencies) / x_scale, r / y_scale, 'o', color='#9B111e')
    axis.title.set_text("Circle Fit Radius vs. Frequency")
    axis.set_xlabel("Frequency (kHz)", fontsize=18)
    axis.set_ylabel("Radius (Ohm)", fontsize=18)

def plot_fit(axis, x, params, func_name, func, color='r', num_points = 1000, show_legend=True, x_scale = 1, y_scale = 1):
    x = np.linspace(min(x), max(x), num_points)
    y_fit = func(x, *params)
    label = f'{func_name} Fit' + '\n' + equation_to_string(func, params)
    axis.plot(x / x_scale, y_fit / y_scale, 'r-', label=label, color=color)
    if show_legend:
        axis.legend()