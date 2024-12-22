import numpy as np
import matplotlib.pyplot as plt

class FuzzyRestaurantSystem:
    def __init__(self):
        # Universe of discourse
        self.price_range = np.arange(0, 101, 1)  # 0-100 dollars
        self.quality_range = np.arange(0, 11, 1)  # 0-10 rating
        
    def price_membership(self, price):
        """Calculate membership values for price categories"""
        cheap = max(0, min((40 - price) / 40, 1))
        moderate = max(0, min((price - 20) / 30, (80 - price) / 30))
        expensive = max(0, min((price - 60) / 40, 1))
        return {'cheap': cheap, 'moderate': moderate, 'expensive': expensive}
    
    def quality_membership(self, quality):
        """Calculate membership values for quality categories"""
        poor = max(0, min((4 - quality) / 4, 1))
        average = max(0, min((quality - 2) / 3, (8 - quality) / 3))
        excellent = max(0, min((quality - 6) / 4, 1))
        return {'poor': poor, 'average': average, 'excellent': excellent}
    
    def cylindrical_extension(self, price_val, quality_val):
        """Perform cylindrical extension of price and quality memberships"""
        price_memberships = self.price_membership(price_val)
        quality_memberships = self.quality_membership(quality_val)
        
        # Create 2D membership matrix
        extended_memberships = {}
        for p_cat, p_val in price_memberships.items():
            for q_cat, q_val in quality_memberships.items():
                key = (p_cat, q_cat)
                # Take minimum of memberships for conjunction
                extended_memberships[key] = min(p_val, q_val)
        
        return extended_memberships
    
    def projection(self, extended_memberships, project_on='price'):
        """Project the fuzzy relation onto either price or quality dimension"""
        projected = {}
        
        if project_on == 'price':
            categories = ['cheap', 'moderate', 'expensive']
        else:  # project on quality
            categories = ['poor', 'average', 'excellent']
            
        for category in categories:
            # Find maximum membership value for each category
            relevant_pairs = [v for k, v in extended_memberships.items() 
                            if k[0 if project_on == 'price' else 1] == category]
            projected[category] = max(relevant_pairs) if relevant_pairs else 0
            
        return projected

    def recommend(self, price, quality):
        """Provide restaurant recommendation based on price and quality"""
        # Perform cylindrical extension
        extended = self.cylindrical_extension(price, quality)
        
        # Project onto both dimensions
        price_proj = self.projection(extended, 'price')
        quality_proj = self.projection(extended, 'quality')
        
        return {
            'extended_memberships': extended,
            'price_projection': price_proj,
            'quality_projection': quality_proj
        }

# Example usage
system = FuzzyRestaurantSystem()

# Let's analyze a restaurant with $45 price and 7.5 quality rating
price = 45
quality = 7.5

result = system.recommend(price, quality)

# Print results
print(f"\nAnalyzing restaurant with price ${price} and quality rating {quality}")
print("\nCylindrical Extension Results:")
for (p_cat, q_cat), membership in result['extended_memberships'].items():
    if membership > 0:
        print(f"Price: {p_cat}, Quality: {q_cat} -> Membership: {membership:.2f}")

print("\nPrice Projection Results:")
for category, membership in result['price_projection'].items():
    print(f"{category}: {membership:.2f}")

print("\nQuality Projection Results:")
for category, membership in result['quality_projection'].items():
    print(f"{category}: {membership:.2f}")
    
# import numpy as np
# import skfuzzy as fuzz
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # Step 1: Define the fuzzy set for temperature
# temp = np.arange(0, 51, 1)  # Temperature range from 0°C to 50°C
# comfortable_temp = fuzz.trapmf(temp, [18, 22, 26, 30])  # Comfortable range is 18-30°C

# # Plot the original fuzzy set
# plt.figure(figsize=(10, 5))
# plt.plot(temp, comfortable_temp, label="Comfortable Temperature", color="blue")
# plt.title("1D Fuzzy Set: Comfortable Temperature")
# plt.xlabel("Temperature (°C)")
# plt.ylabel("Membership Degree")
# plt.legend()
# plt.grid()
# plt.show()

# # Step 2: Cylindrical extension to include humidity
# humidity = np.arange(0, 101, 1)  # Humidity range from 0% to 100%
# temp_mesh, hum_mesh = np.meshgrid(temp, humidity)

# # Extend the fuzzy set
# comfortable_weather = np.minimum(
#     np.expand_dims(comfortable_temp, axis=0),
#     np.ones_like(temp_mesh)
# )

# # Step 3: Visualize the 3D fuzzy set (Cylindrical Extension)
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111, projection='3d')

# # Create the surface plot
# surface = ax.plot_surface(temp_mesh, hum_mesh, comfortable_weather, cmap="coolwarm", edgecolor='k', alpha=0.8)
# fig.colorbar(surface, ax=ax, label="Membership Degree")

