import numpy as np
from matplotlib import pyplot as plt

from solarflow.inout import read_csv_file, to_filename
from solarflow.data import get_unique_frequencies, get_data_by_frequency, extract_data_by_header
from solarflow.plot import plot_impedance_by_frequency, plot_circle_fit, set_plotting_defaults, plot_theta_vs_voltage, plot_omega_vs_radius, plot_fit
from solarflow.analysis import fit_circles_by_frequency, extract_theta_by_frequency, halve_data
from solarflow.fit import lorentzian, arc_tan, modified_lorentzian, gaussian, fit_data

if __name__ == '__main__':
     # Read data from a csv file.
     headers, data = read_csv_file('/Users/minerva/Lab/SolarFlow/data/Sq_12_07_17_freq_sweep.csv',
                                   delimiter=', ',
                                   start_line=3)
     
     # Extract impedance data by frequency.
     unique_frequencies = get_unique_frequencies(data)
     values_by_frequency = get_data_by_frequency(data, headers)
     impedance_data_real = extract_data_by_header(values_by_frequency, 'Z\' (Ohm)')
     impedance_data_im = extract_data_by_header(values_by_frequency, 'Z\'\' (Ohm)')
     
     # Plot impedance data by frequency.
     set_plotting_defaults()
     fig, ax = plt.subplots()
     selected_frequencies = unique_frequencies[-8:-4]
     plot_impedance_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, axis=ax)

     # Fit a circle to the impedance data.
     circle_fits = fit_circles_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im)
     plot_circle_fit(circle_fits, axis=ax, plot_centers = True)
     plt.savefig('/Users/minerva/Lab/SolarFlow/output/07_17/circle_fits.png', dpi=500, bbox_inches='tight')

     # Extract voltage and $\Theta$ data by frequency.
     voltage_data = extract_data_by_header(values_by_frequency, 'Voltage (V)')
     theta_data = extract_theta_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, circle_fits)

     # Plot $\Theta$ data by selected frequency.
     fig, ax = plt.subplots()
     plot_theta_vs_voltage(selected_frequencies, theta_data, voltage_data, axis=ax)
     plt.savefig('/Users/minerva/Lab/SolarFlow/output/07_17/theta_vs_voltage.png', dpi=500, bbox_inches='tight')

     # Plot circle radius as a function of frequency.
     fig, ax = plt.subplots()
     plot_omega_vs_radius(selected_frequencies, circle_fits, axis=ax)
     plt.savefig('/Users/minerva/Lab/SolarFlow/output/07_17/radius_vs_omega.png', dpi=500, bbox_inches='tight')

     # Focus in on V vs. theta for a single frequency
     target_frequency = 8e5
     # theta_data = extract_theta_by_frequency([target_frequency, ], impedance_data_real, impedance_data_im, circle_fits)

     # Try fitting several functions
     fit_functions = {
          'Lorentzian': lorentzian,
          'Arctan': arc_tan,
          'Modified Lorentzian': modified_lorentzian,
          'Gaussian': gaussian
     }
     for fit_name, function in fit_functions.items():
          fig, ax = plt.subplots()
          plot_theta_vs_voltage([target_frequency, ], theta_data, voltage_data, axis=ax)
          colors = ['#FFA500', '#FF0000']
          for data_idx, (voltage_subset, theta_subset) in enumerate(halve_data([voltage_data[target_frequency], theta_data[target_frequency]])):
               fit_params = fit_data(voltage_subset, theta_subset, fit_name, function)
               plot_fit(ax, voltage_subset, fit_params, fit_name, function, color=colors[data_idx])

          print(f"Fitting: {fit_name}")
          plt.savefig(f'/Users/minerva/Lab/SolarFlow/output/07_17/{to_filename(fit_name)}_fit.png', dpi=500, bbox_inches='tight')

     # Limit fitting to arctan function
     fig, ax = plt.subplots()
     fit_name, function = 'Arctan', arc_tan
     plot_theta_vs_voltage([target_frequency, ], theta_data, voltage_data, axis=ax)
     # Cerulean hex code
     ruby_color = '#E0115F'

     colors = ['#E0115F', '#FFC0CB', '#FF69B4', '#FF1493', '#DB7093', '#C71585', '#FF00FF', '#8A2BE2', '#4B0082', '#9400D3']

     # Filter out data points with low voltage magnitude
     voltage_cutoff = 0.2
     for data_idx, (voltage_subset, theta_subset) in enumerate(halve_data([voltage_data[target_frequency], theta_data[target_frequency]])):
          voltage_subset, theta_subset = voltage_subset[np.abs(voltage_subset) > voltage_cutoff], theta_subset[np.abs(voltage_subset) > voltage_cutoff]
          fit_params = fit_data(voltage_subset, theta_subset, fit_name, function)
          voltage_subset_1, voltage_subset_2 = voltage_subset[voltage_subset < -voltage_cutoff], voltage_subset[voltage_subset > voltage_cutoff]
          plot_fit(ax, voltage_subset_1, fit_params, fit_name, function, color=colors[data_idx], show_legend=False)
          plot_fit(ax, voltage_subset_2, fit_params, fit_name, function, color=colors[data_idx], show_legend=False)

     plt.savefig(f'/Users/minerva/Lab/SolarFlow/output/07_17/arctan_fit_filtered.png', dpi=500, bbox_inches='tight')
     
     # Test on other frequencies
     selected_frequencies = selected_frequencies[:3]
     fig, ax = plt.subplots()
     plot_theta_vs_voltage(selected_frequencies, theta_data, voltage_data, axis=ax)
     for frequency_idx, frequency in enumerate(selected_frequencies):
          theta_data = extract_theta_by_frequency([frequency, ], impedance_data_real, impedance_data_im, circle_fits)
          for data_idx, (voltage_subset, theta_subset) in enumerate(halve_data([voltage_data[frequency], theta_data[frequency]])):
               voltage_subset, theta_subset = voltage_subset[np.abs(voltage_subset) > voltage_cutoff], theta_subset[np.abs(voltage_subset) > voltage_cutoff]
               fit_params = fit_data(voltage_subset, theta_subset, fit_name, function)
               voltage_subset_1, voltage_subset_2 = voltage_subset[voltage_subset < -voltage_cutoff], voltage_subset[voltage_subset > voltage_cutoff]

               color_idx = frequency_idx * len(selected_frequencies) + data_idx
               plot_fit(ax, voltage_subset_1, fit_params, fit_name, function, color=colors[color_idx % len(colors)], show_legend=False)
               plot_fit(ax, voltage_subset_2, fit_params, fit_name, function, color=colors[color_idx % len(colors)], show_legend=False)

     plt.savefig(f'/Users/minerva/Lab/SolarFlow/output/07_17/arctan_fit_multiple.png', dpi=500, bbox_inches='tight')