import random
import cv2 as cv

class Ball:
    def __init__(self, width):
        self.x = random.randint(0, width)
        self.y = 15
        self.vy = 0

        self.color = (
            random.randint(0, 255),  # R
            random.randint(0, 255),  # G
            random.randint(0, 255)  # B
        )

    def update(self, height):
        self.vy += 1
        self.y += self.vy
        if self.y + 15 > height:
            self.y = height - 15
            self.vy = -self.vy * 0.7
            if abs(self.vy) < 1:
                self.vy = 0

    def check_collision(self):
        pass