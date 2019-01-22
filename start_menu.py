import pygame
import os

size = WIDTH, HEIGHT = (800, 600)
v = 50  # пикселей в секунду
fps = 40
WINDOW_PADDING = 10
BASE_BUTTONS_WIDTH = 250
BASE_BUTTONS_HEIGHT = 45
LEVELS_BUTTONS_WIDTH = 75
LEVELS_BUTTONS_HEIGHT = 75
BUTTON_BG = "#F5F5F5"
BG_COLOR = "#9995BD"


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
    def __init__(self, group, width, height, x, y, bg='#BFBECD', bg_border=""):
        super().__init__(group)
        group.add(self)
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color(bg))
        if bg_border:
            pygame.draw.rect(self.image, pygame.Color(bg_border), (0, 0, self.width, self.height), 1)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_text(self, text, text_x, text_y, size=35, bold=True):
        font = get_font(size, bold=True)
        text = font.render(text, 1, pygame.Color("#323232"))
        self.image.blit(text, (text_x, text_y))


class AreaRect(pygame.sprite.Sprite):
    def __init__(self, group, width, height, x, y, bg="#BFBECD"):
        super().__init__(group)
        group.add(self)
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.image = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.image, pygame.Color(bg), (0, 0, self.width, self.height), 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def add_text(self, text, x, y, size=15, bold=False):
        font = get_font(size, bold=False)
        text = font.render(text, 1, pygame.Color("#323232"))
        self.image.blit(text, (x, y))

    def add_rect(self, x, y, width, height, bg):
        pygame.draw.rect(self.image, pygame.Color(bg), (x, y, width, height), 0)

    def add_button(self, x, y, width, height, text, text_offset_x=0, text_offset_y=0, size=15, border=""):
        if border:
            pygame.draw.rect(self.image, pygame.Color(border), (x - 1, y - 1, width + 2, height + 2), 1)
        pygame.draw.rect(self.image, pygame.Color(BUTTON_BG), (x, y, width, height), 0)
        self.add_text(text, x + text_offset_x, y + text_offset_y, size)


def start_window():
    title_width, title_height = 400, 80
    title = Title(start_window_sprites, title_width, title_height, WIDTH // 2 - title_width // 2, 1)
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    auth_header_x, auth_header_y = 360, 60,
    auth_header = Title(start_window_sprites, auth_header_x, auth_header_y, WIDTH // 2 - 360 // 2, HEIGHT // 4,
                        bg="#C8C7D0")
    auth_header.set_text("Вход игрока", 80, 15, 25)

    window_content = AreaRect(start_window_sprites, auth_header.width, auth_header.height * 4, auth_header.x,
                              auth_header.y + auth_header.height + 1, "#BFBECD")
    window_content.add_text("Введите имя вашего игрового профиля.", 10, 20, size=13)
    window_content.add_rect(auth_header.width // 4.5, 80, auth_header.width // 1.8, 50, "#ffffff")
    window_content.add_button(auth_header.width // 4.5 + 20, 170,
                              auth_header.width // 1.8 - 40, 35, "Начать игру", 20, 10)


def menu_window():
    cont_width, cont_height = 470, 550
    window_content = AreaRect(menu_window_sprites, cont_width, cont_height, WIDTH // 2 - cont_width // 2,
                              0, "#BFBECD")
    title_width, title_height = 400, 80
    title = Title(menu_window_sprites, title_width, title_height, WIDTH // 2 - title_width // 2, 1, bg="#CDCDD3",
                  bg_border="#9A999F")
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    title_menu_width, title_menu_height = 360, 80
    title_menu = Title(menu_window_sprites, title_menu_width, title_menu_height, WIDTH // 2 - title_menu_width // 2,
                       100, bg="#CDCDD3", bg_border="#9A999F")
    title_menu.set_text("Главное меню", title.x // 4, title.y + 20, size=30)

    buttons_data = ["Выбрать уровень", "Руководство", "Рекорды", "Создатели", "Выход"]
    for i, button in enumerate(buttons_data):
        window_content.add_button(cont_width // 2 - BASE_BUTTONS_WIDTH // 2, 240 + BASE_BUTTONS_HEIGHT * i * 1.2,
                                  BASE_BUTTONS_WIDTH, BASE_BUTTONS_HEIGHT, button, 20, 10, size=20, border="#9A999F")

    score_width, score_height = 470, 40
    score_content = AreaRect(menu_window_sprites, score_width, score_height, WIDTH // 2 - score_width // 2,
                             window_content.y + window_content.height + 2, "#BFBECD")
    score_content.add_text("Счёт игрока: 0", score_width // 4 + 15, 10, size=18)


def levels_window():
    cont_width, cont_height = 470, 550
    window_content = AreaRect(menu_window_sprites, cont_width, cont_height, WIDTH // 2 - cont_width // 2,
                              0, "#BFBECD")
    title_width, title_height = 400, 80
    title = Title(menu_window_sprites, title_width, title_height, WIDTH // 2 - title_width // 2, 1, bg="#CDCDD3",
                  bg_border="#9A999F")
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    title_menu_width, title_menu_height = 360, 80
    title_menu = Title(menu_window_sprites, title_menu_width, title_menu_height, WIDTH // 2 - title_menu_width // 2,
                       100, bg="#CDCDD3", bg_border="#9A999F")
    title_menu.set_text("Выбор уровня", title.x // 4, title.y + 20, size=30)

    buttons_data = [["Обучение", "Уровень 1", "Уровень 2"], ["Уровень 3", "Уровень 4", "Уровень 5"],
                    ["Уровень 6", "Уровень 7", "Уровень 8"]]
    for i in range(len(buttons_data)):
        for j in range(len(buttons_data[i])):
            window_content.add_button((cont_width // 2 - LEVELS_BUTTONS_WIDTH * 1.7) + 90 * j,
                                      (160 + LEVELS_BUTTONS_HEIGHT) + 90 * i,
                                      LEVELS_BUTTONS_WIDTH, LEVELS_BUTTONS_HEIGHT, buttons_data[i][j],
                                      5, 30, size=11, border="#9A999F")

    score_width, score_height = 470, 40
    score_content = AreaRect(menu_window_sprites, score_width, score_height, WIDTH // 2 - score_width // 2,
                             window_content.y + window_content.height + 2, "#BFBECD")
    score_content.add_text("Счёт игрока: 0", score_width // 4 + 15, 10, size=18)


pygame.init()
screen = pygame.display.set_mode(size)
running = True
screen.fill(pygame.Color(BG_COLOR))
start_window_sprites = pygame.sprite.Group()
menu_window_sprites = pygame.sprite.Group()
levels_window_sprites = pygame.sprite.Group()

# start_window()
# menu_window()
levels_window()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    start_window_sprites.update()
    start_window_sprites.draw(screen)

    menu_window_sprites.update()
    menu_window_sprites.draw(screen)

    levels_window_sprites.update()
    levels_window_sprites.draw(screen)

    pygame.display.flip()
