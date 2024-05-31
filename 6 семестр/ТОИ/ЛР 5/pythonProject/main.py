import cv2
import numpy as np

image_paths = ["frame1.png", "frame2.png", "frame3.png", "frame4.png", "frame5.png",
               "frame6.png", "frame7.png", "frame8.png", "frame9.png", "frame10.png"]

background = cv2.imread(image_paths[0])

moving_object = np.zeros_like(background)

for path in image_paths[1:]:
    frame = cv2.imread(path)

    diff = cv2.absdiff(background, frame)

    _, thresholded = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    moving_object = cv2.bitwise_or(moving_object, thresholded)

    background = cv2.addWeighted(background, 0.9, frame, 0.1, 0)

cv2.imwrite("background.jpg", background)
cv2.imwrite("moving_object.jpg", moving_object)

