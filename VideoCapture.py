import cv2

from game.armBend.ArmBendGame import ArmBendGame
from solution.Hands import Hands


class VideoCapture:
    def __init__(self):
        self.game = ArmBendGame()
        self.hands = Hands()
        self.wait_key_time = 10

    def handle_video_capture(self):
        capture = cv2.VideoCapture(0)

        while capture.isOpened():
            retval, image = capture.read()
            if not retval:
                print("error")
                break

            # image = cv2.flip(image, 1)  # 图像水平翻转

            self.game.game_start(image)
            # self.hands.process(image)

            cv2.imshow('', image)
            key = cv2.waitKey(self.wait_key_time)
            if key == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    video_capture = VideoCapture()
    video_capture.handle_video_capture()
