import numpy as np
from scipy.optimize import least_squares

def lorentzian(x, a, b, c, d):
    x = np.array(x)
    return a / (1 + ((x - b) / c) ** 2) + d

def arc_tan(x, a, b, c, d):
    x = np.array(x)
    return a * np.abs(np.arctan(b * x + c)) + d

def modified_lorentzian(x, a, b, c, d):
    x = np.array(x)
    return a / (1 + ((x - b) / c) ** 2) + d * x

def gaussian(x, a, b, c, d):
    x = np.array(x)
    return a * np.exp(-((x - b) / c) ** 2) + d

# def inverse_quadratic(x, a, b, c, d):
#     x = np.array(x)
#     return a + b / ((c * x - d) ** 2)

def inverse_quadratic(x, a, b, c):
    x = np.array(x)
    return a + b / ((x - c) ** 2)

def get_initial_guess(fit_name):
    if fit_name == 'Lorentzian':
        return [-1, 0, 1, 0]
    elif fit_name == 'Arctan':
        return [1, 1, 1, 0]
    elif fit_name == 'Modified Lorentzian':
        return [-1, 0, 1, 0]
    elif fit_name == 'Gaussian':
        return [-1, 0, 1, 0]
    # elif fit_name == 'Inverse Quadratic':
    #     return [0, 1e5, 1 / 1e5, 1]
    elif fit_name == 'Inverse Quadratic':
        return [0, 1, 1]
    else:
        raise ValueError(f"Unknown fit function: {fit_name}")

def fit_data(x, y, fit_name, fit_function, initial_guess=None):
    def residuals(params, x, y):
        return y - fit_function(x, *params)
    
    if not initial_guess:
        initial_guess = get_initial_guess(fit_name)
    result = least_squares(residuals, initial_guess, args=(x, y))
    return result.x
    
def equation_to_string(equation, params):
    """
    Convert an equation and its parameters to a string.
    """
    print(*params)
    if equation is inverse_quadratic:
        omega_star = params[2]
        return rf"$|Z^*| = {params[0]:.3e} + \frac{{{params[1]:.3e}}}{{(\omega - \omega^*)^2}}$" + "\n" + rf"$\Omega^*$ = {omega_star / 1e3:.2f} kHz"
    return ""