import time


class TimeInfo:
    def __init__(self, COUNT_DOWN=3, GAME_TIME=10, OVER_TIME=2):
        self.COUNT_DOWN = COUNT_DOWN
        self.GAME_TIME = GAME_TIME
        self.OVER_TIME = OVER_TIME
        self.start_time = -1

        # 游戏状态：1 准备中；2 游戏中；3 结束
        self.status = 1

    def init_start_time(self):
        if self.start_time <= 0:
            self.start_time = time.time()

    def get_use_time(self):
        self.init_start_time()
        cur_time = time.time()
        return cur_time - self.start_time

    def status_change(self):
        info = ''
        run_time = self.COUNT_DOWN + self.GAME_TIME
        round_time = run_time + self.OVER_TIME
        use_time = self.get_use_time()

        if use_time <= self.COUNT_DOWN:
            self.status = 1
            info = 'Ready'
        elif use_time <= run_time:
            self.status = 2
            info = run_time - use_time
        elif use_time <= round_time:
            self.status = 3
            info = 'Over'
        else:
            self.start_time = -1
        return info, self.status
