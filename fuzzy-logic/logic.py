def simple_fan_control(temperature):
    if temperature <= 20:
        fan_speed = 30  # Slow
    elif 20 < temperature <= 30:
        fan_speed = 60  # Medium
    else:
        fan_speed = 100  # Fast
    return fan_speed

# Example Temperatures
temperatures = [18, 22, 27, 35]
for temp in temperatures:
    speed = simple_fan_control(temp)
    print(f"Temperature: {temp}°C -> Fan Speed: {speed}%")