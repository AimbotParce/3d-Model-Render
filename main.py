from datetime import datetime

import cv2

from obj.camera import Camera
from obj.cube import Cube
from obj.light.pointLight import PointLight
from obj.light.sunLight import Sun
from obj.macros.pyramid import Pyramid
from obj.scene import Scene
from obj.squarePlane import Square


def main():
    scene = Scene(backgroundColor=(246, 186, 108))

    # Add objects:
    scene.add_object(
        Cube(name="testCube", color=(255, 255, 255), origin=[0, 0, 0], rotation=[0, 0, 0], scale=[1, 1, 1])
    )
    # scene.add_object(
    #     Square(
    #         name="testPlane",
    #         color=(80, 200, 126),
    #         origin=[0, 0, -2],
    #         rotation=[0, 0, 0],
    #         scale=[100, 100, 1],
    #         infinite=True,
    #     )
    # )
    # scene.add_object(
    #     Pyramid(name="testPyramid", color=(255, 100, 0), origin=[0, 0, 0], rotation=[0, 0, 0], scale=[1, 1, 1])
    # )

    # Add lights:
    scene.add_light(PointLight(name="testLight", color=(255, 255, 255), origin=[-3, 1, 1], brightness=10))
    scene.add_light(Sun(name="testSunLight", color=(255, 255, 255), rotation=[60, 0, 0], brightness=1))

    camera = Camera(
        name="testCamera",
        origin=[-6, 0, 0],
        rotation=[0, 0, 0],
        resolution=[1920, 1080],  # Y, x
        sensor=(0.01, 0.01),  # Y, x
        focal=0.005,
        depth=30,
        scene=scene,
    )

    start = datetime.now()
    print(f"[{start.strftime('%H:%M:%S')}] Rendering...")

    cv2.startWindowThread()
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

    img = camera.get_image()
    finish = datetime.now()
    print(f"[{finish.strftime('%H:%M:%S')}] Done! ({finish - start})")

    cv2.imwrite(f"renders/Render_{finish.strftime('%m_%d_%H_%M_%S')}.png", img)
    cv2.imshow("Image", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
