from SpriteGroup import SpriteGroup
import Interface
import constants
import pygame
import FileLoadManager


class GameController:
    """Объект, управляющий практически всем в игре"""

    def __init__(self, textures=None, sounds=None, levels=None, screen=None):
        """Инициализация объекта"""
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
        """Обновление игры и проверка перехода из уровня в меню"""
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
        """Привязка контроллера турелей"""
        self.turret_gen = turret_gen

    def set_enemy_gen(self, enemy_gen):
        """Привязка контроллера врагов"""
        self.enemy_gen = enemy_gen

    def initialization(self, level=1):
        """Настройка перед запуском уровня"""
        self.interface = SpriteGroup()
        self.turret_gen.generate_turrets(level)
        self.enemy_gen.generate_enemies(level)
        self.score = 0

    def set_pause(self, value):
        """Остановить/возобновить игру"""
        self.pause = value

    def set_win(self, value):
        """Обозначить ситуацию выигрыша"""
        self.win = value
        if self.win is not None:
            Interface.end_modal(value)
        if self.win:
            player = Interface.USERS[Interface.PLAYER]
            if player["current_level"] <= constants.target_level:
                Interface.USERS[Interface.PLAYER][
                    "current_level"] = constants.target_level + 1
            Interface.USERS[Interface.PLAYER]["score"] += self.score
            FileLoadManager.save_json_file(Interface.USERS)
