import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Define the universe (temperature range: 0 to 40°C)
temperature_universe = np.arange(0, 41, 1)

# Define Gaussian membership functions
cool = fuzz.gaussmf(temperature_universe, mean=10, sigma=5)   # Gaussian with mean=10, sigma=5
warm = fuzz.gaussmf(temperature_universe, mean=25, sigma=10)   # Gaussian with mean=25, sigma=5
hot = fuzz.gaussmf(temperature_universe, mean=35, sigma=5)    # Gaussian with mean=35, sigma=5

# Plot the membership functions
plt.figure(figsize=(10, 5))
plt.plot(temperature_universe, cool, label="Cool", color="blue")
plt.plot(temperature_universe, warm, label="Warm", color="orange")
plt.plot(temperature_universe, hot, label="Hot", color="red")
plt.title("Non-Linear Membership Functions (Gaussian) - Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Membership Degree")
plt.legend()
plt.grid()
plt.show()
