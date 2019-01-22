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


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

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

    def get_event(self, event):
        pass


class Turret(Sprite):

    def __init__(self, group, pos, size, image):
        super().__init__(group, pos, size, image)
        self.reserve_image = self.image
        self.rotation = 90

    def get_event(self, event):
        x, y = event.pos[0] - self.rect.x, -(event.pos[1] - self.rect.y)
        try:
            angle = math.degrees(math.atan(y / x))
        except ZeroDivisionError:
            angle = 90
        if x < 0:
            angle += 180
        self.image = pygame.transform.rotate(self.reserve_image,
                                             angle)
        self.rotation = angle


pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Turret Master Python")
pygame.display.set_icon(load_image("game_icon.png", color_key=-1))
clock = pygame.time.Clock()

textures = {"machine_gun": load_image("turrets/machine_gun.png")}

all_sprites = SpriteGroup()
turrets = SpriteGroup()
machine_gun = Turret(turrets, (200, 200), (72, 72), "machine_gun")


def render():
    screen.fill(pygame.Color("black"))
    turrets.draw(screen)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            turrets.get_event(event)
    render()
    clock.tick(FPS)
    pygame.display.flip()
