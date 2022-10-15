import numpy as np
from bin.objectClass import Object


class Scene:
    def __init__(self, objects: list[Object], backgroundColor: tuple):
        self.objects = objects
        self.backgroundColor = backgroundColor

    def set_background_color(self, color: tuple):
        self.backgroundColor = color

    def project(self, pt):
        """Get the distance from point to scene."""
        dists = [obj.project(pt) for obj in self.objects]

        minIdx = np.argmin(dists)
        return dists[minIdx], self.objects[minIdx]

    def add_object(self, obj: Object):
        self.objects.append(obj)

    def get_objects(self):
        return self.objects
