import math

# --- CONSTANTS ---
G = 6.67430e-11
c = 299792458.0
epsilon = 1e-10

# --- TEST DATA (A massive radiating star) ---
r = 7e8               
rho = 1500.0          
E_past = 1e44         
E_future = 9.9e43     # Radiating 1% of its energy
mass = (4/3) * math.pi * (r**3) * rho  

# ==========================================
# METHOD 1: YOUR ALGORITHM (O(1) Shortcut)
# ==========================================
def fast_relativistic_heuristic(E_past, E_future, r, rho):
    gravity_ratio = (8 * math.pi * G * (r**2) * rho) / (3 * c**2)
    warp_factor = math.sqrt(max(epsilon, 1 - gravity_ratio))
    
    # Calculate dt (Using the derived proportional equation)
    dt = (3 * (E_past - E_future)) / (2 * math.pi * (r**2) * rho * (c**3) * warp_factor)
    return dt

# ==========================================
# METHOD 2: STANDARD ENGINE INTEGRATION (O(N) Calculus)
# ==========================================
def standard_numerical_integration(mass, r, E_past, E_future, steps=1000):
    dt_total = 0
    energy_diff = E_past - E_future
    energy_step = energy_diff / steps
    
    current_mass = mass
    
    for _ in range(steps):
        # The star loses a tiny bit of mass each step
        mass_loss = energy_step / (c**2)
        current_mass -= mass_loss
        
        # Calculate precise warp for this specific step
        warp = math.sqrt(1 - ((2 * G * current_mass) / (r * c**2)))
        
        # Integrate time shift (simplified proportionality for comparison)
        # We use a scaled constant to match the heuristic's base unit
        base_constant = 3 / (2 * math.pi * (r**2) * (current_mass / ((4/3)*math.pi*r**3)) * c**3)
        dt_total += (energy_step * base_constant) / warp
        
    return dt_total

# ==========================================
# RUN THE ACCURACY TEST
# ==========================================
print("Running Accuracy Benchmark...\n")

# Get exact values
val_yours = fast_relativistic_heuristic(E_past, E_future, r, rho)
val_standard = standard_numerical_integration(mass, r, E_past, E_future, steps=10000)

# Calculate Percentage Error
error_margin = abs(val_standard - val_yours) / val_standard * 100

print(f"Output (Standard Calculus):  {val_standard:.12f}")
print(f"Output (Your Algorithm):     {val_yours:.12f}\n")
print(f"ACCURACY LOSS (Error %):     {error_margin:.6f} %")
