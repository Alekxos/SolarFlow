import numpy as np
from matplotlib import pyplot as plt

from solarflow.inout import read_csv_file, combine_data_from_list
from solarflow.data import get_unique_frequencies, get_data_by_frequency, extract_data_by_header, gen_path_list_from_dir
from solarflow.plot import plot_impedance_by_frequency, plot_circle_fit, set_plotting_defaults, plot_theta_vs_voltage, plot_omega_vs_radius, plot_fit
from solarflow.fit import fit_data, inverse_quadratic
from solarflow.analysis import fit_circles_by_frequency, extract_theta_by_frequency

if __name__ == '__main__':
     
     # 100um Square
     root = '../data/Sq_100_'
     
     # Plot impedance data by frequency, set allowed frequencies by resistor
     set_plotting_defaults()
     Sq100_Resistances = {
          # '0 Ohm': [1E6, 5E5, 1E5],
          # '1.5 kOhm': [1E6, 5E5, 1E5],
          '10 kOhm': [1E6, 7E5, 6.5E5, 6E5, 5.9E5, 5.7E5, 5E5, 1E5] #5.5E5, 5.3E5, 5.1E5, 
          # '563 kOhm': [1E6, 5E5, 1E5]
     }
     
     for set_name, selected_frequencies in Sq100_Resistances.items():
          directory = root+set_name
          filelist = gen_path_list_from_dir(directory)
          headers, data = combine_data_from_list(filelist)
          
          # Extract impedance data by frequency.
          frequencies = get_unique_frequencies(data)
          unique_frequencies = get_unique_frequencies(data)
          values_by_frequency = get_data_by_frequency(data, headers, frequency_override=Sq100_Resistances[set_name])
          impedance_data_real = extract_data_by_header(values_by_frequency, 'Z\' (Ohm)')
          impedance_data_im = extract_data_by_header(values_by_frequency, 'Z\'\' (Ohm)')
          
          fig, ax = plt.subplots()
          ax.invert_yaxis()
          ax.spines['left'].set_position('center')
          ax.spines['bottom'].set_position('center')
          ax.spines['right'].set_color('none')
          ax.spines['top'].set_color('none')
          plot_impedance_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, axis=ax)
          circle_fits = fit_circles_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im)
          plot_circle_fit(circle_fits, axis=ax, plot_centers = True)
          plt.savefig(f'../output/09_05/100_Sq_impedance_data_{set_name}_selected_frequencies.png', dpi=500, bbox_inches='tight')

     # # Plot circle radius as a function of frequency.
     # fig, ax = plt.subplots()
     # selected_frequencies = frequency_sets['10 kOhm']
     # plot_omega_vs_radius(selected_frequencies, circle_fits, axis=ax, x_scale=1e3)

     # # Fit inverse quadratic to radius vs. omega and plot fit
     # radii = [circle_fits[freq][2] for freq in selected_frequencies]
     # custom_initial_guess = [0, 1e16, 4.5e5]
     # result = fit_data(selected_frequencies, radii, 'Inverse Quadratic', inverse_quadratic, initial_guess=custom_initial_guess)
     # print(f"Result: {result}")
     # plot_fit(ax, selected_frequencies, result, 'Inverse Quadratic', inverse_quadratic, color='b', x_scale=1e3)

     # plt.savefig(f'../output/09_05/radius_vs_omega.png', dpi=500, bbox_inches='tight')