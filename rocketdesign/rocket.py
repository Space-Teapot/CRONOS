"""Rocket class and related utilities for closedrocket."""

import numpy as np
import yaml
from rocketdesign.component import Component
from propulsion.propsys import Engine, Tank

# Module docstring
__all__ = ["Rocket"]


class Rocket:
    """Rocket class representing a rocket's physical properties and state.
    
    Attributes:
        name (str): Name of the rocket
        components (np.ndarray): Array of components (engines, tanks, etc.) that make up the rocket
    """
    
    def __init__(self, filename: str):
        """Initialize a Rocket instance with given physical properties."""
        self._components = np.array([])  # Initialize an empty array for components
        
        # Load rocket properties from YAML file
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
            for component in data.get('components', []):
                self.add_component(component)  # Add each component to the rocket
        
    def add_component(self, component):
        """Add a component to the rocket."""
        if not isinstance(component, dict) or len(component) != 1:
            raise ValueError("component must be a dictionary with exactly one key")

        component_type, properties = next(iter(component.items()))

        if component_type == "Engine":
            obj = Engine(**properties)
        elif component_type == "Tank":
            obj = Tank(**properties)
        elif component_type == "Component":
            obj = Component(**properties)
        else:
            raise ValueError(f"Unsupported component type: {component_type}")

        self._components = np.append(self._components, obj)
    
    def print(self):
        """Print a string representation of the Rocket instance."""
        print(f"Rocket with {len(self._components)} components: {self._components}")
        
    def get_aero_model(self):
        """Get the aerodynamic model of the rocket."""
        # Placeholder for actual aerodynamic model retrieval
        Cd = 0.5  # Placeholder drag coefficient
        Cm = 0    # Placeholder moment coefficient
        return Cd, Cm
    
    def get_mass(self):
        """Get the total mass of the rocket."""
        total_mass = sum(component._mass for component in self._components)
        return total_mass
    
    def get_MOI(self):
        """Get the total moment of inertia of the rocket."""
        # Placeholder, need to use parallel axis theorem to combine MOIs of components
        total_MOI = sum(component._MOI for component in self._components)
        return total_MOI
    
    def get_reference_area(self):
        """Get the reference area of the rocket."""
        # Placeholder for actual reference area calculation
        return 1.0  # Placeholder reference area in m^2
    
    def get_reference_length(self):
        """Get the reference length of the rocket."""
        # Placeholder for actual reference length calculation
        return 1.0  # Placeholder reference length in m