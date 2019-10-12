import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets):
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 点击play按钮重置所有信息
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        scoreboard.prep_score()
        scoreboard.prep_highscore()
        scoreboard.prep_level()
        scoreboard.prep_ships()
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.reload_ship()

def update_screen(ai_settings, screen, stats, scoreboard, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    scoreboard.show_score()

    # 游戏非活动情况下绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    # 更新子弹位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_aliens_reserve(ai_settings, screen, stats, scoreboard, ship, aliens, bullets)

def check_aliens_reserve(ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    # 碰撞后消除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_highscore(stats, scoreboard)
    if len(aliens) == 0:
        bullets.empty()
        # 删除现有的子弹并新建一群外星人
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        scoreboard.prep_level()
        creat_fleet(ai_settings, screen, aliens, ship)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_aliens_rows(ai_settings, ship_height, alien_height):
    """计算可以容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_aliens_y = int(available_space_y / (2 * alien_height))
    return number_aliens_y


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = 50 + 2 * alien_height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)


def creat_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_aliens_y = get_aliens_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, scoreboard, screen, ship, aliens, bullets):
    """响应飞船被外星人撞到"""
    if stats.ships_left > 0:
        # 剩余飞船数减一
        stats.ships_left -= 1
        # 清空外星人和子弹
        scoreboard.prep_ships()
        aliens.empty()
        bullets.empty()

        # 创建新的外星人和飞船
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.reload_ship()

        # 暂停0.5秒
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, scoreboard, screen, ship, aliens, bullets):
    # 检查是否有外星人到了底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.y >= screen_rect.bottom:
            # 像飞船被撞一样处理
            ship_hit(ai_settings, stats, scoreboard, screen, ship, aliens, bullets)

def update_aliens(ai_settings, stats, scoreboard, screen, ship, aliens, bullets):
    """检查外星人位置是否到屏幕边缘"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检查飞船是否与外星人相撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, scoreboard, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, scoreboard, screen, ship, aliens, bullets)

def check_highscore(stats, scoreboard):
    if stats.score > stats.highscore:
        stats.highscore = stats.score
        score_record = stats.highscore
        scoreboard.prep_highscore()
        with open('record.txt', 'w') as file_object:
            file_object.write(str(score_record))
