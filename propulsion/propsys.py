"""Engine and tank class and related utilities for CRONOS."""

import numpy as np
from scipy.optimize import fsolve
from rocketdesign.component import Component

# Module docstring
__all__ = ["Engine", "Tank"]


class Engine(Component):
    """Engine class representing an engine's physical properties and state.

    Attributes:
        size (tuple): Dimensions of the engine (length, diameter) [m]
        mass (float): Mass of the engine [kg]
        MOI (np.ndarray): Moment of inertia tensor of the engine [kg*m^2]
        At (float): Throat area of the nozzle [m^2]
        Ae (float): Exit area of the nozzle [m^2]
        Tc (float): Chamber temperature [K]
        gamma (float): Specific heat ratio of the exhaust gases
        R (float): Specific gas constant for the exhaust gases [J/(kg*K)]
    """
    
    def __init__(self, dimensions: tuple, density: float, At: float = 0.0, Ae: float = 0.0, Tc: float = 0.0, gamma: float = 1.4, R: float = 287.0):
        """Initialize an Engine instance with given physical properties."""
        Component.__init__(self, dimensions, density, shape="cylinder")
        self.At = At
        self.Ae = Ae
        self.Tc = Tc
        self.gamma = gamma
        self.R = R
        
    def get_thrust_isp(self, Pc: float, Pa: float) -> tuple:
        """Calculate the thrust and specific impulse produced by the engine at a given time.

        Args:
            Pc (float): Chamber pressure [Pa]
            Pa (float): Ambient pressure [Pa]

        Returns:
            tuple: Thrust produced by the engine [N] and specific impulse [s]
        """

        # Calculate Mach number, pressure, temperature, velocity, and mass flow rate at exit from isentropic flow relations
        Me = self.area_mach(self.Ae / self.At, supersonic=True)
        Pe = Pc * (1 + (self.gamma - 1) / 2 * Me ** 2) ** (-self.gamma / (self.gamma - 1))
        Te = self.Tc * (1 + (self.gamma - 1) / 2 * Me ** 2) ** -1
        Ve = Me * np.sqrt(self.gamma * self.R * Te)
        mdot = Pe * self.Ae * Ve / (self.R * Te)
        
        # Calculate thrust and specific impulse
        thrust = mdot * Ve + (Pa - Pe) * self.Ae
        isp = thrust / (mdot * 9.80665)  # Convert to specific impulse in seconds
        
        return thrust, isp

    def area_mach(self, A_Astar: float, supersonic: bool = True) -> float:
        """Calculate the Mach number for a sonic area ratio using isentropic flow relations.

        Args:
            A_Astar (float): Area ratio A/A* where A* is sonic-condition area
            supersonic (bool): Whether to return the supersonic solution

        Returns:
            float: Mach number
        """
        def func(M):
            return (1 / M) * ((2 / (self.gamma + 1)) * (1 + (self.gamma - 1) / 2 * M ** 2)) ** ((self.gamma + 1) / (2 * (self.gamma - 1))) - A_Astar
        M = fsolve(func, 1.0 + 0.1 if supersonic else 0.5)[0]
        return M[0]
    
class Tank(Component):
    """Tank class representing a propellant tank's physical properties and state.

    Attributes:
        size (tuple): Dimensions of the tank (length, diameter) [m]
        mass (float): Mass of the tank [kg]
        MOI (np.ndarray): Moment of inertia tensor of the tank [kg*m^2]
    """
    
    def __init__(self, dimensions: tuple, density):
        """Initialize a Tank instance with given physical properties."""
        Component.__init__(self, dimensions, density, shape="cylinder")