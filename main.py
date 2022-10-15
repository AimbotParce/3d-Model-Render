from datetime import datetime

import cv2

from obj.camera import Camera
from obj.cube import Cube
from obj.scene import Scene

testCube = Cube("testCube", (0, 0, 0), [0, 0, 0], [0, 0, 0], [1, 1, 1])

testScene = Scene([testCube], (246, 186, 108))

testCamera = Camera("testCamera", [-5, 0, 0], [0, 0, 0], 5, [100, 100], 100, testScene)


start = datetime.now()
print(f"[{start.strftime('%H:%M:%S')}] Rendering...")
cv2.startWindowThread()
cv2.namedWindow("Image", cv2.WINDOW_FREERATIO)
img = testCamera.get_image()
print(f"[{datetime.now().strftime('%H:%M:%S')}] Done! ({datetime.now() - start})")
print(img.shape)
cv2.imshow("Image", img)
cv2.waitKey(0)
