import numpy as np
from scipy.optimize import least_squares

# Residuals for least squares fitting
def residuals(params, points):
    xc, yc, r = params
    return np.sqrt((points[:, 0] - xc) ** 2 + (points[:, 1] - yc) ** 2) - r

# Fit single circle and return center and radius
def _fit_circle(points):
    initial_guess = np.mean(points, axis=0).tolist() + [np.mean(np.std(points, axis=0))]
    result = least_squares(residuals, initial_guess, args=(points,))
    xc, yc, r = result.x
    return xc, yc, r

# Fit circles by frequency
def fit_circles_by_frequency(frequencies, impedance_data_real, impedance_data_im):
    fit_results = {}
    for frequency in frequencies:
        points = np.array([impedance_data_real[frequency], impedance_data_im[frequency]]).T
        xc, yc, r = _fit_circle(points)
        fit_results[frequency] = (xc, yc, r)
    return fit_results

def extract_theta_by_frequency(freqs, impedance_data_real, impedance_data_im, circle_fits):
    return {freq: np.arctan2(impedance_data_im[freq]- circle_fits[freq][1], impedance_data_real[freq] - circle_fits[freq][0]) for freq in freqs}