from bin.macroClass import Macro
from bin.objectClass import Object
from obj.cube import Cube


class Pyramid(Macro):
    def __init__(self, name, color, origin, rotation, scale):
        objects = [
            Cube(name="testCube", color=color, origin=[0, 0, 1], rotation=[0, 0, 0], scale=[1, 1, 1]),
            Cube(name="testCube", color=color, origin=[0, 0, 0], rotation=[0, 0, 0], scale=[2, 2, 1]),
            Cube(name="testCube", color=color, origin=[0, 0, -1], rotation=[0, 0, 0], scale=[4, 4, 1]),
        ]
        super().__init__(name, objects, origin, rotation, scale)
