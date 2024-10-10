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
        self.camera_matrix = self.__compute_camera_matrix()

    def get_planes(self):
        """I don't need planes for the camera."""
        return []

    def __compute_camera_matrix(self):
        """Compute the camera matrix."""
        ku = self.resolution[1] / self.sensor[1]
        kv = self.resolution[0] / self.sensor[0]
        C = np.array(
            [[self.focal * kv, 0, self.resolution[0] / 2], [0, -self.focal * ku, self.resolution[1] / 2], [0, 0, 1]]
        )
        R = self.rotation_matrix
        RT = np.zeros((4, 4))
        RT[:3, :3] = R
        RT[:3, 3] = self.origin
        RT[3, 3] = 1

        middle = np.zeros((3, 4))
        middle[:3, :3] = np.eye(3)

        return C @ middle @ RT

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

    def get_image_raycasting(self):
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

    def get_image(self):
        """Get the image of the objects from the camera."""
        img = np.zeros((self.resolution[0], self.resolution[1], 3), dtype=np.uint8)
        relativePts = np.concatenate([obj.get_points() for obj in self.scene.objects]) - self.origin
        points = np.ones((len(relativePts), 4))
        points[:, :3] = relativePts

        projections = (points @ self.camera_matrix.T).astype(int)[:, :2]
        print(projections)

        indx = np.logical_and(
            np.logical_and((projections[:, 0] >= 0), (projections[:, 0] < self.resolution[1])),
            np.logical_and((projections[:, 1] >= 0), (projections[:, 1] < self.resolution[0])),
        )

        projections = projections[indx]
        print(projections)

        img[projections + (np.array(self.resolution) / 2).astype(int)] = (255, 255, 255)

        return img
