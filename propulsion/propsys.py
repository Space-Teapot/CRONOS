"""Engine and tank class and related utilities for CRONOS."""

import numpy as np
from scipy.optimize import fsolve
from rocketdesign.component import Component

# Module docstring
__all__ = ["Engine", "Tank"]


class Engine(Component):
    """Engine class representing an engine's physical properties and state.

    Attributes:
        _dimensions (tuple): Dimensions of the engine (length, diameter) [m]
        _mass (float): Mass of the engine [kg]
        _MOI (np.ndarray): Moment of inertia tensor of the engine [kg*m^2]
        _At (float): Throat area of the nozzle [m^2]
        _Ae (float): Exit area of the nozzle [m^2]
        _Tc (float): Chamber combustion temperature [K]
        _gamma (float): Specific heat ratio of the exhaust gases
        _R (float): Specific gas constant for the exhaust gases [J/(kg*K)]
    """
    
    def __init__(self, dimensions: tuple, dry_density: float, At: float = 0.0, Ae: float = 0.0, Tc: float = 0.0, gamma: float = 1.4, R: float = 287.0):
        """Initialize an Engine instance with given physical properties."""
        Component.__init__(self, dimensions, dry_density, shape="cyl")
        self._At = At
        self._Ae = Ae
        self._Tc = Tc
        self._gamma = gamma
        self._R = R
        
    def get_thrust_isp(self, Pc: float, Pa: float) -> tuple:
        """Calculate the thrust and specific impulse produced by the engine at a given time.

        Args:
            Pc (float): Chamber pressure [Pa]
            Pa (float): Ambient pressure [Pa]

        Returns:
            tuple: Thrust produced by the engine [N] and specific impulse [s]
        """

        # Calculate flow properties at exit from isentropic flow relations
        Me = self.area_mach(self._Ae / self._At, supersonic=True)
        Pe = Pc * (1 + (self._gamma - 1) / 2 * Me ** 2) ** (-self._gamma / (self._gamma - 1))
        Te = self._Tc * (1 + (self._gamma - 1) / 2 * Me ** 2) ** -1
        Ve = Me * np.sqrt(self._gamma * self._R * Te)
        mdot = Pe * self._Ae * Ve / (self._R * Te)
        
        # Calculate thrust and specific impulse
        thrust = mdot * Ve + (Pe - Pa) * self._Ae
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
            return (1 / M) * ((2 / (self._gamma + 1)) * (1 + (self._gamma - 1) / 2 * M ** 2)) ** ((self._gamma + 1) / (2 * (self._gamma - 1))) - A_Astar
        M = fsolve(func, 1.0 + 0.1 if supersonic else 0.5)[0]
        return M
    
class Tank(Component):
    """Tank class representing a propellant tank's physical properties and state.

    Attributes:
        _dimensions (tuple): Dimensions of the tank (length, diameter) [m]
        _mass (float): Mass of the tank [kg]
        _MOI (np.ndarray): Moment of inertia tensor of the tank [kg*m^2]
        _prop_mass (float): Initial mass of the propellant in the tank [kg]
        _prop_temp (float): Initial temperature of the propellant in the tank [K]
    """
    
    def __init__(self, dimensions: tuple, shell_density: float, propellant, prop_mass: float, prop_temp: float):
        """Initialize a Tank instance with given physical properties."""
        Component.__init__(self, dimensions, shell_density, "cyl")
        self._prop_mass = prop_mass  # kg
        self._prop_temp = prop_temp  # K

        # PLACEHOLDER propellant data, will interpolate from tabulated data or something
        if propellant == "N2O":
            self.rho0 = self._prop_mass / self._volume  # kg/m^3
            self._R = 287  # J/(kg*K)
            self._gamma = 1.4
            self._P0 = self.rho0 * self._R * self._prop_temp  # Pa
        elif propellant == "ethanol":
            self.rho0 = self._prop_mass / self._volume  # kg/m^3
            self._R = 287  # J/(kg*K)
            self._gamma = 1.4
            self._P0 = self.rho0 * self._R * self._prop_temp  # Pa
        else:
            raise ValueError("Unsupported propellant type. Supported types: 'N2O', 'ethanol'.")
    
    def get_pressure(self) -> float:
        """Calculate the current pressure in the tank based on propellant mass and temperature.

        Returns:
            float: Current pressure in the tank [Pa]
        """
        # Placeholder for actual pressure calculation based on propellant properties
        return self._P0  # Return initial pressure as a placeholder