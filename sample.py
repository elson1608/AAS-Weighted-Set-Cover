import numpy as np
from scipy.stats import geom, randint, variation
import sys

# Define a function to update the plot
def sample(cv, n):
    if cv > 1 or cv < 0:
        print('cv must be in [0,1)')
    if cv == 0:
        return np.ones(n, dtype=np.uint8)
    elif cv == 1:
        # Sample n positive integers uniformly
        sample = randint.rvs(1, 100, size=n)
        return sample
    else:
        p = 1 - cv**2
        sample = geom.rvs(p, size=n)
        iterations = 0
    while True:
        current_cv = variation(sample, ddof=1)
        current_mean = np.mean(sample)
        diff = np.abs(cv - current_cv)
        if diff < 10**(-3) or iterations > n/100:
            break

        if current_cv > cv:
            # Find the index of the value furthest from the mean
            index = np.argmax(np.abs(sample - current_mean))
            
            # Move the value closer to the mean by adjusting based on its relation to the mean
            if sample[index] > current_mean:
                sample[index] = max(1, sample[index] - int(10**diff * np.log10(n)))
            else:
                sample[index] = max(1, sample[index] + int(10**diff * np.log10(n)))
        else:
            # Find the index of the value closest to the mean, but only if it's greater than 1
            # since costs can't be 0
            valid_values = [val for val in sample if val > 1]
            if not valid_values:
                print('no valid values left')
                break  # No progress can be made if all values are 1 or less

            # Find the index of the value closest to the mean
            index = np.argmin(np.abs(valid_values - current_mean))
            index = np.where(sample == valid_values[index])[0][0]
            # Move the value away from the mean by adjusting based on its relation to the mean
            if sample[index] > current_mean:
                sample[index] = max(1, sample[index] + int(10**diff * np.log10(n)))
            else:
                sample[index] = max(1, sample[index] - int(10**diff * np.log10(n)))
            iterations += 1
    return sample