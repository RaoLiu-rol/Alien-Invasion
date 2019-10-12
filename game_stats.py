class GameStats():
    """跟踪游戏信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        #游戏刚启动时处于非活动状态
        self.game_active = False
        # 读取最高分
        try:
            with open('record.txt', 'r') as file_object:
                record = file_object.read()
                scorerecord = record.rstrip()
            self.highscore = int(scorerecord)
        except FileNotFoundError:
            self.highscore = 0
        self.level = 1

    def reset_stats(self):
        """初始化在游戏运行期间可能会变化的信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1