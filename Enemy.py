import pygame
from Sprite import Sprite
from Scale import Scale
from Shell import Shell
from Explosion import Explosion
import constants


class Enemy(Sprite):
    """Класс врага"""

    def __init__(self, group, pos, size, enemy_type="soldier",
                 game_controller=None):
        """Инициализация врага"""
        self.game_controller = game_controller
        self.textures = self.game_controller.textures[enemy_type]
        super().__init__(group, pos, size, image=self.textures[0],
                         game_controller=game_controller)
        levels = self.game_controller.levels
        self.rotation = 0
        self.enemy_type = enemy_type
        self.move_period = levels["enemy_periods"][enemy_type]
        self.speed = levels["enemy_speed"][enemy_type]
        self.max_health = levels["enemy_health"][enemy_type]
        self.health = self.max_health
        self.scale = Scale(group=game_controller.interface,
                           pos=[self.rect.centerx, self.rect.y - 20],
                           size=[self.rect.width - 4, 12], target=self,
                           scale="enemy_health",
                           game_controller=self.game_controller)
        self.start_frame = self.game_controller.frames
        self.texture = 0
        self.size = size
        self.pause = False
        self.lose_pos = -20

    def update(self):
        """Проверка столкновений со снарядами и жизнеспособности"""
        self.pause = self.game_controller.pause
        levels = self.game_controller.levels
        if not self.pause:
            shells = self.game_controller.shells
            sprites = pygame.sprite.spritecollide(self, shells, False)
            for shell in sprites:
                if isinstance(shell, Shell):
                    if shell.turret_type in ["rocket_launcher", "grenade_gun"]:
                        shell.boom()
                    self.health -= levels["shell_damage"][shell.turret_type]
                    if shell.turret_type in ["machine_gun", "heavy_turret"]:
                        shells.remove(shell)
                elif isinstance(shell, Explosion):
                    self.health -= levels["shell_damage"]["explosion"]
            if self.health <= 0:
                self.game_controller.enemy_gen.score += levels["enemy_points"][
                    self.enemy_type]
                self.game_controller.enemy_gen.progress += 1
                self.game_controller.interface.remove(self.scale)
                self.game_controller.enemy_gen.enemies.remove(self)
            self.animate()
            self.scale.update()
        if self.rect.centerx <= self.lose_pos:
            constants.pause = True
            self.game_controller.set_win(False)

    def animate(self):
        """Движение врага"""
        frames = self.game_controller.frames
        if (frames - self.start_frame) % self.move_period == 0:
            index = self.texture
            next_index = (index + 1) % len(self.textures)
            self.rect.x -= self.speed
            pos = (self.rect.x, self.rect.y)
            self.set_image(self.textures[next_index], pos, self.size)
            self.texture = next_index
            self.scale.move()
