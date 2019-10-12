import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 30)

        # 设备初始得分图像
        self.prep_score()
        self.prep_highscore()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_highscore(self):
        """将最高分转换为一幅渲染的图像"""
        rounded_highscore = round(self.stats.highscore, -1)
        score_str = "{:,}".format(rounded_highscore)
        self.highscore_image = self.font.render("Highest Score: " + score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为一幅渲染的图像"""
        self.level_image = self.font.render("Level: " + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom +10

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船
        self.ships.draw(self.screen)

    def prep_ships(self):
        """在屏幕上显示剩余飞船数"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)