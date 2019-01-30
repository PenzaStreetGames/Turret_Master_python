import math
import random
import pygame
from Sprite import Sprite
from constants import FPS


class Shell(Sprite):

    def __init__(self, group, pos, size, image, game_controller=None,
                 rot=0, life=2, speed=100, acceleration=0):
        super().__init__(group, pos, size, image,
                         game_controller=game_controller)
        self.rect.y += random.random() * 3
        self.rotation = rot
        self.image = pygame.transform.rotate(self.image, rot)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.life = life * FPS
        self.speed = speed + random.random() * speed * 0.1
        self.acceleration = acceleration

    def check_death(self):
        if self.game_controller.frames - self.start_frame == self.life:
            shells = self.game_controller.shells
            shells.remove(self)
        else:
            self.move()

    def move(self):
        self.rect.x += math.sin(math.radians(self.rotation)) * self.speed
        self.rect.y += math.cos(math.radians(self.rotation)) * self.speed
        if self.speed > 0:
            self.speed += self.acceleration

    def look_at(self, pos):
        ray_pos = self.rect.center
        x, y = pos
        radius = math.sqrt((x - ray_pos[0]) ** 2 + (y - ray_pos[1]) ** 2)
        self.image.get_rect().width = radius
        print(radius)