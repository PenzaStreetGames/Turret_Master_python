from SpriteGroup import SpriteGroup
import Interface
import constants
import pygame


class GameController:

    def __init__(self, textures=None, sounds=None, levels=None, screen=None):
        self.frames = 0
        self.turret_gen = None
        self.enemy_gen = None
        self.textures = textures
        self.sounds = sounds
        self.levels = levels
        self.shells = SpriteGroup()
        self.interface = SpriteGroup()
        self.screen = screen
        self.pause = False
        self.win = None
        self.score = 0

    def update(self):
        if constants.level_end:
            self.turret_gen.clear()
            self.enemy_gen.clear()
            constants.level_end = False
            if constants.game_process == "level":
                pygame.mixer.music.load("data/sounds/Take_You_Home_Tonight.mp3")
                pygame.mixer.music.play(-1)
        self.shells.get_my_event("check_death")
        self.turret_gen.update()
        self.enemy_gen.update()
        self.pause = constants.pause
        self.frames += 1

    def set_turret_gen(self, turret_gen):
        self.turret_gen = turret_gen

    def set_enemy_gen(self, enemy_gen):
        self.enemy_gen = enemy_gen

    def initialization(self, level=1):
        self.interface = SpriteGroup()
        self.turret_gen.generate_turrets(level)
        self.enemy_gen.generate_enemies(level)

    def set_pause(self, value):
        self.pause = value

    def set_win(self, value):
        print("win")
        self.win = value
        if self.win is not None:
            Interface.end_modal(value)

