import numpy as np
from matplotlib import pyplot as plt
import os

from solarflow.inout import read_csv_file
from solarflow.plot import set_plotting_defaults

def extract_data_by_header(data, header):
    """
    Extract data for a specific header from the data dictionary.
    """
    return data[header] if header in data else None

def plot_impedance_magnitude_vs_voltage(voltage_data, impedance_magnitude_data, axis):
    """
    Plot impedance magnitude vs voltage.
    """
    axis.plot(voltage_data, impedance_magnitude_data, 'o-', color='#007BA7')
    axis.set_xlabel("Voltage (V)", fontsize=18)
    axis.set_ylabel("|Z| (Ohm)", fontsize=18)
    axis.set_title("Impedance Magnitude vs. Voltage")
    axis.grid(True)

def plot_phase_vs_voltage(voltage_data, phase_data, axis):
    """
    Plot phase vs voltage.
    """
    axis.plot(voltage_data, phase_data, 'o-', color='#9B111e')
    axis.set_xlabel("Voltage (V)", fontsize=18)
    axis.set_ylabel("Phase (Deg)", fontsize=18)
    # Title is set in the overlay plot to avoid duplication
    axis.grid(True)

if __name__ == '__main__':
    # Define file paths
    data_file_path = 'solarflow/source_data/20250429_ScalSt2_Critical Frequency Centered/ACV Sweeps/(23) Sq50um_(5,3)_m1p25V_1p25V_824kHz_I-300uA_1_sweep.csv'
    output_folder_name = '20250429_ScalSt2_Critical Frequency Centered/Sq50um_5_3_m1p25V_1p25V_824kHz'
    output_dir_path = f'solarflow/output/{output_folder_name}'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir_path, exist_ok=True)
    
    # Read data from the csv file
    headers, data = read_csv_file(data_file_path, delimiter=',', start_line=3)
    
    # Extract voltage, impedance magnitude, and phase data
    voltage_data = extract_data_by_header(data, 'Voltage (V)')
    impedance_magnitude_data = extract_data_by_header(data, '| Z | (Ohm)')
    phase_data = extract_data_by_header(data, 'Phase (Deg)')
    
    # Set plotting defaults
    set_plotting_defaults(single_color=True)
    
    # Plot impedance magnitude and phase on the same figure with dual y‑axes
    fig, ax1 = plt.subplots(figsize=(10, 6))
    # Impedance magnitude (left y‑axis)
    plot_impedance_magnitude_vs_voltage(voltage_data, impedance_magnitude_data, axis=ax1)
    ax1.set_ylabel("|Z| (Ohm)", fontsize=18, color='#007BA7')
    ax1.tick_params(axis='y', labelcolor='#007BA7')
    # Phase (right y‑axis)
    ax2 = ax1.twinx()
    plot_phase_vs_voltage(voltage_data, phase_data, axis=ax2)
    ax2.set_ylabel("Phase (Deg)", fontsize=18, color='#9B111e')
    ax2.tick_params(axis='y', labelcolor='#9B111e')
    # Shared x‑label and title
    ax1.set_xlabel("Voltage (V)", fontsize=18)
    ax1.set_title("Impedance Magnitude and Phase vs. Voltage")
    # Combine legends from both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper right')
    plt.savefig(f'{output_dir_path}/impedance_phase_overlay.png', dpi=500, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Plots saved to {output_dir_path}")
