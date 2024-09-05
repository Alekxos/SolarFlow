import numpy as np
from matplotlib import pyplot as plt

from solarflow.inout import read_csv_file
from solarflow.data import get_unique_frequencies, get_data_by_frequency, extract_data_by_header
from solarflow.plot import plot_impedance_by_frequency, plot_circle_fit, set_plotting_defaults, plot_theta_vs_voltage, plot_omega_vs_radius
from solarflow.analysis import fit_circles_by_frequency, extract_theta_by_frequency

def analysis(device_keys):
     for device_key in device_keys:
          # Read data from a csv file.
          headers, data = read_csv_file(f'/Users/minerva/Lab/SolarFlow/data/{device_key}_08_21_freq_sweep.csv',
                                        delimiter=',',
                                        start_line=3)
          
          # Extract impedance data by frequency.
          unique_frequencies = get_unique_frequencies(data)
          values_by_frequency = get_data_by_frequency(data, headers)
          impedance_data_real = extract_data_by_header(values_by_frequency, 'Z\' (Ohm)')
          impedance_data_im = extract_data_by_header(values_by_frequency, 'Z\'\' (Ohm)')
          
          # Plot impedance data by frequency.
          set_plotting_defaults()
          fig, ax = plt.subplots()
          if device_key == 'R_2':
               selected_frequencies = unique_frequencies[5:]
          elif device_key == 'R_4':
               selected_frequencies = unique_frequencies[-1:]
          else:
               raise ValueError('Invalid device key')
          print(f"Selected frequencies: {selected_frequencies}")
          plot_impedance_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, axis=ax)
          
          # Fit a circle to the impedance data.
          circle_fits = fit_circles_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im)
          plot_circle_fit(circle_fits, axis=ax, plot_centers = True)
          plt.savefig(f'/Users/minerva/Lab/SolarFlow/output/08_21/{device_key}/circle_fits.png', dpi=500, bbox_inches='tight')

          # Extract voltage and $\Theta$ data by frequency.
          voltage_data = extract_data_by_header(values_by_frequency, 'Voltage (V)')
          theta_data = extract_theta_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, circle_fits)

          # Plot $\Theta$ data by selected frequency.
          fig, ax = plt.subplots()
          plot_theta_vs_voltage(selected_frequencies, theta_data, voltage_data, axis=ax)
          plt.savefig(f'/Users/minerva/Lab/SolarFlow/output/08_21/{device_key}/theta_vs_voltage.png', dpi=500, bbox_inches='tight')

          # Plot circle radius as a function of frequency.
          fig, ax = plt.subplots()
          plot_omega_vs_radius(selected_frequencies, circle_fits, axis=ax)
          plt.savefig(f'/Users/minerva/Lab/SolarFlow/output/08_21/{device_key}/radius_vs_omega.png', dpi=500, bbox_inches='tight')

          if device_key == 'R_2':
               fig, ax = plt.subplots()
               # Extract closest circle center to origin
               circle_centers = np.array([circle_fits[freq][:2] for freq in selected_frequencies])
               apex_center = min(circle_centers, key=lambda x: np.linalg.norm(x))
               print(f"Apex center: {apex_center}")
               # Replot impedance data by frequency, with circle fits
               plot_impedance_by_frequency(selected_frequencies, impedance_data_real, impedance_data_im, axis=ax, add_to_legend=False)
               plot_circle_fit(circle_fits, axis=ax, plot_centers = True)

               # Extract and plot line of bijection using apex center
               line_of_bijection = np.array([apex_center, [0, 0]])
               angle = np.arctan2(line_of_bijection[0][1], line_of_bijection[0][0])
               angle_degrees = angle * 180 / np.pi
               print(f"Angle (degrees): {angle_degrees}")
               ax.axline(line_of_bijection[0], line_of_bijection[1], color='black', linestyle='--', label='Line of Bijection\n' + rf'(angle={angle_degrees:.2f}$^\circ$)')
               ax.plot(apex_center[0], apex_center[1], marker='o', color='gold', label=f'Apex Center\n({apex_center[0]:.2f}, {apex_center[1]:.2f})')
               ax.legend(loc='lower right')
               plt.savefig(f'/Users/minerva/Lab/SolarFlow/output/08_21/{device_key}/line_of_bijection.png', dpi=500, bbox_inches='tight')



if __name__ == '__main__':
     analysis(['R_4', 'R_2'])