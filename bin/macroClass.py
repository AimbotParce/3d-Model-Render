from typing import List

import numpy as np

from bin.objectClass import Object


# This was implemented badly, so I should look deeper into it.
class Macro(Object):
    def __init__(self, name, objects: List[Object], origin, rotation, scale):
        self.name = name
        self.objects = objects
        super().__init__(name, (0, 0, 0), origin, rotation, scale)
        self.apply_object_transformation()

    def get_vertices(self):
        return np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def get_planes(self):
        return []

    def apply_object_transformation(self):
        for obj in self.objects:
            obj.apply_transformation(
                np.array(self.origin) + obj.origin,
                np.array(self.rotation) + obj.rotation,
                np.array(self.scale) * obj.scale,
            )

    def project(self, pt):
        distsNplanes = np.array([obj.project(pt) for obj in self.objects])
        minIdx = np.argmin(distsNplanes[:, 0])
        return distsNplanes[minIdx]

    def get_points(self):
        return np.concatenate([obj.get_points() for obj in self.objects])
