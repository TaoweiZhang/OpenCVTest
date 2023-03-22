from game.armBend.Grade import Grade
from util.VisualizationUtils import *


class Pose:
    def __init__(self):
        self.pose = solutions.pose.Pose()
        self.img = None
        self.landmarks = None  # NormalizedLandmarkList
        self.landmark = None  # RepeatedCompositeContainer
        self.grade = Grade()
        self.grades = []

    def process(self, img):
        self.img = img
        self.draw_line()

        if not self.landmarks:
            return
        self.draw_point_num()

    # 绘制关键点及连线
    def draw_line(self):
        result = solution_process(self.img, self.pose)
        self.landmarks = result.pose_landmarks
        if not self.landmarks:
            return

        connections = solutions.pose_connections.POSE_CONNECTIONS
        draw_landmarks(self.img, self.landmarks, connections)

    # 绘制关键点的序号
    def draw_point_num(self):
        self.landmark = self.landmarks.landmark
        for idx, landmark in enumerate(self.landmark):
            x, y = index2point(self.img, self.landmark, idx)
            put_text2img(self.img, str(idx), (x - 15, y - 2), font_scale=0.4, thickness=1)
