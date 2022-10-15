import numpy as np
from bin.lightClass import Light
from bin.planeClass import Plane


class PointLight(Light):
    def __init__(self, name, color: np.ndarray, origin: np.ndarray, brightness: float):
        """Create a puntual light object. The light is centered at the origin.
        Brightness is the intensity of the light at the origin."""
        self.brightness = brightness
        super().__init__(name, color, origin, [0, 0, 0], [1, 1, 1])

    def get_vertices(self):
        return np.array([[0, 0, 0]])

    def get_planes(self):
        return []

    def get_intensity(self, pt, plane: Plane):
        """Get the intensity of the light at point pt."""

        # Compute the light vector:
        lightVector = self.origin - pt
        distance = np.linalg.norm(lightVector)
        lightVector /= distance
        # Compute the light intensity:
        return np.abs(np.dot(plane.normal, lightVector) * self.brightness / (distance**2))
