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
        self.components = np.array([])  # Initialize an empty array for components
        
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

        self.components = np.append(self.components, obj)
    
    def print(self):
        """Print a string representation of the Rocket instance."""
        print(f"Rocket with {len(self.components)} components: {self.components}")
        