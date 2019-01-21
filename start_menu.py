import pygame
import os

size = WIDTH, HEIGHT = (800, 600)
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


def get_font(size, bold=False):
    return pygame.font.Font(os.path.join("data", "fonts", 'PSG_Font.ttf'), size)


class Title(pygame.sprite.Sprite):
    def __init__(self, group, width, height, x, y, text=None):
        super().__init__(group)
        group.add(self)
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.image = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.image, pygame.Color('#BFBECD'), (0, 0, self.width, self.height), 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def set_text(self, text, text_x, text_y, size=135, bold=True):
        font = get_font(size, bold=True)
        text = font.render(text, 1, pygame.Color("#323232"))
        self.image.blit(text, (text_x, text_y))


def start_window():
    title_width, title_height = 400, 80
    title = Title(all_sprites, title_width, title_height, WIDTH // 2 - title_width // 2, 1)
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)
    auth_header_x, auth_header_y = 360, 60,
    auth_header = Title(all_sprites, auth_header_x, auth_header_y, WIDTH // 2 - 360 // 2, HEIGHT // 4, "Мастер турелей")
    auth_header.set_text("fgs", auth_header.x, auth_header.y)
    # auth = WindowAuth(all_sprites, WIDTH, HEIGHT)



pygame.init()
screen = pygame.display.set_mode(size)
running = True
screen.fill(pygame.Color("#9995BD"))
all_sprites = pygame.sprite.Group()
start_window()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()
    all_sprites.draw(screen)



    pygame.display.flip()