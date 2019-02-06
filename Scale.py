import pygame
from Sprite import Sprite
import math


class Scale(Sprite):

    def __init__(self, group, pos, size, target, scale, game_controller=None):
        self.game_controller = game_controller
        textures = self.game_controller.textures
        if scale in ["turret_health", "enemy_health"]:
            self.images = textures["health"]
        elif scale == "ammunition":
            self.images = textures["bullets"]
        self.scale_type = scale
        self.target = target
        super().__init__(group, pos, size, game_controller=game_controller,
                         image=self.images[-1])
        self.radius = self.pos[1] - self.target.pos[1]
        if self.scale_type in ["ammunition", "turret_health"]:
            self.max_value = self.target.max_shells
        elif self.scale_type == "enemy_health":
            self.max_value = self.target.max_health

    def update(self):
        if self.scale_type in ["ammunition", "turret_health"]:
            value = self.target.shells
        elif self.scale_type == "enemy_health":
            value = self.target.health
        index = math.ceil(value / self.max_value * len(self.images))
        index = index if index < len(self.images) else len(self.images) - 1
        index = 0 if index < 0 else index
        index = 0 if value == 0 else index
        self.set_image(self.images[int(index)], self.pos, self.size)
        if self.scale_type in ["ammunition", "turret_health"]:
            self.rotate()

    def rotate(self):
        delta_x = math.sin(math.radians(self.target.rotation)) * self.radius
        delta_y = math.cos(math.radians(self.target.rotation)) * self.radius
        self.rect.center = (self.target.pos[0] + delta_x,
                            self.target.pos[1] + delta_y)
        self.image = pygame.transform.rotate(self.reserve_image,
                                             self.target.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self):
        self.rect.center = (self.target.rect.center[0], self.rect.center[1])
