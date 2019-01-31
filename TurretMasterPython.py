import pygame
import os
import math
import random
import json
from constants import *
from SpriteGroup import SpriteGroup
from Sprite import Sprite
from Turret import Turret
from TurretGenerator import TurretGenerator
from Shell import Shell
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


pygame.init()
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
            "background": load_image("backgrounds/stage1.png")}

with open("levels.json", "r", encoding="utf-8") as infile:
    levels = json.loads(infile.read())

game_controller = GameController(textures=textures, levels=levels,
                                 screen=screen)
game_controller.set_turret_gen(TurretGenerator(game_controller))
all_sprites = SpriteGroup()
game_controller.initialization()


def render():
    screen.fill(pygame.Color("black"))
    background = pygame.transform.scale(textures["background"], screen_size)
    screen.blit(background, [0, 0])
    game_controller.shells.draw(screen)
    game_controller.turret_gen.turrets.draw(screen)
    game_controller.interface.draw(screen)


mouse_click = False
running = True
while running:
    render()
    turrets = game_controller.turret_gen.turrets
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            turrets.get_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = event
            turrets.get_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            turrets.get_event(event)
            mouse_click = False
    if mouse_click:
        turrets.get_event(mouse_click)
    game_controller.update()
    render()
    clock.tick(FPS)
    pygame.display.flip()
