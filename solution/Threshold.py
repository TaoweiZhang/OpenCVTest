class Threshold:
    def __init__(self, max_num=10):
        self.max_num = max_num
        self.thresholds = []
        self.threshold = -1

    def cal_threshold(self, EAR):
        if len(self.thresholds) == self.max_num:
            self.threshold = sum(self.thresholds) / self.max_num

        self.thresholds.append(EAR)

        return self.threshold
