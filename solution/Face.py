from solution.Threshold import Threshold
from util import Utils
from util.VisualizationUtils import *


class Face:
    def __init__(self):
        self.face = solutions.face_mesh.FaceMesh()
        self.face_detection = solutions.face_detection.FaceDetection()
        self.face_landmarks = None
        self.landmark = None
        self.detection = None

        self.img = None
        self.blink_index = 0
        self.threshold = Threshold()

        # 左眼关键点序号
        self.FACEMESH_LEFT_EYE = [362, 385, 387, 263, 373, 380]
        # 右眼关键点序号
        self.FACEMESH_RIGHT_EYE = [33, 160, 158, 133, 153, 144]

        self.face_x = 0
        self.face_y = 0
        self.face_height = 0
        self.face_width = 0

    def process(self, img):
        self.img = img
        multi_face_landmarks, detections = self.get_landmarks()
        if not multi_face_landmarks or not detections:
            return

        # 默认只处理识别到的第一张脸
        self.face_landmarks = multi_face_landmarks[0]
        self.landmark = self.face_landmarks.landmark
        self.detection = detections[0]

        # self.draw_line()
        # self.draw_point_num()
        self.draw_face_area()
        self.blink_detection()

    def get_landmarks(self):
        multi_face_landmarks = solution_process(self.img, self.face).multi_face_landmarks
        detections = solution_process(self.img, self.face_detection).detections
        return multi_face_landmarks, detections

    # 画出人脸的矩形区域及关键点（圆）
    def draw_face_area(self):
        # 法一
        # 人脸矩阵区域
        img_height, img_width = self.img.shape[:2]
        location_data = self.detection.location_data
        bounding_box = location_data.relative_bounding_box
        self.face_x = int(bounding_box.xmin * img_width)
        self.face_y = int(bounding_box.ymin * img_height)
        self.face_height = int(bounding_box.height * img_height)
        self.face_width = int(bounding_box.width * img_width)
        pt1 = (self.face_x, self.face_y)
        pt2 = (self.face_x + self.face_width, self.face_y + self.face_height)
        cv2.rectangle(self.img, pt1, pt2, color=(0, 0, 255), thickness=2)

        # 关键点
        # for landmark in location_data.relative_keypoints:
        #     x = landmark.x
        #     y = landmark.y
        #     x, y = solutions.drawing_utils._normalized_to_pixel_coordinates(x, y, img_width, img_height)
        #     cv2.circle(self.img, (x, y), radius=3, color=(0, 0, 255), thickness=2)

        # 法二
        # solutions.drawing_utils.draw_detection(self.img, self.detection)

    # 眨眼检测
    def blink_detection(self, threshold_percentage=0.9):
        EAR = self.cal_EAR()
        threshold = self.threshold.cal_threshold(EAR)
        if threshold == -1:
            return

        # 若发现眨眼，将人脸区域图像保存至本地
        if EAR < threshold * threshold_percentage:
            cv2.imwrite('pic/blink_detection/{}.jpg'.format(self.blink_index),
                        self.img[self.face_y:self.face_y + self.face_height, self.face_x:self.face_x + self.face_width])
            print('blink pic saved')
            self.blink_index += 1

    # 计算纵横比EAR
    def cal_EAR(self):
        # 计算右眼左侧的关键点
        p2 = index2point(self.img, self.landmark[160])
        p6 = index2point(self.img, self.landmark[144])
        # 计算右眼右侧的关键点
        p3 = index2point(self.img, self.landmark[158])
        p5 = index2point(self.img, self.landmark[153])
        # 横向的关键点
        p1 = index2point(self.img, self.landmark[33])
        p4 = index2point(self.img, self.landmark[133])

        dis_p2_p6 = Utils.get_distance(p2, p6)
        dis_p3_p5 = Utils.get_distance(p3, p5)
        dis_p1_p4 = Utils.get_distance(p1, p4)

        EAR = (dis_p2_p6 + dis_p3_p5) / (dis_p1_p4 * 2.0) * 10
        return EAR

    # 绘制关键点及连线
    def draw_line(self):
        conn = solutions.face_mesh_connections
        draw_landmarks(self.img, self.face_landmarks, conn.FACEMESH_RIGHT_EYE | conn.FACEMESH_LEFT_EYE,
                       color=(0, 255, 0), thickness=1)

    # 绘制关键点的序号
    def draw_point_num(self):
        for idx, landmark in enumerate(self.landmark):
            if idx not in self.FACEMESH_LEFT_EYE and idx not in self.FACEMESH_RIGHT_EYE:
                continue
            x, y = index2point(self.img, landmark)
            put_text2img(self.img, str(idx), (x - 15, y - 5), font_scale=0.2, thickness=1)
