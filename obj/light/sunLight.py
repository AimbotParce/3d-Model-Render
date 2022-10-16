import numpy as np
from bin.lightClass import Light
from bin.planeClass import Plane


class Sun(Light):
    def __init__(self, name, color: np.ndarray, rotation: np.ndarray, brightness: float):
        """Create a puntual light object. The light is centered at the origin.
        Brightness is the intensity of the light at the origin."""
        self.brightness = brightness
        super().__init__(name, color, (0, 0, 0), rotation, [1, 1, 1])

    def get_vertices(self):
        return np.array([[0, 0, 0], [0, 0, -1]])

    def get_planes(self):
        return []

    def apply_transformation(self, translation, rotation, scale):
        super().apply_transformation(translation, rotation, scale)
        self.direction = self.points[1] - self.points[0]
        self.direction /= np.linalg.norm(self.direction)

    def get_intensity(self, pt, plane: Plane):
        """Get the intensity of the light at point pt."""

        # Compute the light intensity:
        return np.dot(plane.normal, -self.direction) * self.brightness
