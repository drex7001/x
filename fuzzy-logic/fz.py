import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt

class FuzzyTemperatureController:
    def __init__(self):
        # Create fuzzy variables
        self.temperature = ctrl.Antecedent(np.arange(0, 51, 1), 'temperature')
        self.heating_power = ctrl.Consequent(np.arange(0, 101, 1), 'heating_power')

        # Define fuzzy membership functions for temperature
        self.temperature['very_cold'] = fuzz.trimf(self.temperature.universe, [0, 0, 15])
        self.temperature['cold'] = fuzz.trimf(self.temperature.universe, [10, 20, 30])
        self.temperature['mild'] = fuzz.trimf(self.temperature.universe, [20, 25, 35])
        self.temperature['warm'] = fuzz.trimf(self.temperature.universe, [30, 40, 50])
        self.temperature['hot'] = fuzz.trimf(self.temperature.universe, [40, 50, 50])

        # Define fuzzy membership functions for heating power
        self.heating_power['low'] = fuzz.trimf(self.heating_power.universe, [0, 0, 50])
        self.heating_power['medium'] = fuzz.trimf(self.heating_power.universe, [0, 50, 100])
        self.heating_power['high'] = fuzz.trimf(self.heating_power.universe, [50, 100, 100])

        # Define fuzzy rules
        rule1 = ctrl.Rule(self.temperature['very_cold'], self.heating_power['high'])
        rule2 = ctrl.Rule(self.temperature['cold'], self.heating_power['medium'])
        rule3 = ctrl.Rule(self.temperature['mild'], self.heating_power['low'])
        rule4 = ctrl.Rule(self.temperature['warm'], self.heating_power['low'])
        rule5 = ctrl.Rule(self.temperature['hot'], self.heating_power['low'])

        # Create control system
        self.heating_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        self.heating = ctrl.ControlSystemSimulation(self.heating_ctrl)

    def control_heating(self, temperature):
        """
        Compute heating power for a given temperature
        """
        # Pass the input temperature to the control system
        self.heating.input['temperature'] = temperature
        
        # Compute the output
        self.heating.compute()
        
        return self.heating.output['heating_power']

    def visualize_membership_functions(self):
        """
        Visualize temperature and heating power membership functions
        """
        # Visualize temperature membership functions
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        for label in self.temperature.terms:
            plt.plot(self.temperature.universe, 
                     self.temperature[label].mf, 
                     label=label)
        plt.title('Temperature Membership Functions')
        plt.xlabel('Temperature (°C)')
        plt.ylabel('Membership Degree')
        plt.legend()

        # Visualize heating power membership functions
        plt.subplot(1, 2, 2)
        for label in self.heating_power.terms:
            plt.plot(self.heating_power.universe, 
                     self.heating_power[label].mf, 
                     label=label)
        plt.title('Heating Power Membership Functions')
        plt.xlabel('Heating Power')
        plt.ylabel('Membership Degree')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def detailed_analysis(self, temperature):
        """
        Provide detailed fuzzy logic analysis
        """
        # Compute membership degrees
        temp_memberships = {
            label: fuzz.interp_membership(self.temperature.universe, 
                                          self.temperature[label].mf, 
                                          temperature)
            for label in self.temperature.terms
        }
        
        # Compute heating power
        heating_power = self.control_heating(temperature)
        
        return {
            'temperature': temperature,
            'temperature_memberships': temp_memberships,
            'heating_power': heating_power
        }

# Demonstration
def main():
    # Create fuzzy controller
    controller = FuzzyTemperatureController()
    
    # Visualize membership functions
    controller.visualize_membership_functions()
    
    # Test temperatures
    test_temperatures = [5, 17, 23, 35, 42]
    
    print("Fuzzy Logic Temperature Control Analysis:")
    for temp in test_temperatures:
        analysis = controller.detailed_analysis(temp)
        
        print(f"\nTemperature: {temp}°C")
        print("Temperature Memberships:")
        for category, degree in analysis['temperature_memberships'].items():
            print(f"  {category}: {degree:.2f}")
        
        print(f"Recommended Heating Power: {analysis['heating_power']:.2f}")


main()