from typing import Union

import numpy as np


class Plane:
    def __init__(self, pt1, pt2, pt3, color=(255, 255, 255), infinite=False):
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
        self.color = color

        self.v12 = pt2 - pt1
        self.v13 = pt3 - pt1
        self.v23 = pt3 - pt2

        self.infinite = infinite
        self.normal = self.__get_normal()

    def __get_normal(self):
        norm = np.cross(self.v12, self.v13)
        return norm / np.linalg.norm(norm)

    def project(self, pt) -> Union[float, np.ndarray]:
        """Get the distance from point to plane."""

        planeDist = np.dot(self.normal, pt - self.pt1)

        if self.infinite:
            return np.abs(planeDist)

        # Get orthonormal projection of pt onto plane
        projPt = pt - planeDist * self.normal

        # Check if projected point is within triangle
        if (
            self.normal.dot(np.cross(self.v12, projPt - self.pt1)) >= 0
            and self.normal.dot(np.cross(self.v23, projPt - self.pt2)) >= 0
            and self.normal.dot(np.cross(-self.v13, projPt - self.pt3)) >= 0
        ):
            return np.abs(planeDist)

        # Projected point is outside triangle, find closest point on triangle
        # Get closest point on each edge
        edges = [
            self.__get_closest_edge_point(self.pt1, self.pt2, projPt),
            self.__get_closest_edge_point(self.pt2, self.pt3, projPt),
            self.__get_closest_edge_point(self.pt3, self.pt1, projPt),
        ]

        # Get distance to each edge
        dist = [np.linalg.norm(edge - pt) for edge in edges]
        # Find closest edge
        # minIdx = np.argmin(dist)
        return min(dist)

    def __get_closest_edge_point(self, pt1, pt2, pt):
        v12 = pt2 - pt1
        v1p = pt - pt1
        v12norm = v12 / np.linalg.norm(v12)
        proj = v1p.dot(v12norm)
        if proj <= 0:
            return pt1
        elif proj >= np.linalg.norm(v12):
            return pt2
        else:
            return pt1 + proj * v12norm
