# --------------------------------------------------
# 1. Define membership functions for INPUTS
#    Room Temperature (°C): Cold, Warm, Hot
#    Fan Setting (%): Low, Medium, High
# --------------------------------------------------

def mem_temp_cold(T):
    """
    Piecewise-constant membership for 'Cold' in [0..40 °C].
    """
    if 0 <= T <= 10:
        return 1.0
    elif 10 < T <= 20:
        return 0.4
    else:
        return 0.0

def mem_temp_warm(T):
    """
    Piecewise-constant membership for 'Warm' in [0..40 °C].
    """
    if 0 <= T <= 10:
        return 0.0
    elif 10 < T <= 20:
        return 0.6
    elif 20 < T <= 30:
        return 0.9
    elif 30 < T <= 40:
        return 0.5
    else:
        return 0.0

def mem_temp_hot(T):
    """
    Piecewise-constant membership for 'Hot' in [0..40 °C].
    """
    if 0 <= T <= 10:
        return 0.0
    elif 10 < T <= 20:
        return 0.0
    elif 20 < T <= 30:
        return 0.8
    elif 30 < T <= 40:
        return 1.0
    else:
        return 0.0

def mem_fan_low(F):
    """
    Piecewise-constant membership for 'Low' in [0..100%].
    """
    if 0 <= F <= 20:
        return 1.0
    elif 21 <= F <= 40:
        return 0.3
    else:
        return 0.0

def mem_fan_medium(F):
    """
    Piecewise-constant membership for 'Medium' in [0..100%].
    """
    if 0 <= F <= 20:
        return 0.0
    elif 21 <= F <= 40:
        return 0.4
    elif 41 <= F <= 70:
        return 0.8
    elif 71 <= F <= 100:
        return 0.5
    else:
        return 0.0

def mem_fan_high(F):
    """
    Piecewise-constant membership for 'High' in [0..100%].
    """
    if 0 <= F <= 20:
        return 0.0
    elif 21 <= F <= 40:
        return 0.2
    elif 41 <= F <= 70:
        return 0.7
    elif 71 <= F <= 100:
        return 1.0
    else:
        return 0.0

# --------------------------------------------------
# 2. Define membership functions for the OUTPUT
#    Fan Speed (rpm): Low, Medium, High  in [0..2000 rpm]
# --------------------------------------------------

def mem_out_low(rpm):
    """
    Piecewise-constant membership for output 'Low' (0..2000 rpm).
    """
    if 0 <= rpm <= 500:
        return 1.0
    elif 501 <= rpm <= 1000:
        return 0.4
    else:
        return 0.0

def mem_out_medium(rpm):
    """
    Piecewise-constant membership for output 'Medium' (0..2000 rpm).
    """
    if 0 <= rpm <= 500:
        return 0.0
    elif 501 <= rpm <= 1000:
        return 0.3
    elif 1001 <= rpm <= 1500:
        return 0.8
    elif 1501 <= rpm <= 2000:
        return 0.5
    else:
        return 0.0

def mem_out_high(rpm):
    """
    Piecewise-constant membership for output 'High' (0..2000 rpm).
    """
    if 0 <= rpm <= 500:
        return 0.0
    elif 501 <= rpm <= 1000:
        return 0.2
    elif 1001 <= rpm <= 1500:
        return 0.6
    elif 1501 <= rpm <= 2000:
        return 1.0
    else:
        return 0.0

# --------------------------------------------------
# 3. Given inputs: T=22°C, Fan=60%
#    Evaluate membership of each fuzzy set
# --------------------------------------------------

T = 22
F = 60

cold = mem_temp_cold(T)
warm = mem_temp_warm(T)
hot  = mem_temp_hot(T)

low_f   = mem_fan_low(F)
med_f   = mem_fan_medium(F)
high_f  = mem_fan_high(F)

print("Input memberships:")
print(f"  Cold={cold}, Warm={warm}, Hot={hot}")
print(f"  Low={low_f}, Medium={med_f}, High={high_f}")

# --------------------------------------------------
# 4. Rules (AND = min), Zadeh's max-min inference
#    Rules:
#       R1: If Cold & Low -> Speed = Low
#       R2: If Warm & Medium -> Speed = Medium
#       R3: If Hot & High -> Speed = High
#       R4: If Warm & Low -> Speed = Low
#       R5: If Hot & Medium -> Speed = Medium
# --------------------------------------------------

