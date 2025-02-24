import cv2 as cv
import random
from Ball import Ball
from PoseTracker import PoseTracker


class Main:

    def __init__(self):
        self.camera = cv.VideoCapture(0)
        self.balls = []
        self.tracker = PoseTracker()

    def game(self):
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            frame = cv.flip(frame, 1)
            height, width, channels = frame.shape

            points, frame = self.tracker.process_frame(frame)
            print(points)

            if random.random() < 0.05:
                self.balls.append(Ball(random.randint(15, width - 15)))

            for ball in self.balls:
                ball.update(height, 0.5, points)
                cv.circle(frame, (int(ball.x), int(ball.y)), 15, ball.color, -1)

            cv.imshow('Video', frame)

            if cv.waitKey(15) & 0xFF == ord('q'):
                break

        self.camera.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    app = Main()
    app.game()
