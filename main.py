import math
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------- Constants ----------
g = 9.81  # Acceleration due to gravity (m/s^2)

# ---------- Functions ----------
def simulate_motion():
    """Simulate and visualize the projectile motion in real-time with and without air resistance."""
    # Clear any previous plot
    ax.clear()
    ax.set_title("Projectile Motion Simulation")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")

    try:
        # Get user inputs
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
    v0x, v0y = v0 * math.cos(angle), v0 * math.sin(angle)
    dt = 0.02  # Small time step for smooth animation

    # Initialize lists for storing trajectory data
    x_ideal, y_ideal, x_real, y_real = [0], [0], [0], [0]
    vx, vy = v0x, v0y  # Initial velocities for real motion

    while y_real[-1] >= 0 or y_ideal[-1] >= 0:
        # Update ideal motion (no air resistance)
        if y_ideal[-1] >= 0:
            x_ideal.append(x_ideal[-1] + v0x * dt)
            y_ideal.append(y_ideal[-1] + v0y * dt - 0.5 * g * dt**2)
            v0y -= g * dt

        # Update real motion (with air resistance)
        if y_real[-1] >= 0:
            ax_drag = -drag_coeff * vx / mass
            ay_drag = -g - (drag_coeff * vy / mass)
            vx += ax_drag * dt
            vy += ay_drag * dt
            x_real.append(x_real[-1] + vx * dt)
            y_real.append(y_real[-1] + vy * dt)

        # Plot real-time update
        ax.plot(x_ideal, y_ideal, color="blue", label="No Air Resistance" if len(x_ideal) == 2 else "")
        ax.plot(x_real, y_real, color="orange", label="With Air Resistance" if len(x_real) == 2 else "")
        ax.legend()
        canvas.draw()
        root.update_idletasks()

        # Stop updating if both trajectories hit the ground
        if y_ideal[-1] < 0 and y_real[-1] < 0:
            break

def reset_fields():
    """Clear all input fields."""
    entry_velocity.delete(0, tk.END)
    entry_angle.delete(0, tk.END)
    entry_mass.delete(0, tk.END)
    entry_drag.delete(0, tk.END)
    ax.clear()
    ax.set_title("Projectile Motion Simulation")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    canvas.draw()

def open_theory():
    """Open theory page in the web browser."""
    import webbrowser
    webbrowser.open("https://farside.ph.utexas.edu/teaching/336k/Newton/node29.html")

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Projectile Motion Simulator with Real-Time Visualization")
root.geometry("800x600")
root.config(bg="black")

# Title Label
title_label = tk.Label(
    root, text="Projectile Motion Simulator", font=("Arial", 20, "bold"), bg="black", fg="orange"
)
title_label.pack(pady=10)

# Input Frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Input Fields
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

# Graph Setup in tkinter window
fig = Figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.set_title("Projectile Motion Simulation")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Height (m)")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Footer Label
footer_label = tk.Label(
    root, text="Physics + Code = 🚀", font=("Arial", 10, "italic"), bg="black", fg="orange"
)
footer_label.pack(pady=10)

# Run the GUI
root.mainloop()
