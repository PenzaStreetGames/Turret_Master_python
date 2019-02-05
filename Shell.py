import math
import random
import pygame
from Sprite import Sprite
from constants import FPS
from Explosion import Explosion


class Shell(Sprite):

    def __init__(self, group, pos, size, image, game_controller=None,
                 rot=0, turret_type=None, target=None):
        super().__init__(group, pos, size, image,
                         game_controller=game_controller)
        levels = self.game_controller.levels
        self.rect.y += random.random() * 3
        self.rotation = rot
        self.image = pygame.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.life = int(levels["shells_life"][turret_type] * FPS)
        self.speed = levels["shells_speed"][turret_type] + \
                     random.random() * levels["shells_speed"][turret_type] * 0.1
        self.acceleration = levels["shells_acceleration"][turret_type]
        self.turret_type = turret_type
        self.target = target
        self.pre_dis = math.sqrt((target[0] - self.rect.x) ** 2 +
                                 (target[1] - self.rect.y) ** 2)

    def check_death(self):
        if self.game_controller.frames - self.start_frame == self.life:
            shells = self.game_controller.shells
            shells.remove(self)
        else:
            self.move()
        if self.turret_type in ["grenade_gun", "rocket_launcher"]:
            delta_fly = 20
            turret_dis = math.sqrt((self.target[0] - self.rect.x) ** 2 +
                                   (self.target[1] - self.rect.y) ** 2)
            if turret_dis > self.pre_dis:
                self.boom()
            self.pre_dis = turret_dis

    def move(self):
        self.rect.x += math.sin(math.radians(self.rotation)) * self.speed
        self.rect.y += math.cos(math.radians(self.rotation)) * self.speed
        if self.speed > 0:
            self.speed += self.acceleration

    def boom(self):
        textures = self.game_controller.textures
        Explosion(self.game_controller.shells,
                  (self.rect.x, self.rect.y),
                  [self.game_controller.levels["explosion_size"]
                   [0]] * 2, textures["explosion"],
                  game_controller=self.game_controller,
                  rot=self.rotation)
        shells = self.game_controller.shells
        shells.remove(self)
