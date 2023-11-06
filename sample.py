import numpy as np

# Define a function to update the plot
def sample(cv, n):
    t = (-3*cv**2 - cv * np.sqrt(5*cv**2 + 4)) / (2*(cv**2-1))
    
    while True:
        sample = np.random.beta(1/t, 1/(t+1), n)
        # Calculate the current coefficient of variation (CV) of the sample
        current_std = np.std(sample)
        current_mean = np.mean(sample)
        sample = current_mean + (sample - current_mean) * (cv * current_mean / current_std)

        if np.all((sample >= 0) & (sample <= 1)):
            return sample