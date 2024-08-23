from collections import defaultdict
import numpy as np

def read_csv_file(file_name, verbose=True, delimiter=',', start_line=0):
    """
    Read a csv file and return a list of lists.
    """
    headers = []
    data = defaultdict(list)
    with open(file_name, 'r') as f:
        for i, line in enumerate(f):
            if i < start_line:
                continue
            elif i == start_line:
                headers =line.strip().split(delimiter)
            else:
                for column, value in enumerate(line.strip().split(delimiter)):
                    data[headers[column]].append(value)
    if verbose:
        print(f"Read {len(data)} lines from {file_name}")
    for key in data.keys():
        data[key] = np.array([float(value) if value != '' else np.nan for value in data[key]])
    return headers, data