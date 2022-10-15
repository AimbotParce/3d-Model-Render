import numpy as np
from bin.objectClass import Object
from bin.planeClass import Plane


class Square(Object):
    def __init__(self, name, color, origin, rotation, scale, infinite=False):
        """Create a square plane object. Not to be confused with the basic triangular plane, this is a renderable object."""
        self.infinite = infinite
        super().__init__(name, color, origin, rotation, scale)

    def get_vertices(self):
        return np.array(
            [
                [-1 / 2, -1 / 2, 0],
                [1 / 2, -1 / 2, 0],
                [1 / 2, 1 / 2, 0],
                [-1 / 2, 1 / 2, 0],
            ]
        )

    def get_planes(self):
        if self.infinite:
            return [Plane(self.points[0], self.points[1], self.points[2], infinite=True)]
        return [
            Plane(self.points[0], self.points[1], self.points[2]),
            Plane(self.points[1], self.points[3], self.points[2]),
        ]
