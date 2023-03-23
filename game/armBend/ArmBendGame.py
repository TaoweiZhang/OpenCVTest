from game.TimeInfo import TimeInfo
from util import Utils
from game.armBend.Grade import Grade
from solution.Pose import Pose
from util.VisualizationUtils import index2point, put_text2img


class ArmBendGame:
    def __init__(self):
        self.pose = Pose()
        self.grade = Grade()
        self.time = TimeInfo()
        self.grade_flag = True
        self.grades = []

    def game_grades_show(self, frame):
        if len(self.grades) != 0:
            y = 200
            for i in range(len(self.grades) - 1, -1, -1):
                put_text2img(frame, 'Time {}: {}'.format(i + 1, self.grades[i]), (400, y), font_scale=1,
                             color=(230, 216, 173))  # 历史成绩显示
                y += 30

    # 手臂弯曲计数
    def arm_bend_count(self):
        point12 = index2point(self.pose.img, self.pose.landmark, 12)
        point14 = index2point(self.pose.img, self.pose.landmark, 14)
        point16 = index2point(self.pose.img, self.pose.landmark, 16)

        angle = Utils.get_angle(point12, point14, point16)
        if angle < 15 and self.grade.status == 1:
            self.grade.count += 1
            self.grade.status = 2
        if angle > 60:
            self.grade.status = 1

        put_text2img(self.pose.img, str(self.grade.count), (50, 100), font_scale=3, color=(230, 216, 173),
                     thickness=3)  # 当前局成绩显示

    def game_start(self, frame):
        info, status = self.time.status_change()

        if status == 3 and self.grade_flag:
            count = self.grade.count
            self.grade.count_init()
            self.grades.append(str(count))
            self.grade_flag = False

        if status == 2:
            self.grade_flag = True
            self.pose.process(frame)
            if not self.pose.landmarks:
                return
            self.arm_bend_count()
            put_text2img(frame, info, (500, 100), font_scale=3, color=(0, 255, 0), thickness=3)  # 游戏时间显示
        else:
            put_text2img(frame, info, (130, 250), font_scale=3, color=(0, 0, 255), thickness=3)

        self.game_grades_show(frame)