# # Set labels and title
# ax.set_title("3D Fuzzy Set: Comfortable Weather (Cylindrical Extension)")
# ax.set_xlabel("Temperature (°C)")
# ax.set_ylabel("Humidity (%)")
# ax.set_zlabel("Membership Degree")
# plt.show()

# # Step 4: Project back to temperature
# projected_temp = np.max(comfortable_weather, axis=0)

# # Plot the projected fuzzy set
# plt.figure(figsize=(10, 5))
# plt.plot(temp, comfortable_temp, label="Original", color="blue", linestyle="dashed")
# plt.plot(temp, projected_temp, label="Projected", color="red")
# plt.title("Projection Back to Temperature")
# plt.xlabel("Temperature (°C)")
# plt.ylabel("Membership Degree")
# plt.legend()
# plt.grid()
# plt.show()

# # import numpy as np
# # import skfuzzy as fuzz
# # import matplotlib.pyplot as plt
# # from mpl_toolkits.mplot3d import Axes3D

# # # Step 1: Define the fuzzy set for temperature
# # temp = np.linspace(10, 40, 50)  # Temperature range from 10°C to 40°C
# # humidity = np.linspace(0, 100, 50)  # Humidity range from 0% to 100%

# # # Create a 2D grid for Temperature (X) and Humidity (Y)
# # temp_grid, hum_grid = np.meshgrid(temp, humidity)

# # # Define a fuzzy set for "Comfortable Temperature" (1D membership function)
# # comfortable_temp = np.maximum(1 - np.abs((temp_grid - 25) / 10), 0)

# # # Cylindrical Extension: Membership degree is constant along Humidity (Y-axis)
# # membership_values = comfortable_temp  # Constant for all Y

# # # Plot the cylindrical extension
# # fig = plt.figure(figsize=(10, 7))
# # ax = fig.add_subplot(111, projection='3d')

# # # Surface plot
# # surface = ax.plot_surface(temp_grid, hum_grid, membership_values, cmap="viridis", edgecolor='none')

# # # Labels and titles
# # ax.set_title("Cylindrical Extension of a Fuzzy Set (Comfortable Temperature)")
# # ax.set_xlabel("Temperature (°C)")
# # ax.set_ylabel("Humidity (%)")
# # ax.set_zlabel("Membership Degree")
# # ax.set_zlim(0, 1)  # Ensure Z-axis is [0, 1]
# # fig.colorbar(surface, ax=ax, label="Membership Degree")
# # plt.show()

# # # Step 2: Project back to temperature (Max membership values along Humidity axis)
# # projected_temp = np.max(membership_values, axis=0)

# # # Plot the original and projected fuzzy set
# # plt.figure(figsize=(10, 5))
# # plt.plot(temp, projected_temp, label="Projected", color="red")
# # plt.title("Projection Back to Temperature")
# # plt.xlabel("Temperature (°C)")
# # plt.ylabel("Membership Degree")
# # plt.legend()
# # plt.grid()
# # plt.show()

# # # import numpy as np
# # # import matplotlib.pyplot as plt

# # # class FuzzyRestaurantSystem:
# # #     def __init__(self):
# # #         # Universe of discourse
# # #         self.price_range = np.arange(0, 101, 1)  # 0-100 dollars
# # #         self.quality_range = np.arange(0, 11, 1)  # 0-10 rating
        
# # #     def price_membership(self, price):
# # #         """Calculate membership values for price categories"""
# # #         cheap = max(0, min((40 - price) / 40, 1))
# # #         moderate = max(0, min((price - 20) / 30, (80 - price) / 30))
# # #         expensive = max(0, min((price - 60) / 40, 1))
# # #         return {'cheap': cheap, 'moderate': moderate, 'expensive': expensive}
    
# # #     def quality_membership(self, quality):
# # #         """Calculate membership values for quality categories"""
# # #         poor = max(0, min((4 - quality) / 4, 1))
# # #         average = max(0, min((quality - 2) / 3, (8 - quality) / 3))
# # #         excellent = max(0, min((quality - 6) / 4, 1))
# # #         return {'poor': poor, 'average': average, 'excellent': excellent}
    
# # #     def cylindrical_extension(self, price_val, quality_val):
# # #         """Perform cylindrical extension of price and quality memberships"""
# # #         price_memberships = self.price_membership(price_val)
# # #         quality_memberships = self.quality_membership(quality_val)
        
# # #         # Create 2D membership matrix
# # #         extended_memberships = {}
# # #         for p_cat, p_val in price_memberships.items():
# # #             for q_cat, q_val in quality_memberships.items():
# # #                 key = (p_cat, q_cat)
# # #                 # Take minimum of memberships for conjunction
# # #                 extended_memberships[key] = min(p_val, q_val)
        
