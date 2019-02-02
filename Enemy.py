import pygame
from Sprite import Sprite
from Scale import Scale


class Enemy(Sprite):

    def __init__(self, group, pos, size, enemy_type="soldier", image=None,
                 game_controller=None):
        super().__init__(group, pos, size, image=image,
                         game_controller=game_controller)
        levels = self.game_controller.levels
        self.rotation = -90
        self.enemy_type = enemy_type
        self.move_period = levels["enemy_periods"][enemy_type]
        self.speed = levels["enemy_speed"][enemy_type]
        self.max_health = levels["enemy_health"][enemy_type]
        self.health = self.max_health
        self.scale = Scale()
        self.scale = Scale(group=game_controller.interface,
                           pos=[self.rect.centerx, self.rect.y - 30],
                           size=[self.rect.width - 20, 16], target=self,
                           scale="enemy_health",
                           game_controller=self.game_controller)
