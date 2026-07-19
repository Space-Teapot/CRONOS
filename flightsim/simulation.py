"""Flight simulation engine for 3-DoF rocket trajectory analysis."""

import numpy as np
import matplotlib.pyplot as plt
import ambiance
from scipy.integrate import odeint
from rocketdesign.rocket import Rocket

# Module docstring
__all__ = ["FlightSimulator"]


class FlightSimulator:
    """3-Degree-of-Freedom rocket flight simulator.
    
    Simulates rocket flight including:
    - Vertical acceleration (altitude, velocity)
    - Lateral motion
    - Attitude/rotation
    """
    
    def __init__(self, rocket: Rocket, initial_conditions: np.ndarray, time_span: np.ndarray):
        """Initialize the flight simulator."""
        self.rocket = rocket
        self.initial_conditions = initial_conditions
        self.time_span = time_span
    
    def run(self):
        """Run the flight simulation."""
        # Integrate the equations of motion using odeint
        solution, info = odeint(self.equations_of_motion, self.initial_conditions, self.time_span, full_output=True, mxstep=5000)
        return solution, info
    
    def equations_of_motion(self, state, t):
        """Define the equations of motion for the rocket."""
        # Unpack state variables
        x, y, vx, vy, theta = state
        theta = theta % (2 * np.pi)  # Normalize angle to [0, 2*pi]
        gamma = np.arctan2(vy, vx)  # Flight path angle
        
        # Compute forces and moments (placeholder)
        # In a real implementation, you would calculate aerodynamic forces,
        # thrust, gravity, etc., based on the rocket's properties and state.
        
        # Calculate dynamic pressure and aerodynamic forces
        q = 0.5 * self.atmospheric_conditions(y)[2][0] * (vx**2 + vy**2)  # Dynamic pressure
        
        # Linear dynamics given mass, rotation, and aerodynamic coefficients
        g = 9.81  # Gravity [m/s^2]
        Cd = self.rocket.Cd[0]  # Placeholder: use the first element of Cd for simplicity
        ax = -q * Cd * np.cos(gamma) / self.rocket.mass
        ay = -g - q * Cd * np.sin(gamma) / self.rocket.mass
        
        # Rotational dynamics given moment of inertia and aerodynamic moment coefficients
        Cm = self.rocket.Cm[0] # Placeholder: use the first element of Cm for simplicity
        MOI = self.rocket.MOI
        M = Cm * q * self.rocket.sref * self.rocket.lref
        dtheta_dt = M / MOI[1, 1]  # Rotation about the y-axis (pitch)

        return np.array([vx, vy, ax, ay, dtheta_dt])
    
    def atmospheric_conditions(self, altitude):
        """Get atmospheric conditions at a given altitude using the ambiance library."""
        atmosphere = ambiance.Atmosphere(altitude)
        return atmosphere.temperature, atmosphere.pressure, atmosphere.density