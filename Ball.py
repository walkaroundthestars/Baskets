import random
import cv2 as cv
import numpy as np


class Ball:
    def __init__(self, x_pos, radius=15):
        self.radius = radius
        self.x = x_pos
        self.y = 15
        self.vy = 0
        self.vx = 0

        self.color = (
            random.randint(0, 255),  # R
            random.randint(0, 255),  # G
            random.randint(0, 255)  # B
        )

    def update(self, height, gravity, points):

        self.vy += gravity
        self.x += self.vx  # Add horizontal movement
        self.y += self.vy

        for point in points:
            start, end = np.array(point[0]), np.array(point[1])
            ball_pos = np.array([self.x, self.y])

            # Vector from start to end (line segment)
            line_vec = end - start
            line_vec = line_vec / np.linalg.norm(line_vec)  # Normalize line direction

            # Find the closest point on the line segment
            ball_vec = ball_pos - start
            proj = np.dot(ball_vec, line_vec)  # Project ball onto the line
            proj = np.clip(proj, 0, np.linalg.norm(end - start))
            closest_point = start + proj * line_vec

            # Distance between ball and line
            distance = np.linalg.norm(ball_pos - closest_point)

            if distance <= self.radius:  # Collision detected
                # **Find Normal and Tangent**
                normal = (ball_pos - closest_point)
                normal = normal / np.linalg.norm(normal)  # Normalize normal vector
                tangent = np.array([-normal[1], normal[0]])  # Perpendicular tangent

                # **Reflect velocity across the normal**
                velocity = np.array([self.vx, self.vy])
                normal_component = np.dot(velocity, normal) * normal
                tangent_component = np.dot(velocity, tangent) * tangent

                # Reverse normal component (bounce), keep tangent component (slide)
                reflection = -normal_component * 0.5 + tangent_component * 0.98

                # **Update ball velocity**
                self.vx, self.vy = reflection[0], reflection[1]
                self.x, self.y = closest_point + normal * (self.radius + 1)  # Prevent overlap

                # Stop jittering when movement is too small
                if abs(self.vy) < 1:
                    self.vy = 0
                if abs(self.vx) < 0.5:
                    self.vx = 0


        if self.y + self.radius > height:
            self.y = height - self.radius
            self.vy = -self.vy * gravity
            if abs(self.vy) < 1:
                self.vy = 0

    def check_collision(self):
        pass
