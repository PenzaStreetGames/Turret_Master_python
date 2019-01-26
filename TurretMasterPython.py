import pygame
import os
import math
import random
import json

FPS = 25


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


class GameController:

    def __init__(self):
        self.frames = 0

    def update(self):
        shells.get_my_event("check_death")
        self.frames += 1

    def initialization(self):
        turret_gen.generate_turrets(2)


class TurretGenerator:

    def __init__(self):
        self.turrets = SpriteGroup()
        self.game_controller = game_controller

    def generate_turrets(self, level):
        turret_list = levels["turrets"][str(level)]
        pos = levels["turret_positions"]
        for i in range(len(turret_list)):
            self.turrets.add(Turret(self.turrets, pos[str(i + 1)], (72, 72),
                                    turret_list[i]))
        turrets.add(self.turrets)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_my_event(self, event):
        if event == "check_death":
            for sprite in self:
                sprite.check_death()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group, pos, size, image):
        super().__init__(group)
        self.rect = pygame.Rect(*pos, *size)
        self.rect.center = pos
        self.rect.size = size
        self.center = [pos[0] + size[0] // 2, pos[1] + size[1] // 2]
        self.image = textures[image]
        self.image = pygame.transform.scale(self.image, size)
        self.start_frame = game_controller.frames
        self.pos = pos
        self.size = size

    def get_event(self, event):
        pass


class Turret(Sprite):

    def __init__(self, group, pos, size, image, shot_period=2):
        super().__init__(group, pos, size, image)
        self.reserve_image = self.image
        self.rotation = 90
        self.turret_type = image
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
        if self.shot_period == self.shot_frame:
            if self.turret_type == "machine_gun":
                bullet = Shell(shells, self.rect.center, [12, 18], "bullet",
                               rot=self.rotation + 90, speed=40)
            self.shot_frame = 0
        else:
            self.shot_frame += 1


class Scale(Sprite):

    def __init__(self, turret, scale):
        self.turret = turret
        if scale == "health":
            self.images = textures["health"]
        elif scale == "ammunition":
            self.images = textures["bullets"]

    def update(self):
        pass


class Shell(Sprite):

    def __init__(self, group, pos, size, image, rot=0, life=2, speed=100):
        super().__init__(group, pos, size, image)
        self.rect.y += random.random() * 3
        self.rotation = rot
        self.image = pygame.transform.rotate(self.image, rot)
        self.life = life * FPS
        self.speed = speed + random.random() * speed * 0.1

    def check_death(self):
        if game_controller.frames - self.start_frame == self.life:
            shells.remove(self)
        else:
            self.move()

    def move(self):
        self.rect.x += math.sin(math.radians(self.rotation)) * self.speed
        self.rect.y += math.cos(math.radians(self.rotation)) * self.speed


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
            "heavy_shell": load_image("shells/laser_shell.png"),
            "rocket": load_image("shells/explosion.png"),
            "grenade": load_image("shells/grenade.png"),
            "explosion": load_image("shells/explosion.png"),
            "grenade_explosion": load_image("shells/explosion_grenade.png"),
            "health": [f"scales/heath_bar/heat{image}.png"
                       for image in range(11)],
            "bullets": [f"scales/ammunition/bullet{image}.png"
                       for image in range(6)]}

with open("levels.json", "r", encoding="utf-8") as infile:
    levels = json.loads(infile.read())

turret_properties = {}

game_controller = GameController()
turret_gen = TurretGenerator()
all_sprites = SpriteGroup()
turrets = SpriteGroup()
shells = SpriteGroup()
game_controller.initialization()


def render():
    screen.fill(pygame.Color("black"))
    shells.draw(screen)
    turrets.draw(screen)


mouse_click = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            turrets.get_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = event
            turrets.get_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_click = False
    if mouse_click:
        turrets.get_event(mouse_click)
    game_controller.update()
    render()
    clock.tick(FPS)
    pygame.display.flip()
