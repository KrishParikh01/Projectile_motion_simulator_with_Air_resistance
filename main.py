import math
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
import webbrowser

# ---------- Constants ----------
g = 9.81  # Acceleration due to gravity (m/s^2)

# ---------- Functions ----------
def simulate_motion():
    """Simulate the projectile motion with and without air resistance."""
    try:
        v0 = float(entry_velocity.get())
        angle = math.radians(float(entry_angle.get()))
        mass = float(entry_mass.get())
        drag_coeff = float(entry_drag.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values.")
        return

    if v0 <= 0 or mass <= 0:
        messagebox.showwarning("Invalid Input", "Velocity and mass must be positive.")
        return

    # Calculate initial velocity components
    v0x = v0 * math.cos(angle)
    v0y = v0 * math.sin(angle)

    # Generate time array for ideal motion
    t_max = (2 * v0y / g) * 1.2  # Extend slightly beyond theoretical flight time
    t = np.linspace(0, t_max, 500)

    # Simulate ideal motion (no air resistance)
    x_ideal = v0x * t
    y_ideal = v0y * t - 0.5 * g * t**2

    # Calculate max height and range for ideal motion
    max_height_ideal = (v0y**2) / (2 * g)
    range_ideal = (v0**2) * math.sin(2 * angle) / g

    # Simulate real motion (with air resistance) using small time steps
    dt = t[1] - t[0]
    x_real, y_real = [0], [0]
    vx, vy = v0x, v0y  # Initialize velocity components
    while y_real[-1] >= 0:
        ax = -drag_coeff * vx / mass  # Acceleration due to air resistance (x)
        ay = -g - (drag_coeff * vy / mass)  # Acceleration due to gravity + drag (y)

        # Update velocities
        vx += ax * dt
        vy += ay * dt

        # Update positions
        x_real.append(x_real[-1] + vx * dt)
        y_real.append(y_real[-1] + vy * dt)

    # Calculate max height and range for real motion
    max_height_real = max(y_real)
    range_real = x_real[-1]

    # Plotting the trajectories
    plt.figure(figsize=(10, 6))
    plt.plot(x_ideal, y_ideal, label="No Air Resistance", linestyle="--", color="blue")
    plt.plot(x_real, y_real, label="With Air Resistance", color="orange")

    # Display calculated values on plot
    plt.text(range_ideal * 0.5, max_height_ideal, f"Max Height (Ideal): {max_height_ideal:.2f} m\nRange (Ideal): {range_ideal:.2f} m",
             color="blue", ha="center")
    plt.text(range_real * 0.5, max_height_real, f"Max Height (Real): {max_height_real:.2f} m\nRange (Real): {range_real:.2f} m",
             color="orange", ha="center")

    plt.title("Projectile Motion Simulation")
    plt.xlabel("Distance (m)")
    plt.ylabel("Height (m)")
    plt.legend()
    plt.grid(True)
    plt.show()

def reset_fields():
    """Clear all input fields."""
    entry_velocity.delete(0, tk.END)
    entry_angle.delete(0, tk.END)
    entry_mass.delete(0, tk.END)
    entry_drag.delete(0, tk.END)

def open_theory():
    """Open theory page in the web browser."""
    webbrowser.open("https://farside.ph.utexas.edu/teaching/336k/Newton/node29.html")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Projectile Motion Simulator")
root.geometry("600x400")
root.config(bg="black")

# Title Label
title_label = tk.Label(
    root, text="Projectile Motion Simulator", font=("Arial", 20, "bold"), bg="black", fg="orange"
)
title_label.pack(pady=10)

# Input Frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Initial Velocity (m/s):").grid(row=0, column=0, padx=5, pady=5)
entry_velocity = ttk.Entry(input_frame)
entry_velocity.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Launch Angle (degrees):").grid(row=1, column=0, padx=5, pady=5)
entry_angle = ttk.Entry(input_frame)
entry_angle.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Mass (kg):").grid(row=2, column=0, padx=5, pady=5)
entry_mass = ttk.Entry(input_frame)
entry_mass.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Drag Coefficient (kg/s):").grid(row=3, column=0, padx=5, pady=5)
entry_drag = ttk.Entry(input_frame)
entry_drag.grid(row=3, column=1, padx=5, pady=5)

# Button Frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

simulate_button = ttk.Button(button_frame, text="Simulate", command=simulate_motion)
simulate_button.grid(row=0, column=0, padx=10)

reset_button = ttk.Button(button_frame, text="Reset", command=reset_fields)
reset_button.grid(row=0, column=1, padx=10)

exit_button = ttk.Button(button_frame, text="Exit", command=root.destroy)
exit_button.grid(row=0, column=2, padx=10)

# Theory Button
theory_button = ttk.Button(button_frame, text="Theory", command=open_theory)
theory_button.grid(row=0, column=3, padx=10)

# Footer Label
footer_label = tk.Label(
    root, text="Physics + Code = 🚀", font=("Arial", 10, "italic"), bg="black", fg="orange"
)
footer_label.pack(pady=10)

# Run the GUI
root.mainloop()
