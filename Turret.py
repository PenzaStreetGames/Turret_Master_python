import pygame
from Sprite import Sprite
from Shell import Shell
from Scale import Scale
import math


class Turret(Sprite):
    """Класс турели"""

    def __init__(self, group, pos, size, turret_type="machine_gun", image=None,
                 game_controller=None):
        """Инициализация турели"""
        super().__init__(group, pos, size, image=image,
                         game_controller=game_controller)
        levels = self.game_controller.levels
        self.rotation = 90
        self.turret_type = turret_type
        self.shot_period = levels["shot_periods"][turret_type]
        self.shot_frame = self.shot_period
        self.max_shells = levels["turret_max_shells"][turret_type]
        self.shells = self.max_shells
        if self.turret_type in ["machine_gun", "grenade_gun", "rocket_launcher",
                                "heavy_turret"]:
            scale = "ammunition"
        elif self.turret_type in ["laser_turret", "spitfire"]:
            scale = "turret_health"
        self.scale = Scale(group=game_controller.interface,
                           pos=[self.rect.centerx, self.rect.y - 20],
                           size=[self.rect.width - 20, 16], target=self,
                           scale=scale,
                           game_controller=self.game_controller)
        self.work = True
        self.active = True
        self.repairing = False
        self.repair_speed = levels["repairing_speed"][turret_type]
        self.pressed = False
        self.pause = False

    def get_event(self, event):
        """Обработка управления"""
        if event.type == pygame.MOUSEMOTION:
            self.rotate(*event.pos)
            if self.pressed and self.turret_type == "laser_turret":
                self.press(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.active:
                if not self.work:
                    if self.rect.collidepoint(event.pos):
                        self.repairing = True
                else:
                    if self.turret_type != "laser_turret":
                        self.shot(event.pos)
                    else:
                        self.press(event.pos)
                self.pressed = True
            else:
                if self.rect.collidepoint(event.pos):
                    turret_gen = self.game_controller.turret_gen
                    turret_gen.change_turret(self)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False

    def rotate(self, x, y):
        """Поворот турели"""
        self.pause = self.game_controller.pause
        if self.work and self.active and not self.pause:
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
        """Выстрел турели"""
        textures = self.game_controller.textures
        sounds = self.game_controller.sounds
        levels = self.game_controller.levels
        if self.active and not self.pause:
            if self.shells > 0 and self.work:
                if self.shot_period == self.shot_frame:
                    shell_type = levels["turret_shells"][self.turret_type]
                    image = textures[shell_type]
                    shells = self.game_controller.shells
                    size = levels["shell_sizes"][self.turret_type]
                    Shell(shells, self.rect.center, size,
                          game_controller=self.game_controller,
                          image=image,
                          rot=self.rotation + 90,
                          turret_type=self.turret_type, target=pos)
                    self.shells -= 1
                    self.shot_frame = 0
                    self.scale.update()
                    sounds[self.turret_type].play()
                else:
                    self.shot_frame += 1
            else:
                self.work = False

    def press(self, pos):
        """Стрельба лазерной турели"""
        textures = self.game_controller.textures
        if self.active and not self.pause:
            if self.shells > 0 and self.work:
                if self.shot_period == self.shot_frame:
                    shells = self.game_controller.shells
                    if self.turret_type == "laser_turret":
                        x1, y1 = self.rect.center
                        x2, y2 = pos
                        radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
                        if radius >= 350:
                            radius = 350
                        Shell(shells, self.rect.center, [10, radius * 2],
                              game_controller=self.game_controller,
                              image=textures["laser_shell"],
                              rot=self.rotation - 90,
                              turret_type=self.turret_type, target=pos)
                    self.shells -= 1
                    self.scale.update()
                else:
                    self.shot_frame += 1
            else:
                self.work = False

    def update(self):
        """Проверка работоспособности турели"""
        active_type = self.game_controller.turret_gen.active_type
        self.active = self.turret_type == active_type
        self.pause = self.game_controller.pause
        if self.repairing and not self.pause:
            self.repair()

    def repair(self):
        """Восстановление турели"""
        if self.shells < self.max_shells:
            self.shells += self.repair_speed
            self.scale.update()
        else:
            self.shells = self.max_shells
            self.work = True
            self.repairing = False
