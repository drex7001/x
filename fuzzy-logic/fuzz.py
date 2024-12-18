import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. Define the inputs (temperature and humidity) and output (fan speed)
temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')  # 0°C to 40°C
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')        # 0% to 100%
fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')      # 0% to 100%

# Print the universe values of temperature, humidity, and fan_speed
print("Temperature universe values:", temperature.universe)
print("Humidity universe values:", humidity.universe)
print("Fan speed universe values:", fan_speed.universe)

# 2. Define fuzzy sets using membership functions
# Temperature fuzzy sets
temperature['cool'] = fuzz.trimf(temperature.universe, [0, 0, 20])
temperature['warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 50])

# Humidity fuzzy sets
humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [30, 50, 70])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 100, 100])

# Fan speed fuzzy sets
fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [60, 100, 100])

# 3. Define advanced fuzzy rules
rule1 = ctrl.Rule(temperature['cool'] & humidity['low'], fan_speed['slow'])
rule2 = ctrl.Rule(temperature['cool'] & humidity['medium'], fan_speed['slow'])
rule3 = ctrl.Rule(temperature['cool'] & humidity['high'], fan_speed['medium'])

rule4 = ctrl.Rule(temperature['warm'] & humidity['low'], fan_speed['medium'])
rule5 = ctrl.Rule(temperature['warm'] & humidity['medium'], fan_speed['medium'])
rule6 = ctrl.Rule(temperature['warm'] & humidity['high'], fan_speed['fast'])

rule7 = ctrl.Rule(temperature['hot'] & humidity['low'], fan_speed['fast'])
rule8 = ctrl.Rule(temperature['hot'] & humidity['medium'], fan_speed['fast'])
rule9 = ctrl.Rule(temperature['hot'] & humidity['high'], fan_speed['fast'])

# 4. Create control system and simulation
fan_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
fan_simulation = ctrl.ControlSystemSimulation(fan_control)

# 5. List of input values (temperature and humidity)
input_values = [
    (10, 30),
    (15, 50),
    (20, 80),
    (25, 40),
    (30, 60),
    (35, 90),
    (40, 10),
    (50, 20),
    (60, 50),
    (70, 5),
    (80, 10),
]

# 6. Compute fan speed for each input pair
print("Temperature and Humidity to Fan Speed Mapping:")
for temp, hum in input_values:
    fan_simulation.input['temperature'] = temp
    fan_simulation.input['humidity'] = hum
    fan_simulation.compute()
    print(f"Temperature: {temp}°C, Humidity: {hum}% -> Fan Speed: {fan_simulation.output['fan_speed']:.2f}%")

# Optional: Visualize the fuzzy membership functions
temperature.view()  # Temperature fuzzy sets
humidity.view()     # Humidity fuzzy sets
fan_speed.view()    # Fan speed fuzzy sets
plt.show()


# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
# import matplotlib.pyplot as plt

# # 1. Define the input (temperature) and output (fan speed)
# temperature = ctrl.Antecedent(np.arange(0, 41, 1), 'temperature')  # 0°C to 40°C
# fan_speed = ctrl.Consequent(np.arange(0, 101, 1), 'fan_speed')     # 0% to 100%

# # Print the universe values of temperature and fan_speed
# print("Temperature universe values:", temperature.universe)
# print("Fan speed universe values:", fan_speed.universe)

# # 2. Define fuzzy sets using membership functions
# temperature['cool'] = fuzz.trimf(temperature.universe, [0, 0, 20])
# temperature['warm'] = fuzz.trimf(temperature.universe, [15, 25, 35])
# temperature['hot'] = fuzz.trimf(temperature.universe, [30, 40, 50])

# fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 50])
# fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [30, 50, 70])
# fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [60, 100, 100])

# # 3. Define fuzzy rules
# rule1 = ctrl.Rule(temperature['cool'], fan_speed['slow'])
# rule2 = ctrl.Rule(temperature['warm'], fan_speed['medium'])
# rule3 = ctrl.Rule(temperature['hot'], fan_speed['fast'])

# # 4. Create control system and simulation
# fan_control = ctrl.ControlSystem([rule1, rule2, rule3])
# fan_simulation = ctrl.ControlSystemSimulation(fan_control)

# # 5. List of input temperatures
# input_temperatures = [0,10,20,30,40,50,60,70,80,90,100]  # Example temperatures,

# # 6. Compute fan speed for each temperature
# print("Temperature to Fan Speed Mapping:")
# for temp in input_temperatures:
#     fan_simulation.input['temperature'] = temp
#     fan_simulation.compute()
#     print(f"Temperature: {temp}°C -> Fan Speed: {fan_simulation.output['fan_speed']:.2f}%")

# # Optional: Visualize the fuzzy membership functions
# temperature.view()  # Temperature fuzzy sets
# fan_speed.view()    # Fan speed fuzzy sets
# plt.show()
