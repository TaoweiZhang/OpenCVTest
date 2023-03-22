class Grade:
    def __init__(self):
        # 记录当前手臂完全状态
        # 1：未计数；2：已计数
        self.status = 1
        self.count = 0

    def count_init(self):
        self.count = 0