# Compute firing strengths
r1 = min(cold, low_f)       # -> Low
r2 = min(warm, med_f)       # -> Medium
r3 = min(hot,  high_f)      # -> High
r4 = min(warm, low_f)       # -> Low
r5 = min(hot,  med_f)       # -> Medium

print("\nRule firing strengths:")
print(f"  R1 (Cold & Low) -> Low: {r1}")
print(f"  R2 (Warm & Med) -> Med: {r2}")
print(f"  R3 (Hot & High) -> High: {r3}")
print(f"  R4 (Warm & Low) -> Low: {r4}")
print(f"  R5 (Hot & Med) -> Med: {r5}")

# --------------------------------------------------
# 5. Truncate/scale the output membership functions
#    Low set => max firing: L_strength = max(r1, r4) ... but both are 0
#    Medium set => max firing: M_strength = max(r2, r5) = 0.8
#    High set => H_strength = r3 = 0.7
# --------------------------------------------------

L_strength = max(r1, r4)  # = 0.0
M_strength = max(r2, r5)  # = 0.8
H_strength = r3           # = 0.7

print("\nOutput fuzzy-set strengths:")
print(f"  Low={L_strength}, Medium={M_strength}, High={H_strength}")

# --------------------------------------------------
# 6. Build the aggregated membership for output, mu_out(x) = max( truncated(M), truncated(H) ).
#    We'll do it by piecewise sections, as in the example:
#
#    For Medium at 0.8: we clip mem_out_medium(x) at 0.8
#    For High at 0.7:   we clip mem_out_high(x)   at 0.7
#
#    Then take pointwise max.
# --------------------------------------------------

def truncated_mem_out_medium(x):
    return min(mem_out_medium(x), M_strength)

def truncated_mem_out_high(x):
    return min(mem_out_high(x), H_strength)

def aggregated_output(x):
    # Low doesn't fire (strength=0), so we only combine Medium/High
    return max(truncated_mem_out_medium(x), truncated_mem_out_high(x))

# --------------------------------------------------
# 7. Defuzzify via centroid (discretized or piecewise approach).
#    We'll replicate the rectangle approach from the example.
#
#    From the example, the final aggregated membership was:
#        0.0 in [0..500]
#        0.3 in [501..1000]   <-- max(0.3 from Medium, 0.2 from High)
#        0.8 in [1001..1500]  <-- max(0.8 from Medium, 0.6 from High)
#        0.7 in [1501..2000]  <-- max(0.5 from Medium, 1 from High clipped to 0.7)
#
#    We'll compute area & centroid of each rectangle exactly.
# --------------------------------------------------

import numpy as np

# Rectangle 1: x in [501..1000], height=0.3
x1_start, x1_end, h1 = 501, 1000, 0.3
width1 = x1_end - x1_start
area1 = width1 * h1
centroid1 = 0.5*(x1_start + x1_end)
moment1 = area1 * centroid1

# Rectangle 2: x in [1001..1500], height=0.8
x2_start, x2_end, h2 = 1001, 1500, 0.8
width2 = x2_end - x2_start
area2 = width2 * h2
centroid2 = 0.5*(x2_start + x2_end)
moment2 = area2 * centroid2

# Rectangle 3: x in [1501..2000], height=0.7
x3_start, x3_end, h3 = 1501, 2000, 0.7
width3 = x3_end - x3_start
area3 = width3 * h3
centroid3 = 0.5*(x3_start + x3_end)
moment3 = area3 * centroid3

# Summation
A_total = area1 + area2 + area3
M_total = moment1 + moment2 + moment3

rpm_crisp = M_total / A_total

print("\n-- Defuzzification (Rectangle/Centroid) --")
print(f" Rectangle 1: area={area1:.2f}, centroid={centroid1:.2f}, moment={moment1:.2f}")
print(f" Rectangle 2: area={area2:.2f}, centroid={centroid2:.2f}, moment={moment2:.2f}")
print(f" Rectangle 3: area={area3:.2f}, centroid={centroid3:.2f}, moment={moment3:.2f}")
print(f"\n Total Area = {A_total:.2f}")
print(f" Total Moment = {M_total:.2f}")
print(f" Defuzzified Fan Speed = {rpm_crisp:.2f} rpm")
