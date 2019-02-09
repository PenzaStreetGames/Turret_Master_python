from SpriteGroup import SpriteGroup
from Enemy import Enemy
from random import random, choice
import constants
import Interface


class EnemyGenerator:

    def __init__(self, game_controller):
        self.enemies = SpriteGroup()
        self.game_controller = game_controller
        self.start_frame = game_controller.frames
        self.pause = game_controller.pause
        self.create_top = 200
        self.create_radius = 300
        self.create_right = 800
        self.level_enemies = []
        self.spawn_period = 15
        self.enemy_number = 0
        self.counter = 0
        self.progress = 0
        self.max_progress = 1
        self.score = 0

    def generate_enemies(self, level):
        self.enemies = SpriteGroup()
        levels = self.game_controller.levels
        textures = self.game_controller.textures
        self.level_enemies = levels["enemies"][str(level)]
        self.enemy_number = levels["enemy_number"][str(level)]
        self.max_progress = self.enemy_number * 2

    def update(self):
        pause = self.game_controller.pause
        if not pause:
            if self.enemy_number != self.counter:
                frame = self.game_controller.frames
                if (frame - self.start_frame) % self.spawn_period == 0:
                    self.create_enemy()
                    self.counter += 1
                    self.progress += 1
            elif len(self.enemies) == 0:
                if constants.game_process == "level":
                    constants.pause = True
                    self.game_controller.set_win(True)
        for enemy in self.enemies:
            enemy.update()
        if constants.game_process == "level":
            Interface.update_indicator(self.progress / self.max_progress)
            Interface.set_score(self.score)

    def create_enemy(self):
        levels = self.game_controller.levels
        textures = self.game_controller.textures
        enemy_type = self.choose_enemy()
        position = self.get_position()
        width = textures[enemy_type][0].get_rect().width
        height = textures[enemy_type][0].get_rect().height
        size = [width * levels["enemy_scale"], height * levels["enemy_scale"]]
        Enemy(self.enemies, position, size, enemy_type=enemy_type,
              game_controller=self.game_controller)

    def get_position(self):
        y = self.create_top + int(self.create_radius * random())
        x = self.create_right + y // 2
        return x, y

    def choose_enemy(self):
        return choice(self.level_enemies)

    def clear(self):
        self.enemies = SpriteGroup()
