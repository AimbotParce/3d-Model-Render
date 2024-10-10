import numpy as np


class Object:
    def __init__(self, name, color, origin=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        """Create an object. It will be centered at origin.
        Rotation is a list of the euler angles (in deg).
        Scale is a list of the scale factors in each direction."""
        self.name = name
        self.rotation = rotation
        self.scale = scale
        self.origin = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.scale = (1, 1, 1)
        self.vertices = self.get_vertices()
        self.points = self.vertices.copy()
        self.apply_transformation(origin, rotation, scale)
        self.planes = self.get_planes()
        self.set_color(color)

    def set_color(self, color):
        """You can rewrite this method to change how the color is set. For example, each plane can be a different color."""
        for plane in self.planes:
            plane.color = color
        self.color = color

    def project(self, pt):
        """Get the distance from point to object."""
        dists = [plane.project(pt) for plane in self.planes]
        minIdx = np.argmin(dists)
        return dists[minIdx], self.planes[minIdx]

    def apply_transformation(self, translation, rotation, scale):
        """Apply a transformation to the object."""
        self.origin = translation
        self.rotation = rotation
        self.scale = scale
        # Apply scale, relative to the origin:
        self.points = self.vertices * scale

        # Apply rotation, relative to the origin (EULER ANGLES):
        rotation = np.radians(rotation)
        Rx = np.array(
            [[1, 0, 0], [0, np.cos(rotation[0]), -np.sin(rotation[0])], [0, np.sin(rotation[0]), np.cos(rotation[0])]]
        )
        Ry = np.array(
            [[np.cos(rotation[1]), 0, np.sin(rotation[1])], [0, 1, 0], [-np.sin(rotation[1]), 0, np.cos(rotation[1])]]
        )
        Rz = np.array(
            [[np.cos(rotation[2]), -np.sin(rotation[2]), 0], [np.sin(rotation[2]), np.cos(rotation[2]), 0], [0, 0, 1]]
        )
        self.rotation_matrix = Rz @ Ry @ Rx
        self.points = self.points @ self.rotation_matrix

        # Apply translation:
        self.points = self.points + translation

    def get_points(self):
        return self.points

    def get_vertices(self):
        """
        Compute the vertices of the object centered at (0,0,0).
        Translation, rotation and scale will be applied later.
        """
        raise NotImplementedError

    def get_planes(self):
        """
        Compute the planes of the object. Must reference the points in the order of deffinition of the vertices.
        """
        raise NotImplementedError
