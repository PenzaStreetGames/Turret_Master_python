import pygame
import os
import math

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
        self.initialization()

    def update(self):
        shells.get_my_event("check_death")
        self.frames += 1

    def initialization(self):
        pass


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
        self.center = [pos[0] + size[0] // 2, pos[1] + size[1] // 2]
        self.image = textures[image]
        self.image = pygame.transform.scale(self.image, size)
        self.start_frame = game_controller.frames
        self.pos = pos
        self.size = size

    def get_event(self, event):
        pass


class Turret(Sprite):

    def __init__(self, group, pos, size, image):
        super().__init__(group, pos, size, image)
        self.reserve_image = self.image
        self.rotation = 90
        self.turret_type = image

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
        if self.turret_type == "machine_gun":
            bullet = Shell(shells, self.pos, self.size, "bullet",
                           rot=self.rotation + 90, speed=10)


class Shell(Sprite):

    def __init__(self, group, pos, size, image, rot=0, life=2, speed=10):
        super().__init__(group, pos, size, image)
        self.rotation = rot
        self.image = pygame.transform.rotate(self.image, rot)
        self.life = life * FPS
        self.speed = speed

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
            "bullet": load_image("shells/bomb.png")}

game_controller = GameController()
all_sprites = SpriteGroup()
turrets = SpriteGroup()
shells = SpriteGroup()
machine_gun = Turret(turrets, (200, 200), (72, 72), "machine_gun")


def render():
    screen.fill(pygame.Color("black"))
    turrets.draw(screen)
    shells.draw(screen)


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
