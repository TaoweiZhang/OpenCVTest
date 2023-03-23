import numpy as np

from util.Constants import *
from util import Utils
from util.VisualizationUtils import *


class Hands:
    def __init__(self):
        self.hands = solutions.hands.Hands()
        self.img = None

        self.multi_hand_landmarks = {}
        self.hand_types = []
        self.left_hand_landmark = None
        self.right_hand_landmark = None

    def process(self, img):
        self.img = img
        self.draw_line()

        if self.left_hand_landmark is None or self.right_hand_landmark is None:
            return

        self.draw_point_num()
        self.gesture_digit_recognition()
        # self.gesture_ok_recognition()

    def gesture_ok_recognition(self):
        """
        ok手势识别（仅左手）
        大拇指和食指距离几乎为0，其他三根手指不弯曲
        """
        fingertip_ls = [4, 8, 12, 16, 20]
        landmark = self.left_hand_landmark.landmark
        finger_status = np.zeros((4,), dtype=np.uint8)

        for idx, num in enumerate(fingertip_ls[2:]):
            top_y = index2point(self.img, landmark, num)[1]
            mid_y = index2point(self.img, landmark, num - 2)[1]
            finger_status[idx] = top_y < mid_y

        distance = Utils.get_distance(landmark[fingertip_ls[0]], landmark[fingertip_ls[1]])
        finger_status[3] = distance < 0.025

        total = np.sum(finger_status)

        if int(total) == 4:
            put_text2img(self.img, 'OK')

    def gesture_digit_recognition(self):
        """"
        手势数字识别（双手）
        对除大拇指外的手指的y坐标进行比较，进而判断手指是否弯曲
        """
        fingertip_ls = [4, 8, 12, 16, 20]

        for hand_type in self.hand_types:
            finger_status = np.zeros((5,), dtype=np.uint8)
            color = HAND_COLOR[hand_type]
            org = HAND_ORG[hand_type]

            is_right = hand_type == RIGHT_HAND_TYPE
            landmarks = self.right_hand_landmark.landmark if is_right else self.left_hand_landmark.landmark

            for idx, num in enumerate(fingertip_ls):
                if idx == 0:
                    top_x = index2point(self.img, landmarks, num)[0]
                    mid_x = index2point(self.img, landmarks, num - 1)[0]
                    finger_status[idx] = top_x < mid_x if is_right else top_x > mid_x
                    continue

                top_y = index2point(self.img, landmarks, num)[1]
                mid_y = index2point(self.img, landmarks, num - 2)[1]
                finger_status[idx] = top_y < mid_y

            total = np.sum(finger_status)
            put_text2img(self.img, total, org=org, color=color)

    # 绘制关键点及连线
    def draw_line(self):
        result = solution_process(self.img, self.hands)
        multi_hand_landmarks = result.multi_hand_landmarks
        if not multi_hand_landmarks:
            return

        for handedness in result.multi_handedness:
            for classification in handedness.classification:
                label = classification.label
                if label not in self.hand_types:
                    self.hand_types.append(label)

        connections = solutions.hands_connections.HAND_CONNECTIONS
        length = len(self.hand_types) if len(multi_hand_landmarks) > len(self.hand_types) else len(multi_hand_landmarks)
        for i in range(length):
            hand_type = self.hand_types[i]
            color = HAND_COLOR[hand_type]

            is_right = hand_type == RIGHT_HAND_TYPE
            if is_right:
                self.right_hand_landmark = multi_hand_landmarks[i]
                landmark = self.right_hand_landmark
            else:
                self.left_hand_landmark = multi_hand_landmarks[i]
                landmark = self.left_hand_landmark

            draw_landmarks(self.img, landmark, connections, color)

    # 绘制关键点的序号
    def draw_point_num(self):
        for hand_type in self.hand_types:
            color = HAND_COLOR[hand_type]

            is_right = hand_type == RIGHT_HAND_TYPE
            landmarks = self.right_hand_landmark.landmark if is_right else self.left_hand_landmark.landmark
            for idx, landmark in enumerate(landmarks):
                x, y = index2point(self.img, landmarks, idx)
                put_text2img(self.img, str(idx), org=(x - 15, y - 5), font_scale=0.4, color=color, thickness=1)
