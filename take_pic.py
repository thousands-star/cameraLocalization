import os
import cv2
import pygame
import numpy as np
from picamera2 import Picamera2
import time

class Calibration:
    def __init__(self, images_to_collect):
        self.picam2 = Picamera2()
        self.picam2.preview_configuration.main.size = (640, 480)
        self.picam2.preview_configuration.main.format = "RGB888"
        self.picam2.configure("preview")
        self.picam2.start()
        time.sleep(2)

        self.img = np.zeros([480, 640, 3], dtype=np.uint8)
        self.command = {'motion': [0, 0], 'image': False}
        self.image_collected = 0
        self.finish = False
        self.images_to_collect = images_to_collect

    def image_collection(self, dataDir):
        if self.command['image']:
            image = self.picam2.capture_array()
            filename = os.path.join(dataDir, f'calib_{self.image_collected}.png')
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(filename, image)
            self.image_collected += 1
            print(f'Collected {self.image_collected} images for camera calibration.')
        if self.image_collected >= self.images_to_collect:
            self.finish = True
        self.command['image'] = False

    def update_keyboard(self):
        for event in pygame.event.get():
            # Keyboard inputs for optional motion control (extend if needed)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Forward (placeholder)")
                elif event.key == pygame.K_DOWN:
                    print("Backward (placeholder)")
                elif event.key == pygame.K_LEFT:
                    print("Turn Left (placeholder)")
                elif event.key == pygame.K_RIGHT:
                    print("Turn Right (placeholder)")
                elif event.key == pygame.K_RETURN:
                    self.command['image'] = True
            elif event.type == pygame.KEYUP or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.command['motion'] = [0, 0]  # Stop motion

    def control(self):
        # Placeholder if you want to implement motor control
        pass

    def take_pic(self):
        self.img = self.picam2.capture_array()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=int, default=40, help="Number of images to collect")
    args = parser.parse_args()

    currentDir = os.getcwd()
    dataDir = os.path.join(currentDir, 'calib_pics')
    os.makedirs(dataDir, exist_ok=True)

    width, height = 640, 480
    pygame.init()
    canvas = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Calibration')
    canvas.fill((0, 0, 0))
    pygame.display.update()

    calib = Calibration(images_to_collect=args.images)

    print(f'Collecting {args.images} images for camera calibration.')
    print('Press ENTER to capture image.')

    while not calib.finish:
        calib.update_keyboard()
        calib.control()
        calib.take_pic()
        calib.image_collection(dataDir)

        img_surface = pygame.surfarray.make_surface(calib.img)
        img_surface = pygame.transform.flip(img_surface, True, False)
        img_surface = pygame.transform.rotozoom(img_surface, 90, 1)
        canvas.blit(img_surface, (0, 0))
        pygame.display.update()

    print('\nFinished image collection.')
    print('Images saved at:\n', dataDir)
    pygame.quit()
