import numpy as np
from bin.objectClass import Object

from obj.scene import Scene


class Camera(Object):
    def __init__(self, name, origin, rotation, resolution, sensor, focal, depth, scene: Scene):
        self.name = name
        self.origin = origin
        self.rotation = rotation
        self.focal = focal
        self.resolution = resolution
        self.scene = scene
        self.depth = depth
        self.sensor = sensor

        super().__init__(name, (0, 0, 0), origin, rotation, [1, 1, 1])

    def get_vertices(self):
        """I'll use vertices to get the local vectors of the camera."""
        # Camera will be facing in the positive x direction
        return np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def apply_transformation(self, translation, rotation, scale):
        super().apply_transformation(translation, rotation, scale)
        self.vx = self.points[1] - self.points[0]
        self.vy = self.points[2] - self.points[0]
        self.vz = self.points[3] - self.points[0]

    def get_planes(self):
        """I don't need planes for the camera."""
        return []

    def __get_ray_direction(self, x, y):
        """Get the ray from the camera origin to the pixel (x, y)."""
        vector = (
            self.vx * self.focal
            - self.vy * (x / self.resolution[1]) * self.sensor[1]
            + self.vz * (y / self.resolution[0]) * self.sensor[0]
        )
        return vector / np.linalg.norm(vector)

    def __cast_ray(self, x, y):
        """Cast a ray from the camera origin to the pixel (x, y)."""
        rayDirection = self.__get_ray_direction(x, y)
        rayOrigin = self.origin

        totalDistance = 0
        dist, obj, plane = self.scene.project(rayOrigin)
        while dist > 0.001:
            totalDistance += dist
            rayOrigin += rayDirection * dist
            dist, obj, plane = self.scene.project(rayOrigin)
            if totalDistance > self.depth:
                return None, None, None

        # print(rayOrigin, dist)
        return rayOrigin, obj, plane

    def __cast_ray_color(self, x, y):
        pt, obj, plane = self.__cast_ray(x, y)
        if obj is None:
            return self.scene.backgroundColor
        return self.scene.get_color(pt, obj, plane)

    def get_image(self):
        """Get the image of the objects from the camera."""

        return np.array(
            [
                [
                    self.__cast_ray_color(x - self.resolution[1] / 2, self.resolution[0] / 2 - y)
                    for x in range(self.resolution[1])
                ]
                for y in range(self.resolution[0])
            ],
            dtype=np.uint8,
        )
