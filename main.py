from datetime import datetime

import cv2

from obj.camera import Camera
from obj.cube import Cube
from obj.light.pointLight import PointLight
from obj.light.sunLight import Sun
from obj.scene import Scene
from obj.squarePlane import Square


def main():
    testCube = Cube(name="testCube", color=(255, 255, 255), origin=[0, 0, 0], rotation=[45, 45, 0], scale=[1, 1, 1])

    testPlane = Square(
        name="testPlane",
        color=(80, 200, 126),
        origin=[0, 0, -2],
        rotation=[0, 0, 0],
        scale=[100, 100, 1],
        infinite=True,
    )

    testLight = PointLight(name="testLight", color=(255, 255, 255), origin=[-3, 1, 1], brightness=10)
    testSunLight = Sun(name="testSunLight", color=(255, 255, 255), rotation=[0, 0, 0], brightness=1)

    testScene = Scene(objects=[testCube, testPlane], lights=[testSunLight, testLight], backgroundColor=(246, 186, 108))

    testCamera = Camera(
        name="testCamera",
        origin=[-3, 0, 0],
        rotation=[0, 0, 0],
        resolution=[40, 40],  # Y, x
        sensor=(0.01, 0.01),  # Y, x
        focal=0.006,
        depth=30,
        scene=testScene,
    )

    start = datetime.now()
    print(f"[{start.strftime('%H:%M:%S')}] Rendering...")

    cv2.startWindowThread()
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

    img = testCamera.get_image()
    finish = datetime.now()
    print(f"[{finish.strftime('%H:%M:%S')}] Done! ({finish - start})")

    cv2.imwrite(f"renders/Render_{finish.strftime('%m_%d_%H_%M_%S')}.png", img)
    cv2.imshow("Image", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
