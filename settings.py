class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船的设置

        self.ship_limit = 3

        # 子弹的设置

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # 外星人的设置
        self.fleet_drop_speed = 10
        # fleet_direction为1表示向右移，-1表示向左移
        self.fleet_direction = 1

        # 确定速度系数
        self.speed_up_factor = 5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):

        self.ship_speed_factor = 1
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右移，-1表示向左移
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speed_up_factor
        self.bullet_speed_factor *= self.speed_up_factor
        self.alien_speed_factor *= self.speed_up_factor