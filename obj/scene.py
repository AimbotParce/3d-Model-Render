import numpy as np
from bin.lightClass import Light
from bin.objectClass import Object
from bin.planeClass import Plane


class Scene:
    def __init__(self, backgroundColor: tuple = (0, 0, 0), objects: list[Object] = [], lights: list[Light] = []):
        self.objects = objects
        self.lights = lights
        self.backgroundColor = backgroundColor

    def set_background_color(self, color: tuple):
        self.backgroundColor = color

    def project(self, pt):
        """Get the distance from point to scene."""
        distsNplanes = [obj.project(pt) for obj in self.objects]
        dists = [distsNplanes[i][0] for i in range(len(distsNplanes))]

        minIdx = np.argmin(dists)
        return dists[minIdx], self.objects[minIdx], distsNplanes[minIdx][1]

    def add_object(self, obj: Object):
        self.objects.append(obj)

    def add_light(self, light: Light):
        self.lights.append(light)

    def get_color(self, pt, obj: Object, plane: Plane):
        """Get the color of the object at point pt."""
        # Compute the total light at point pt:
        totalLight = np.array([0.0, 0.0, 0.0])
        for light in self.lights:
            lightIntensity = light.get_intensity(pt, plane)
            if lightIntensity > 0:
                totalLight += lightIntensity * light.color / 255

        totalLight = np.clip(totalLight, 0, 1)
        # Compute the color of the object at point pt:
        return plane.color * totalLight

    def get_objects(self):
        return self.objects
