import pygame
from Sprite import Sprite
from Shell import Shell
import math

class Turret(Sprite):

    def __init__(self, group, pos, size, turret_type="machine_gun", image=None,
                 shot_period=2,
                 game_controller=None):
        super().__init__(group, pos, size, image=image,
                         game_controller=game_controller)
        self.reserve_image = self.image
        self.rotation = 90
        self.turret_type = turret_type
        self.shot_frame = 0
        self.shot_period = shot_period

    def get_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.rotate(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.shot()

    def rotate(self, x, y):
        x, y = x - self.rect.x, -(y - self.rect.y)
        try:
            angle = math.degrees(math.atan(y / x))
        except ZeroDivisionError:
            angle = 90
        if x < 0:
            angle += 180
        self.image = pygame.transform.rotate(self.reserve_image,
                                             angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rotation = angle

    def shot(self):
        textures = self.game_controller.textures
        if self.shot_period == self.shot_frame:
            shells = self.game_controller.shells
            if self.turret_type == "machine_gun":
                bullet = Shell(shells, self.rect.center, [12, 18],
                               game_controller=self.game_controller,
                               image=textures["bullet"],
                               rot=self.rotation + 90, speed=40)
            self.shot_frame = 0
        else:
            self.shot_frame += 1