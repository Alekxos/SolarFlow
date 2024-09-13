import numpy as np
from matplotlib import pyplot as plt

from solarflow.inout import read_csv_file
from solarflow.data import get_unique_frequencies, get_data_by_frequency, extract_data_by_header
from solarflow.plot import plot_impedance_by_frequency, plot_circle_fit, set_plotting_defaults, plot_theta_vs_voltage, plot_omega_vs_radius, plot_fit
from solarflow.fit import fit_data, inverse_quadratic
from solarflow.analysis import fit_circles_by_frequency, extract_theta_by_frequency

if __name__ == '__main__':
     headers, data = read_csv_file(f'../data/R_4_08_30_freq_sweep.csv',
                                   delimiter=',',
                                   start_line=3)

     frequencies = get_unique_frequencies(data)
     
     # Extract impedance data by frequency.
     unique_frequencies = get_unique_frequencies(data)
     values_by_frequency = get_data_by_frequency(data, headers)
     impedance_data_real = extract_data_by_header(values_by_frequency, 'Z\' (Ohm)')
     impedance_data_im = extract_data_by_header(values_by_frequency, 'Z\'\' (Ohm)')

     # Plot impedance data by frequency.
     set_plotting_defaults()
     frequency_sets = {
          'lower': unique_frequencies[4:7],
          'upper': unique_frequencies[-10:],
          'middle': unique_frequencies[-14:-6]
     }
     
     for set_name, selected_frequencies in frequency_sets.items():
          fig, ax = plt.subplots()
          ax.invert_yaxis()
          plot_impedance_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, axis=ax)
          if set_name == 'upper':
               circle_fits = fit_circles_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im)
               plot_circle_fit(circle_fits, axis=ax, plot_centers = True)
          plt.savefig(f'../output/08_30/impedance_data_{set_name}.png', dpi=500, bbox_inches='tight')

     # Plot circle radius as a function of frequency.
     fig, ax = plt.subplots()
     selected_frequencies = frequency_sets['upper']
     plot_omega_vs_radius(selected_frequencies, circle_fits, axis=ax, x_scale=1e3)

     # Fit inverse quadratic to radius vs. omega and plot fit
     radii = [circle_fits[freq][2] for freq in selected_frequencies]
     custom_initial_guess = [0, 1e16, 4.5e5]
     result = fit_data(selected_frequencies, radii, 'Inverse Quadratic', inverse_quadratic, initial_guess=custom_initial_guess)
     print(f"Result: {result}")
     plot_fit(ax, selected_frequencies, result, 'Inverse Quadratic', inverse_quadratic, color='b', x_scale=1e3)

     plt.savefig(f'../output/08_30/radius_vs_omega.png', dpi=500, bbox_inches='tight')