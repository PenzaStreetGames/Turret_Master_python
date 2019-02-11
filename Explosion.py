import math
import random
import pygame
from Sprite import Sprite
from constants import FPS


class Explosion(Sprite):
    """Класс взрыва"""

    def __init__(self, group, pos, size, image, game_controller=None, rot=0):
        """Иницифлизация взрыва"""
        super().__init__(group, pos, size, image,
                         game_controller=game_controller)
        levels = self.game_controller.levels
        self.rotation = rot
        self.image = pygame.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.life = levels["explosion_life"] * FPS
        game_controller.sounds["explosion"].play()

    def check_death(self):
        """Жизнедеятельность и проверка жизнеспособности взрыва"""
        if self.game_controller.frames - self.start_frame == self.life:
            shells = self.game_controller.shells
            shells.remove(self)
        else:
            self.animate()

    def animate(self):
        """Аниимация взрыва"""
        x, y = self.game_controller.levels["explosion_size"]
        delta_frame = (
                    self.game_controller.frames - self.start_frame) / self.life
        size = (int((y - x) * delta_frame), int((y - x) * delta_frame))
        self.image = pygame.transform.scale(self.reserve_image, size)
        self.rect = self.image.get_rect(center=self.rect.center)
