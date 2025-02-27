import mediapipe as mp
import cv2


class PoseTracker:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.upper_body_connections = [
            (
                self.mp_pose.PoseLandmark.LEFT_WRIST,
                self.mp_pose.PoseLandmark.LEFT_ELBOW,
            ),
            (
                self.mp_pose.PoseLandmark.LEFT_ELBOW,
                self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            ),
            (
                self.mp_pose.PoseLandmark.LEFT_SHOULDER,
                self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            ),
            (
                self.mp_pose.PoseLandmark.RIGHT_WRIST,
                self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            ),
            (
                self.mp_pose.PoseLandmark.RIGHT_ELBOW,
                self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            ),
        ]

    def process_frame(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        points = []

        if results.pose_landmarks:
            for connection in self.upper_body_connections:
                start = results.pose_landmarks.landmark[connection[0]]
                end = results.pose_landmarks.landmark[connection[1]]
                h, w, _ = frame.shape
                start_point = (int(start.x * w), int(start.y * h))
                end_point = (int(end.x * w), int(end.y * h))
                points.append((start_point, end_point))
                cv2.line(frame, start_point, end_point, (0, 255, 0), 4)

        return points, frame