# # #         return extended_memberships
    
# # #     def projection(self, extended_memberships, project_on='price'):
# # #         """Project the fuzzy relation onto either price or quality dimension"""
# # #         projected = {}
        
# # #         if project_on == 'price':
# # #             categories = ['cheap', 'moderate', 'expensive']
# # #         else:  # project on quality
# # #             categories = ['poor', 'average', 'excellent']
            
# # #         for category in categories:
# # #             # Find maximum membership value for each category
# # #             relevant_pairs = [v for k, v in extended_memberships.items() 
# # #                             if k[0 if project_on == 'price' else 1] == category]
# # #             projected[category] = max(relevant_pairs) if relevant_pairs else 0
            
# # #         return projected

# # #     def recommend(self, price, quality):
# # #         """Provide restaurant recommendation based on price and quality"""
# # #         # Perform cylindrical extension
# # #         extended = self.cylindrical_extension(price, quality)
        
# # #         # Project onto both dimensions
# # #         price_proj = self.projection(extended, 'price')
# # #         quality_proj = self.projection(extended, 'quality')
        
# # #         return {
# # #             'extended_memberships': extended,
# # #             'price_projection': price_proj,
# # #             'quality_projection': quality_proj
# # #         }

# # # # Example usage
# # # system = FuzzyRestaurantSystem()

# # # # Let's analyze a restaurant with $45 price and 7.5 quality rating
# # # price = 45
# # # quality = 7.5

# # # result = system.recommend(price, quality)

# # # # Print results
# # # print(f"\nAnalyzing restaurant with price ${price} and quality rating {quality}")
# # # print("\nCylindrical Extension Results:")
# # # for (p_cat, q_cat), membership in result['extended_memberships'].items():
# # #     if membership > 0:
# # #         print(f"Price: {p_cat}, Quality: {q_cat} -> Membership: {membership:.2f}")

# # # print("\nPrice Projection Results:")
# # # for category, membership in result['price_projection'].items():
# # #     print(f"{category}: {membership:.2f}")

# # # print("\nQuality Projection Results:")
# # # for category, membership in result['quality_projection'].items():
# # #     print(f"{category}: {membership:.2f}")
# # # # import numpy as np
# # # # import skfuzzy as fuzz
# # # # import matplotlib.pyplot as plt

# # # # # Step 1: Define the fuzzy set for temperature
# # # # temp = np.arange(0, 51, 1)  # Temperature range from 0°C to 50°C
# # # # comfortable_temp = fuzz.trapmf(temp, [18, 22, 26, 30])  # Comfortable range is 18-30°C

# # # # # Plot the original fuzzy set
# # # # plt.figure(figsize=(10, 5))
# # # # plt.plot(temp, comfortable_temp, label="Comfortable Temperature", color="blue")
# # # # plt.title("1D Fuzzy Set: Comfortable Temperature")
# # # # plt.xlabel("Temperature (°C)")
# # # # plt.ylabel("Membership Degree")
# # # # plt.legend()
# # # # plt.grid()
# # # # plt.show()

# # # # # Step 2: Cylindrical extension to include humidity
# # # # humidity = np.arange(0, 101, 1)  # Humidity range from 0% to 100%
# # # # temp_mesh, hum_mesh = np.meshgrid(temp, humidity)

# # # # # Extend the fuzzy set
# # # # comfortable_weather = np.minimum(
# # # #     np.expand_dims(comfortable_temp, axis=0),
# # # #     np.ones_like(temp_mesh)
# # # # )

# # # # # Step 3: Visualize the 2D fuzzy set
# # # # plt.figure(figsize=(10, 5))
# # # # plt.contourf(temp_mesh, hum_mesh, comfortable_weather, cmap="coolwarm")
# # # # plt.colorbar(label="Membership Degree")
# # # # plt.title("2D Fuzzy Set: Comfortable Weather (Temperature vs. Humidity)")
# # # # plt.xlabel("Temperature (°C)")
# # # # plt.ylabel("Humidity (%)")
# # # # plt.show()

# # # # # Step 4: Project back to temperature
# # # # projected_temp = np.max(comfortable_weather, axis=0)

# # # # # Plot the projected fuzzy set
# # # # plt.figure(figsize=(10, 5))
# # # # plt.plot(temp, comfortable_temp, label="Original", color="blue", linestyle="dashed")
# # # # plt.plot(temp, projected_temp, label="Projected", color="red")
# # # # plt.title("Projection Back to Temperature")
# # # # plt.xlabel("Temperature (°C)")
# # # # plt.ylabel("Membership Degree")
# # # # plt.legend()
# # # # plt.grid()
# # # # plt.show()
