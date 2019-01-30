import pygame
from Sprite import Sprite
from Shell import Shell
from Scale import Scale
import math

class Turret(Sprite):

    def __init__(self, group, pos, size, turret_type="machine_gun", image=None,
                 shot_period=2, recharging_speed=1,
                 game_controller=None):
        super().__init__(group, pos, size, image=image,
                         game_controller=game_controller)
        self.rotation = 90
        self.turret_type = turret_type
        self.shot_frame = 0
        self.shot_period = shot_period
        self.max_shells = self.game_controller.levels["turret_max_shells"][
                                                        turret_type]
        self.shells = self.max_shells
        if self.turret_type in ["machine_gun", "grenade_gun", "rocket_launcher",
                                "heavy_turret"]:
            self.scale = Scale(group=game_controller.interface,
                               pos=[self.rect.centerx, self.rect.y - 20],
                               size=[self.rect.width - 20, 16], turret=self,
                               scale="ammunition",
                               game_controller=self.game_controller)
        elif self.turret_type in ["laser_turret", "spitfire"]:
            self.scale = Scale(group=game_controller.interface,
                               pos=[self.rect.centerx, self.rect.y - 20],
                               size=[self.rect.width - 20, 16], turret=self,
                               scale="health",
                               game_controller=self.game_controller)
        self.work = True
        self.repairing = False
        self.repair_speed = recharging_speed

    def get_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.rotate(*event.pos)
            if self.turret_type == "laser_turret":
                self.shot(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not self.work:
                if self.rect.collidepoint(event.pos):
                    self.repairing = True
            else:
                self.shot(event.pos)


    def rotate(self, x, y):
        if self.work:
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
            self.scale.rotate()

    def shot(self, pos):
        textures = self.game_controller.textures
        if self.shells > 0 and self.work:
            if self.shot_period == self.shot_frame:
                shells = self.game_controller.shells
                if self.turret_type == "machine_gun":
                    bullet = Shell(shells, self.rect.center, [12, 18],
                                   game_controller=self.game_controller,
                                   image=textures["bullet"],
                                   rot=self.rotation + 90, speed=40)
                    self.shot_frame = 0
                elif self.turret_type == "heavy_turret":
                    heavy_shell = Shell(shells, self.rect.center, [16, 18],
                                        game_controller=self.game_controller,
                                        image=textures["heavy_shell"],
                                        rot=self.rotation + 90, speed=30)
                    self.shot_frame = 0
                elif self.turret_type == "spitfire":
                    fire_clot = Shell(shells, self.rect.center, [28, 28],
                                      game_controller=self.game_controller,
                                      image=textures["fire_clot"],
                                      rot=self.rotation + 90, speed=10,
                                      acceleration=-0.15)
                elif self.turret_type == "laser_turret":
                    pygame.draw.line(self.game_controller.screen,
                                     pygame.Color("red"),
                                     self.rect.center, pos, 10)
                    pygame.display.flip()
                self.shells -= 1
                self.scale.update()
            else:
                self.shot_frame += 1
        else:
            self.work = False

    def update(self):
        if self.repairing:
            self.repair()
        if (self.turret_type == "heavy_turret" and
                self.shot_frame != self.shot_period):
            self.shot_frame += 1

    def repair(self):
        if self.shells < self.max_shells:
            self.shells += self.repair_speed
            self.scale.update()
        else:
            self.shells = self.max_shells
            self.work = True
            self.repairing = False