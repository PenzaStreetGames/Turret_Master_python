import pygame
from Sprite import Sprite
import math

class Scale(Sprite):

    def __init__(self, group, pos, size, turret, scale, game_controller=None):
        self.game_controller = game_controller
        textures = self.game_controller.textures
        if scale == "health":
            self.images = textures["health"]
        elif scale == "ammunition":
            self.images = textures["bullets"]
        self.turret = turret
        super().__init__(group, pos, size, game_controller=game_controller,
                         image=self.images[-1])
        self.radius = self.pos[1] - self.turret.pos[1]
        self.max_shells = self.turret.max_shells

    def update(self):
        shells = self.turret.shells
        index = math.ceil(shells / self.max_shells * len(self.images))
        index = index if index < len(self.images) else len(self.images) - 1
        index = 0 if index < 0 else index
        index = 0 if shells == 0 else index
        self.set_image(self.images[int(index)], self.pos, self.size)
        self.rotate()

    def rotate(self):
        delta_x = math.sin(math.radians(self.turret.rotation)) * self.radius
        delta_y = math.cos(math.radians(self.turret.rotation)) * self.radius
        self.rect.center = (self.turret.pos[0] + delta_x,
                            self.turret.pos[1] + delta_y)
        self.image = pygame.transform.rotate(self.reserve_image,
                                             self.turret.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)