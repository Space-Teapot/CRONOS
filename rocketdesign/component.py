"""Component class and related utilities for closedrocket."""

import numpy as np

# Module docstring
__all__ = ["Component"]


class Component:
    """Component class representing a component's physical properties and state.

    Attributes:
        dimensions (tuple): The dimensions of the component.
        volume (float): The volume of the component [m³].
        mass (float): The mass of the component [kg].
        MOI (np.ndarray): The moment of inertia tensor of the component [kg*m²].
    """
    
    def __init__(self, dimensions: tuple, density: float, shape: str = "cyl"):
        """Initialize a Component instance with given physical properties."""
        if shape == "cyl":
            self.dimensions = dimensions  # (length, diameter)
            self.volume = np.pi * (dimensions[1] / 2) ** 2 * dimensions[0]
            self.mass = self.volume * density
            self.MOI = np.zeros((3, 3))
            self.MOI[0, 0] = (1 / 2) * self.mass * (dimensions[1] / 2) ** 2  # Ixx = (1/2) * m * r^2
            self.MOI[1, 1] = (1 / 12) * self.mass * (3 * (dimensions[1] / 2) ** 2 + dimensions[0] ** 2)
            self.MOI[2, 2] = self.MOI[1, 1]  # Izz = Iyy = (1/12) * m * (3*r^2 + h^2)
        elif shape == "rect":
            self.dimensions = dimensions  # (length, width, height)
            self.volume = dimensions[0] * dimensions[1] * dimensions[2]
            self.mass = self.volume * density
            self.MOI = np.zeros((3, 3))
            self.MOI[0, 0] = (1 / 12) * self.mass * (dimensions[1] ** 2 + dimensions[2] ** 2)  # Ixx = (1/12) * m * (w^2 + h^2)
            self.MOI[1, 1] = (1 / 12) * self.mass * (dimensions[0] ** 2 + dimensions[2] ** 2)  # Iyy = (1/12) * m * (l^2 + h^2)
            self.MOI[2, 2] = (1 / 12) * self.mass * (dimensions[0] ** 2 + dimensions[1] ** 2)  # Izz = (1/12) * m * (l^2 + w^2)
        elif shape == "hcyl":
            self.dimensions = dimensions  # (length, outer_diameter, inner_diameter)
            self.volume = np.pi * (dimensions[1] ** 2 - dimensions[2] ** 2) / 4 * dimensions[0]
            self.mass = self.volume * density
            self.MOI = np.zeros((3, 3))
            self.MOI[0, 0] = (1 / 2) * self.mass * ((dimensions[1] / 2) ** 2 + (dimensions[2] / 2) ** 2)  # Ixx = (1/2) * m * (r_outer^2 + r_inner^2)
            self.MOI[1, 1] = (1 / 12) * self.mass * (3 * ((dimensions[1] / 2) ** 2 + (dimensions[2] / 2) ** 2) + dimensions[0] ** 2)
            self.MOI[2, 2] = self.MOI[1, 1]  # Izz = Iyy = (1/12) * m * (3*(r_outer^2 + r_inner^2) + h^2)