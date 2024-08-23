import numpy as np
from collections import defaultdict

def get_unique_frequencies(data, frequency_header='Frequency (Hz)'):
    """
    Return a list of unique frequencies from the data.
    """
    unique_frequencies = np.unique(data[frequency_header])
    unique_frequencies = unique_frequencies[~np.isnan(unique_frequencies)]
    return unique_frequencies[unique_frequencies.astype(bool)]

def _build_datapoint_dict(data, headers, datapoint_idx):
    """
    Return a dictionary of the data point.
    """
    return {header: data[header][datapoint_idx] for header in headers}

# Output takes the form {frequency: [{header: value}, ]}
def get_data_by_frequency(data, headers, frequency_header='Frequency (Hz)'):
    unique_frequencies = get_unique_frequencies(data)
    values_by_frequency = defaultdict(list)

    for datapoint_idx, frequency in enumerate(data[frequency_header]):
        if frequency in unique_frequencies:
            values_by_frequency[frequency].append(_build_datapoint_dict(data, headers, datapoint_idx))
    
    return values_by_frequency

def extract_data_by_header(values_by_frequency, header):
    """
    Return a list of values for a given header.
    """
    return {frequency: [datapoint[header] for datapoint in values_by_frequency[frequency]] for frequency in values_by_frequency.keys()}