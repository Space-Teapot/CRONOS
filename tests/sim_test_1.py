import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ensure project root is on sys.path so rocket.py and simulation.py can be imported.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from rocketdesign.rocket import Rocket
from flightsim.simulation import FlightSimulator

rocket = Rocket("tests/test_rocket.yaml")
time_span = np.linspace(0, 100, 100)  # Simulate for 100 seconds
sim = FlightSimulator(rocket, initial_conditions=np.array([0, 0, 10, 8000, 0]), time_span=time_span)

solution, info = sim.run()
print("Final state after 100-second simulation:")
print("Position (x, y):", solution[-1, 0], solution[-1, 1])
print("Velocity (vx, vy):", solution[-1, 2], solution[-1, 3])
print("Angle (theta):", solution[-1, 4])

# Plotting: Y vs X and Y vs Time

# Assume state vector columns: [x, y, vx, vy, theta]
x = solution[:, 0]
y = solution[:, 1]

plt.figure()
plt.plot(x, y, '-o')
plt.xlabel('X position')
plt.ylabel('Y position')
plt.title('Trajectory: Y vs X')

plt.figure()
plt.plot(time_span, y, '-o')
plt.xlabel('Time')
plt.ylabel('Y position')
plt.title('Y position vs Time')

plt.show()
