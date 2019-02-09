import pygame
import os
import math
import random
import json
import constants
from SpriteGroup import SpriteGroup
from Sprite import Sprite
from Turret import Turret
from TurretGenerator import TurretGenerator
from Shell import Shell
import Interface
from EnemyGenerator import EnemyGenerator
from GameController import GameController
from Scale import Scale


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def load_sound(name):
    fullname = os.path.join('data/sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    return sound


pygame.init()
pygame.mixer.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Turret Master Python")
pygame.display.set_icon(load_image("game_icon.png", color_key=-1))
clock = pygame.time.Clock()

textures = {"machine_gun": load_image("turrets/machine_gun.png"),
            "machine_gun_shoot": load_image("turrets/machine_gun_shoot.png"),
            "laser_turret": load_image("turrets/laser_turret.png"),
            "rocket_launcher": load_image("turrets/rocket_launcher.png"),
            "spitfire": load_image("turrets/spitfire.png"),
            "heavy_turret": load_image("turrets/heavy_turret.png"),
            "grenade_gun": load_image("turrets/grenade_gun.png"),
            "laser_shell": load_image("shells/laser_shell.png"),
            "fire_clot": load_image("shells/fire_clot.png"),
            "bullet": load_image("shells/bullet.png"),
            "heavy_shell": load_image("shells/heavy_shell.png"),
            "rocket": load_image("shells/rocket.png"),
            "grenade": load_image("shells/grenade.png"),
            "explosion": load_image("shells/explosion.png"),
            "grenade_explosion": load_image("shells/explosion_grenade.png"),
            "health": [load_image(f"scales/health_bar/heat{image}.png")
                       for image in range(11)],
            "bullets": [load_image(f"scales/ammunition_bar/bullet{image}.png")
                        for image in range(6)],
            "label": load_image("label.png"),
            "background": load_image("backgrounds/stage1.png"),
            "soldier": [load_image(f"enemies/soldier{i}.png")
                        for i in range(2)],
            "robot": [load_image(f"enemies/robot{i}.png") for i in range(2)],
            "tank": [load_image(f"enemies/tank{i}.png") for i in range(3)],
            "heavy_soldier": [load_image(f"enemies/heavy_soldier{i}.png")
                              for i in range(2)],
            "heavy_robot": [load_image(f"enemies/heavy_robot{i}.png")
                            for i in range(2)],
            "heavy_tank": [load_image(f"enemies/heavy_tank{i}.png")
                           for i in range(3)]}

sounds = {"explosion": load_sound("turrets/Explosion.wav"),
          "grenade_gun": load_sound("turrets/GrenadeLaunch.wav"),
          "heavy_turret": load_sound("turrets/HeavyTurretShoot.wav"),
          "laser_turret": load_sound("turrets/LaserTurretWork.wav"),
          "machine_gun": load_sound("turrets/MachineGunShoot.wav"),
          "rocket_launcher": load_sound("turrets/RocketLaunch.wav"),
          "spitfire": load_sound("turrets/SpitfireShoot.wav"),
          "recharge_start": load_sound("turrets/RechargeStart.wav"),
          "recharge_finish": load_sound("turrets/RechargeFinish.wav"),
          "robot": load_sound("enemies/RobotStep.wav"),
          "soldier": load_sound("enemies/SoldierStep.wav"),
          "tank": load_sound("enemies/TankMove.wav"),
          "heavy_robot": load_sound("enemies/RobotStep.wav"),
          "heavy_soldier": load_sound("enemies/SoldierStep.wav"),
          "heavy_tank": load_sound("enemies/TankMove.wav"),
          "click": load_sound("interface/Click.wav"),
          "money": load_sound("interface/MoneyMove.wav")}

with open("levels.json", "r", encoding="utf-8") as infile:
    levels = json.loads(infile.read())

game_controller = GameController(textures=textures, levels=levels,
                                 sounds=sounds, screen=screen)
game_controller.set_turret_gen(TurretGenerator(game_controller))
game_controller.set_enemy_gen(EnemyGenerator(game_controller))
all_sprites = SpriteGroup()
pygame.mixer.music.load("data/sounds/Take_You_Home_Tonight.mp3")
pygame.mixer.music.play(-1)
# game_controller.initialization(2)


def render():
    screen.fill(pygame.Color("black"))
    if constants.game_process == "level":
        background = pygame.transform.scale(textures["background"], screen_size)
        screen.blit(background, [0, 0])
        game_controller.shells.draw(screen)
        game_controller.turret_gen.turrets.draw(screen)
        game_controller.enemy_gen.enemies.draw(screen)
        game_controller.interface.draw(screen)
    elif constants.game_process == "start_menu":
        screen.fill(pygame.Color(Interface.BG_COLOR))
        Interface.start_window()
    for group in Interface.groups:
        group.update()
        group.draw(screen)


mouse_click = False
player = ""
if __name__ == '__main__':
    while constants.running:
        turrets = game_controller.turret_gen.turrets
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                constants.running = False
            elif event.type == pygame.MOUSEMOTION:
                turrets.get_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = event
                turrets.get_event(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                turrets.get_event(event)
                mouse_click = False
                for group in Interface.groups:
                    for e in group:
                        if Interface.visible:
                            if isinstance(e, (Interface.Button,
                                              Interface.TextField)):
                                res = e.get_event(event)
                                if res:
                                    Interface.visible = False
            elif event.type == pygame.KEYDOWN:
                if Interface.listen_text:
                    data = pygame.key.name(event.key)
                    if data == "backspace":
                        Interface.PLAYER = Interface.PLAYER[:-1]
                    if data == "return":
                        Interface.scene_init("Начать игру")
                    elif len(data) == 1:
                        Interface.PLAYER += data
        if mouse_click:
            turrets.get_event(mouse_click)
        if constants.initialization:
            game_controller.initialization(constants.target_level)
            constants.initialization = False
            game_controller.pause = False
            pygame.mixer.music.load("data/sounds/Mountain_Jump.mp3")
            pygame.mixer.music.play(-1)
        game_controller.update()
        print(game_controller.enemy_gen.score)
        render()
        Interface.visible = True
        clock.tick(constants.FPS)
        pygame.display.flip()
        player = Interface.PLAYER

