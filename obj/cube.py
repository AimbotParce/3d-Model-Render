import numpy as np
from bin.objectClass import Object
from bin.planeClass import Plane


class Cube(Object):
    def __init__(self, name, color: np.ndarray, origin: np.ndarray, rotation: np.ndarray, scale: np.ndarray):
        """Create a cube object. The cube is centered at the origin. sideLength is the length of the cube's sides.
        Rotation is a list of the euler angles (in deg). Scale is a list of the scale factors in each direction."""
        super().__init__(name, color, origin, rotation, scale)

    def get_vertices(self):
        return np.array(
            [
                [-1 / 2, -1 / 2, 1 / 2],  # Front right top
                [1 / 2, -1 / 2, 1 / 2],  # Back right top
                [1 / 2, 1 / 2, 1 / 2],  # Back left top
                [-1 / 2, 1 / 2, 1 / 2],  # Front left top
                [-1 / 2, 1 / 2, -1 / 2],  # Front left bottom
                [1 / 2, 1 / 2, -1 / 2],  # Back left bottom
                [1 / 2, -1 / 2, -1 / 2],  # Back right bottom
                [-1 / 2, -1 / 2, -1 / 2],  # Front right bottom
            ]
        )

    def get_planes(self):
        return [
            Plane(self.points[0], self.points[1], self.points[2]),  # Top
            Plane(self.points[2], self.points[3], self.points[0]),  # Top
            Plane(self.points[1], self.points[6], self.points[5]),  # Back
            Plane(self.points[5], self.points[2], self.points[1]),  # Back
            Plane(self.points[6], self.points[7], self.points[4]),  # Bottom
            Plane(self.points[4], self.points[5], self.points[6]),  # Bottom
            Plane(self.points[7], self.points[0], self.points[3]),  # Front
            Plane(self.points[3], self.points[4], self.points[7]),  # Front
            Plane(self.points[6], self.points[1], self.points[0]),  # Right
            Plane(self.points[0], self.points[7], self.points[6]),  # Right
            Plane(self.points[2], self.points[5], self.points[4]),  # Left
            Plane(self.points[4], self.points[3], self.points[2]),  # Left
        ]
