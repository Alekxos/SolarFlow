import numpy as np
from matplotlib import pyplot as plt

from solarflow.inout import read_csv_file
from solarflow.data import get_unique_frequencies, get_data_by_frequency, extract_data_by_header
from solarflow.plot import plot_impedance_by_frequency, plot_circle_fit, set_plotting_defaults, plot_theta_vs_voltage, plot_omega_vs_radius
from solarflow.analysis import fit_circles_by_frequency, extract_theta_by_frequency

if __name__ == '__main__':
     # Read data from a csv file.
     headers, data = read_csv_file('/Users/minerva/Lab/SolarFlow/data/Sq_14_08_18_freq_sweep_2.csv',
                                   delimiter=', ',
                                   start_line=3)
     
     # Extract impedance data by frequency.
     unique_frequencies = get_unique_frequencies(data)
     print(f"unique_frequencies: {unique_frequencies}")
     values_by_frequency = get_data_by_frequency(data, headers)
     impedance_data_real = extract_data_by_header(values_by_frequency, 'Z\' (Ohm)')
     impedance_data_im = extract_data_by_header(values_by_frequency, 'Z\'\' (Ohm)')
     
     # Plot impedance data by frequency.
     set_plotting_defaults()
     fig, ax = plt.subplots()
     selected_frequencies = unique_frequencies[5:]
     plot_impedance_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, axis=ax)

     # Fit a circle to the impedance data.
     circle_fits = fit_circles_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im)
     plot_circle_fit(circle_fits, axis=ax, plot_centers = True)
     plt.savefig('/Users/minerva/Lab/SolarFlow/output/08_18/circle_fits.png', dpi=500, bbox_inches='tight')

     # Extract voltage and $\Theta$ data by frequency.
     voltage_data = extract_data_by_header(values_by_frequency, 'Voltage (V)')
     theta_data = extract_theta_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, circle_fits)

     # Plot $\Theta$ data by selected frequency.
     fig, ax = plt.subplots()
     plot_theta_vs_voltage(selected_frequencies, theta_data, voltage_data, axis=ax)
     plt.savefig('/Users/minerva/Lab/SolarFlow/output/08_18/theta_vs_voltage.png', dpi=500, bbox_inches='tight')

     # Plot circle radius as a function of frequency.
     fig, ax = plt.subplots()
     plot_omega_vs_radius(selected_frequencies, circle_fits, axis=ax)
     plt.savefig('/Users/minerva/Lab/SolarFlow/output/08_18/radius_vs_omega.png', dpi=500, bbox_inches='tight')
     
     