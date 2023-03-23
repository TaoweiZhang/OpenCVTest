from util import Utils
from game.armBend.Grade import Grade
from solution.Pose import Pose
from game.TimeInformation import TimeInformation
from util.VisualizationUtils import index2point, put_text2img


class ArmBendGame:
    def __init__(self):
        self.pose = Pose()
        self.grade = Grade()
        self.time = TimeInformation()
        self.grades = []
        # 游戏状态
        # 1：开始前的倒计时状态；2：Ready Go!；3：游戏进行时
        self.status = 1

    def variable_init(self):
        self.status_init()
        self.time.time_init()
        self.grade.count_init()

    def status_init(self):
        self.status = 1

    # 手臂弯曲计数
    def arm_bend_count(self):
        point12 = index2point(self.pose.img, self.pose.landmark[12])
        point14 = index2point(self.pose.img, self.pose.landmark[14])
        point16 = index2point(self.pose.img, self.pose.landmark[16])

        angle = Utils.get_angle(point12, point14, point16)
        if angle < 15 and self.grade.status == 1:
            self.grade.count += 1
            self.grade.status = 2
        if angle > 60:
            self.grade.status = 1

        put_text2img(self.pose.img, str(self.grade.count), (50, 100), font_scale=3, color=(230, 216, 173),
                     thickness=3)  # 当前局成绩显示

    def game_start(self, frame):
        if len(self.grades) != 0:
            y = 200
            for i in range(len(self.grades) - 1, -1, -1):
                put_text2img(frame, 'Time {}: {}'.format(i + 1, self.grades[i]), (400, y), font_scale=1,
                             color=(230, 216, 173))  # 历史成绩显示
                y += 30

        if self.status == 1 and self.time.count_down > 0:
            put_text2img(frame, str(self.time.count_down), (500, 100), font_scale=3, color=(0, 255, 0),
                         thickness=3)  # 游戏开始倒计时
            if self.time.time_count != 0 and self.time.time_count % 250 == 0:
                self.time.count_down -= 1

        if self.status == 1 and self.time.count_down == 0:
            self.status = 2
            self.time.time_count = 0

        if self.status == 2:
            put_text2img(frame, 'Ready Go!', (130, 250), font_scale=3, color=(0, 0, 255), thickness=3)  # Ready Go!字符串
            if self.time.time_count == 200:
                self.status = 3

        if self.status == 3:
            self.pose.process(frame)
            if not self.pose.landmarks:
                return
            self.arm_bend_count()

            put_text2img(frame, str(self.time.game_total_time), (500, 100), font_scale=3, color=(0, 255, 0),
                         thickness=3)  # 游戏时间显示

            if self.time.time_count % 250 == 0:
                self.time.game_total_time -= 1

            if self.time.game_total_time == 0:
                self.grades.append(str(self.grade.count))
                self.variable_init()

        self.time.time_count += 10
