import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Define the input (temperature) and output (fan speed)
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')  # 0°C to 40°C
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')     # 0% to 100%

# 2. Define fuzzy sets using membership functions
temperature['cool'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 40])

fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [60, 100, 100])

# 3. Define fuzzy rules
rule1 = ctrl.Rule(temperature['cool'], fan_speed['slow'])
rule2 = ctrl.Rule(temperature['warm'], fan_speed['medium'])
rule3 = ctrl.Rule(temperature['hot'], fan_speed['fast'])

# 4. Create control system and simulation
fan_control = ctrl.ControlSystem([rule1, rule2, rule3])
fan_simulation = ctrl.ControlSystemSimulation(fan_control)

# 5. List of input temperatures
input_temperatures = [-10,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21, 22,23,24,25,26,27,28,29,30,31,32,33,34, 35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,80,90,99,1001556496446]  # Example temperatures,

# 6. Compute fan speed for each temperature
print("Temperature to Fan Speed Mapping:")
for temp in input_temperatures:
    fan_simulation.input['temperature'] = temp
    fan_simulation.compute()
    print(f"Temperature: {temp}°C -> Fan Speed: {fan_simulation.output['fan_speed']:.2f}%")

# Optional: Visualize the fuzzy membership functions
temperature.view()  # Temperature fuzzy sets
fan_speed.view()    # Fan speed fuzzy sets
plt.show()
