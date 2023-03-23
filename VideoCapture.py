import time

import cv2

from game.armBend.ArmBendGame import ArmBendGame
from solution.Hands import Hands
from solution.Face import Face
from util.VisualizationUtils import put_text2img


class VideoCapture:
    def __init__(self):
        self.game = ArmBendGame()
        self.hands = Hands()
        self.face = Face()

        self.wait_key_time = 20
        self.prev_frame_time = 0
        self.new_frame_time = 0

    # 计算并显示FPS
    def cal_FPS(self, frame):
        self.new_frame_time = time.time()
        fps = 1 / (self.new_frame_time - self.prev_frame_time)
        self.prev_frame_time = self.new_frame_time
        put_text2img(frame, int(fps), (7, 70), color=(100, 255, 0))

    def handle_video_capture(self):
        capture = cv2.VideoCapture(0)

        while capture.isOpened():
            retval, frame = capture.read()
            if not retval:
                print("can't read image")
                break

            # frame = cv2.flip(frame, 1)  # 图像水平翻转
            # self.cal_FPS(frame)

            # self.game.game_start(frame)
            # self.hands.process(frame)
            self.face.process(frame)
            cv2.imshow('', frame)
            key = cv2.waitKey(self.wait_key_time)
            if key == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    video_capture = VideoCapture()
    video_capture.handle_video_capture()
