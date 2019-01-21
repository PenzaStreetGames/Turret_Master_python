import pygame
import os

size = width, height = (500, 500)
v = 50  # пикселей в секунду
fps = 40


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, group, coords):
        super().__init__(group)

    def update(self):
        pass

    def get_event(self, event):
        pass




pygame.init()



screen = pygame.display.set_mode(size)
running = True
screen.fill(pygame.Color("#9995BD"))

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Platform(platforms_group, event.pos)
            if event.button == 3:
                if not player:
                    player = Player(main_group, event.pos)
                else:
                    player.set_coords(event.pos)
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed().index(1)
            if key == 276:
                player.set_coords((player.rect.x - 10, player.rect.y))
            elif key == 275:
                player.set_coords((player.rect.x + 10, player.rect.y))


    pygame.display.flip()