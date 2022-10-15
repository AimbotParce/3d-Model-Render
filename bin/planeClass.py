from typing import Union

import numpy as np


class Plane:
    def __init__(self, pt1, pt2, pt3, color=(255, 255, 255), isinfinite=False):
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3
        self.color = color

        self.v12 = pt2 - pt1
        self.v13 = pt3 - pt1
        self.v23 = pt3 - pt2

        self.isinfinite = isinfinite
        self.normal = self.__get_normal()

    def __get_normal(self):
        norm = np.cross(self.v12, self.v13)
        return norm / np.linalg.norm(norm)

    def project(self, pt) -> Union[float, np.ndarray]:
        """Get the distance from point to plane."""

        planeDist = self.normal.dot(pt - self.pt1)

        # Get orthonormal projection of pt onto plane
        projPt = pt - planeDist * self.normal

        if self.isinfinite:
            return planeDist

        # Check if projected point is within triangle
        isIn = (
            self.normal.dot(np.cross(self.v12, projPt - self.pt1)) >= 0
            and self.normal.dot(np.cross(self.v23, projPt - self.pt2)) >= 0
            and self.normal.dot(-np.cross(self.v13, projPt - self.pt3)) >= 0
        )
        if isIn:
            return planeDist

        # Projected point is outside triangle, find closest point on triangle
        # Get closest point on each edge
        edges = [
            self.__get_closest_edge_point(self.pt1, self.pt2, projPt),
            self.__get_closest_edge_point(self.pt2, self.pt3, projPt),
            self.__get_closest_edge_point(self.pt3, self.pt1, projPt),
        ]

        # Get distance to each edge
        dist = [np.linalg.norm(edge - projPt) for edge in edges]
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
