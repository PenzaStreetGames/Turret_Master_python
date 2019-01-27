import pygame
from Sprite import Sprite

class Scale(Sprite):

    def __init__(self, turret, scale):
        self.turret = turret
        textures = self.game_controller.textures
        if scale == "health":
            self.images = textures["health"]
        elif scale == "ammunition":
            self.images = textures["bullets"]

    def update(self):
        pass