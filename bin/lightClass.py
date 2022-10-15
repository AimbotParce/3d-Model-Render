import numpy as np

from bin.objectClass import Object


class Light(Object):
    def __init__(self, name, color, origin, rotation, scale):
        super().__init__(name, np.array(color), origin, rotation, scale)

    def get_intensity(self, pt, plane):
        raise NotImplementedError
