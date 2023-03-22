class TimeInformation:
    def __init__(self, count_down=3, game_total_time=5):
        self.time_count = 0  # 毫秒计数
        self.count_down = count_down  # 倒计时时长
        self.game_total_time = game_total_time  # 一局游戏时长
        self.times = [count_down, game_total_time]

    def time_init(self):
        self.time_count = 0
        self.count_down = self.times[0]
        self.game_total_time = self.times[1]
