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
    
    Attributes:
        _rocket (Rocket): The rocket object to be simulated
        _initial_conditions (np.ndarray): Initial state vector [x, y, vx, vy, theta]
        _time_span (np.ndarray): Time span for the simulation [t0, tf]
    """
    
    def __init__(self, rocket: Rocket, initial_conditions: np.ndarray, time_span: np.ndarray):
        """Initialize the flight simulator."""
        self._rocket = rocket
        self._initial_conditions = initial_conditions
        self._time_span = time_span
    
    def run(self):
        """Run the flight simulation."""
        # Integrate the equations of motion using odeint
        solution, info = odeint(self.equations_of_motion, self._initial_conditions, self._time_span, full_output=True, mxstep=5000)
        return solution, info
    
    def equations_of_motion(self, state, t):
        """Define the equations of motion for the rocket."""
        # Unpack state variables
        x, y, vx, vy, theta = state
        theta = theta % (2 * np.pi)  # Normalize angle to [0, 2*pi]
        gamma = np.arctan2(vy, vx)  # Flight path angle
        
        # Get aerodynamic coefficients and mass properties from the rocket
        Cd, Cm = self._rocket.get_aero_model()  # Placeholder: use the first element of Cd for simplicity
        mass = self._rocket.get_mass()
        MOI = self._rocket.get_MOI()
        
        # Calculate dynamic pressure and aerodynamic forces
        q = 0.5 * self.atmospheric_conditions(y)[2][0] * (vx**2 + vy**2)
        
        # Linear dynamics given mass, rotation, and aerodynamic coefficients
        g = 9.81  # Gravity [m/s^2]
        ax = -q * Cd * np.cos(gamma) / mass
        ay = -g - q * Cd * np.sin(gamma) / mass
        
        # Rotational dynamics given moment of inertia and aerodynamic moment coefficients
        M = Cm * q * self._rocket.get_reference_area() * self._rocket.get_reference_length()
        dtheta_dt = M / MOI[1, 1]  # Rotation about the y-axis (pitch)

        return np.array([vx, vy, ax, ay, dtheta_dt])
    
    def atmospheric_conditions(self, altitude):
        """Get atmospheric conditions at a given altitude using the ambiance library."""
        atmosphere = ambiance.Atmosphere(altitude)
        return atmosphere.temperature, atmosphere.pressure, atmosphere.density