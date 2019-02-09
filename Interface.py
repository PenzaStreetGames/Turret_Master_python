import pygame
import os
import constants
from FileLoadManager import *
import TurretMasterPython

size = WIDTH, HEIGHT = (800, 600)
v = 50  # пикселей в секунду
CHOOSEN_LEVEL = 1
WINDOW_PADDING = 10
BASE_BUTTONS_WIDTH = 250
BASE_BUTTONS_HEIGHT = 45
LEVELS_BUTTONS_WIDTH = 75
LEVELS_BUTTONS_HEIGHT = 75
BUTTON_BG = "#F5F5F5"
BG_COLOR = "#9995BD"
PLAYER = ""
USERS = load_json_file("users.json", False)
SCORE = 0
Records = [[name, data["score"]] for name, data in USERS.items()]
Records.sort(key=lambda pair: pair[1], reverse=True)
SCENES_TEXT = {
    "titres_window": load_data_file("about.txt"),
    "learn_window": load_data_file("howplay.txt"),
    "records_window": formating(Records)}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def set_score(data):
    global SCORE, Records
    USERS[PLAYER] = USERS.get(PLAYER, {"score": 0, "current_level": 1})
    SCORE = data
    Records = [[name, data["score"]] for name, data in USERS.items()]
    Records.sort(key=lambda pair: pair[1], reverse=True)
    SCENES_TEXT["records_window"] = formating(Records)


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
            pygame.draw.rect(self.image, pygame.Color(bg_border),
                             (0, 0, self.width, self.height), 1)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def set_text(self, text, text_x, text_y, size=35, bold=True):
        font = get_font(size, bold=True)
        text = font.render(text, 1, pygame.Color("#323232"))
        self.image.blit(text, (text_x, text_y))


class AreaRect(pygame.sprite.Sprite):
    def __init__(self, group, width, height, x, y, bg="#BFBECD"):
        super().__init__(group)
        group.add(self)
        self.group = group
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.image = pygame.Surface((self.width, self.height))
        pygame.draw.rect(self.image, pygame.Color(bg),
                         (0, 0, self.width, self.height), 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def add_text(self, text, x, y, size=15, bold=False):
        font = get_font(size, bold=False)
        text = font.render(text, 1, pygame.Color("#323232"))
        self.image.blit(text, (x, y))

    def add_rect(self, x, y, width, height, bg, border=False):
        if border:
            pygame.draw.rect(self.image, pygame.Color(border),
                             (x, y, width + 2, height + 2), 1)
        pygame.draw.rect(self.image, pygame.Color(bg),
                         (x + 1, y + 1, width, height), 0)

    def add_button(self, x, y, width, height, text, text_offset_x=0,
                   text_offset_y=0, size=15, border=""):
        Button(self.group, self.x + x, self.y + y, width, height, text, border,
               size, text_offset_x, text_offset_y)

    def add_textfield(self, x, y, width, height, text, text_offset_x=0,
                      text_offset_y=0, size=15, border=""):
        TextField(self.group, self.x + x, self.y + y, width, height, text,
                  border, size, text_offset_x, text_offset_y)


class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, width, height, text, border, size,
                 text_offset_x, text_offset_y):
        super().__init__(group)
        self.width = width
        self.height = height
        if border:
            self.image = pygame.Surface((self.width + 2, self.height + 2))
            self.image.fill(pygame.Color(border))
            surf = pygame.Surface((self.width, self.height))
            surf.fill(pygame.Color(BUTTON_BG))
            self.image.blit(surf, (1, 1))
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(pygame.Color(BUTTON_BG))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.text = text
        self.add_text(text, text_offset_x, text_offset_y, size)

    def add_text(self, text, x, y, size=15, bold=False):
        font = get_font(size, bold=False)
        text = font.render(text, 1, pygame.Color("#323232"))
        self.image.blit(text, (x, y))

    def boom(self):
        print(self.text)

    def get_event(self, event):
        if self.rect.collidepoint(event.pos):
            # self.boom()
            scene_init(self.text)
            return True


class TextField(Button):
    def __init__(self, group, x, y, width, height, text, border, size,
                 text_offset_x, text_offset_y):
        super().__init__(group, x, y, width, height, text, border, size,
                         text_offset_x, text_offset_y)

    def update(self):
        global listen_text
        if listen_text:
            self.text = input_data
            self.add_text(self.text, 5, 15)

    def get_event(self, event):
        global listen_text
        if self.rect.collidepoint(event.pos):
            listen_text = True


def start_window():
    screen.fill(pygame.Color(BG_COLOR))

    title_width, title_height = 400, 80
    title = Title(start_window_sprites, title_width, title_height,
                  WIDTH // 2 - title_width // 2, 1)
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    auth_header_x, auth_header_y = 360, 60,
    auth_header = Title(start_window_sprites, auth_header_x, auth_header_y,
                        WIDTH // 2 - 360 // 2, HEIGHT // 4,
                        bg="#C8C7D0")
    auth_header.set_text("Вход игрока", 80, 15, 25)

    window_content = AreaRect(start_window_sprites, auth_header.width,
                              auth_header.height * 4, auth_header.x,
                              auth_header.y + auth_header.height + 1, "#BFBECD")
    window_content.add_text("Введите имя вашего игрового профиля.", 10, 20,
                            size=13)
    window_content.add_textfield(auth_header.width // 4.5, 80,
                                 auth_header.width // 1.8, 50, "   ", 20, 10,
                                 border="#9A999F")
    window_content.add_button(auth_header.width // 4.5 + 20, 170,
                              auth_header.width // 1.8 - 40, 35, "Начать игру",
                              20, 10, border="#9A999F")


def menu_window():
    screen.fill(pygame.Color(BG_COLOR))

    cont_width, cont_height = 470, 550
    window_content = AreaRect(menu_window_sprites, cont_width, cont_height,
                              WIDTH // 2 - cont_width // 2,
                              0, "#BFBECD")
    title_width, title_height = 400, 80
    title = Title(menu_window_sprites, title_width, title_height,
                  WIDTH // 2 - title_width // 2, 1, bg="#CDCDD3",
                  bg_border="#9A999F")
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    title_menu_width, title_menu_height = 360, 80
    title_menu = Title(menu_window_sprites, title_menu_width, title_menu_height,
                       WIDTH // 2 - title_menu_width // 2,
                       100, bg="#CDCDD3", bg_border="#9A999F")
    title_menu.set_text("Главное меню", title.x // 4, title.y + 20, size=30)

    buttons_data = ["Выбрать уровень", "Руководство", "Рекорды", "Создатели",
                    "Выход"]
    for i, button in enumerate(buttons_data):
        window_content.add_button(cont_width // 2 - BASE_BUTTONS_WIDTH // 2,
                                  240 + BASE_BUTTONS_HEIGHT * i * 1.2,
                                  BASE_BUTTONS_WIDTH, BASE_BUTTONS_HEIGHT,
                                  button, 20, 10, size=20, border="#9A999F")

    score_width, score_height = 470, 40
    score_content = AreaRect(menu_window_sprites, score_width, score_height,
                             WIDTH // 2 - score_width // 2,
                             window_content.y + window_content.height + 2,
                             "#BFBECD")
    score_content.add_text(f"Счёт: {SCORE}", score_width - 150, 10, size=18)
    score_content.add_text(PLAYER, 30, 10, size=18)

    constants.level_end = True
    TurretMasterPython.game_controller.update()
    constants.game_process = "start_menu"


def levels_window():
    screen.fill(pygame.Color(BG_COLOR))

    cont_width, cont_height = 470, 550
    window_content = AreaRect(levels_window_sprites, cont_width, cont_height,
                              WIDTH // 2 - cont_width // 2,
                              0, "#BFBECD")
    title_width, title_height = 400, 80
    title = Title(levels_window_sprites, title_width, title_height,
                  WIDTH // 2 - title_width // 2, 1, bg="#CDCDD3",
                  bg_border="#9A999F")
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    title_menu_width, title_menu_height = 360, 80
    title_menu = Title(levels_window_sprites, title_menu_width,
                       title_menu_height, WIDTH // 2 - title_menu_width // 2,
                       100, bg="#CDCDD3", bg_border="#9A999F")
    title_menu.set_text("Выбор уровня", title.x // 4, title.y + 20, size=30)

    buttons_data = [["Уровень 1", "Уровень 2", "Уровень 3"],
                    ["Уровень 4", "Уровень 5", "Уровень 6"]]
    l = 0
    for i in range(len(buttons_data)):
        for j in range(len(buttons_data[i])):
            l += 1
            if l > USERS[PLAYER]["current_level"]:
                break
            window_content.add_button(
                (cont_width // 2 - LEVELS_BUTTONS_WIDTH * 1.7) + 90 * j,
                (160 + LEVELS_BUTTONS_HEIGHT) + 90 * i,
                LEVELS_BUTTONS_WIDTH, LEVELS_BUTTONS_HEIGHT, buttons_data[i][j],
                5, 30, size=11, border="#9A999F")
    window_content.add_button(cont_width // 2 - LEVELS_BUTTONS_WIDTH * 1.7,
                              (160 + LEVELS_BUTTONS_HEIGHT) + 90 * (i + 1),
                              (LEVELS_BUTTONS_WIDTH + 10) * 3, 35,
                              "Назад в главное меню", 25, 10, border="#9A999F")
    score_width, score_height = 470, 40
    score_content = AreaRect(levels_window_sprites, score_width, score_height,
                             WIDTH // 2 - score_width // 2,
                             window_content.y + window_content.height + 2,
                             "#BFBECD")
    score_content.add_text(f"Счёт: {SCORE}", score_width - 150, 10, size=18)
    score_content.add_text(PLAYER, 30, 10, size=18)


def titres_window():
    screen.fill(pygame.Color(BG_COLOR))

    cont_width, cont_height = 470, 550
    window_content = AreaRect(titres_sprites, cont_width, cont_height,
                              WIDTH // 2 - cont_width // 2,
                              0, "#BFBECD")
    title_width, title_height = 400, 80
    title = Title(titres_sprites, title_width, title_height,
                  WIDTH // 2 - title_width // 2, 1, bg="#CDCDD3",
                  bg_border="#9A999F")
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    title_menu_width, title_menu_height = 360, 80
    title_menu = Title(titres_sprites, title_menu_width, title_menu_height,
                       WIDTH // 2 - title_menu_width // 2,
                       100, bg="#CDCDD3", bg_border="#9A999F")
    title_menu.set_text("Создатели", title.x // 3, title.y + 20, size=30)
    for i, row in enumerate(SCENES_TEXT["titres_window"]):
        window_content.add_text(row, 60, 225 + 30 * i, size=15)

    window_content.add_button(cont_width // 2 - LEVELS_BUTTONS_WIDTH * 1.7,
                              500,
                              (LEVELS_BUTTONS_WIDTH + 10) * 3, 35,
                              "Назад в главное меню", 25, 10, border="#9A999F")
    score_width, score_height = 470, 40
    score_content = AreaRect(titres_sprites, score_width, score_height,
                             WIDTH // 2 - score_width // 2,
                             window_content.y + window_content.height + 2,
                             "#BFBECD")

    score_content.add_text(f"Счёт: {SCORE}", score_width - 150, 10, size=18)
    score_content.add_text(PLAYER, 30, 10, size=18)


def records_window():
    screen.fill(pygame.Color(BG_COLOR))

    cont_width, cont_height = 470, 550
    window_content = AreaRect(records_sprites, cont_width, cont_height,
                              WIDTH // 2 - cont_width // 2,
                              0, "#BFBECD")
    title_width, title_height = 400, 80
    title = Title(records_sprites, title_width, title_height,
                  WIDTH // 2 - title_width // 2, 1, bg="#CDCDD3",
                  bg_border="#9A999F")
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    title_menu_width, title_menu_height = 360, 80
    title_menu = Title(records_sprites, title_menu_width, title_menu_height,
                       WIDTH // 2 - title_menu_width // 2,
                       100, bg="#CDCDD3", bg_border="#9A999F")
    title_menu.set_text("Рекорды", title.x // 2, title.y + 20, size=30)
    for i, row in enumerate(SCENES_TEXT["records_window"][:5]):
        window_content.add_rect(50, 250 + 45 * i, title_width, 40, bg="#CDCDD3",
                                border="#9A999F")
        window_content.add_text(row, 60, 255 + 45 * i, size=15)

    window_content.add_button(cont_width // 2 - LEVELS_BUTTONS_WIDTH * 1.7,
                              500,
                              (LEVELS_BUTTONS_WIDTH + 10) * 3, 35,
                              "Назад в главное меню", 25, 10, border="#9A999F")
    score_width, score_height = 470, 40
    score_content = AreaRect(records_sprites, score_width, score_height,
                             WIDTH // 2 - score_width // 2,
                             window_content.y + window_content.height + 2,
                             "#BFBECD")
    score_content.add_text(f"Счёт: {SCORE}", score_width - 150, 10, size=18)
    score_content.add_text(PLAYER, 30, 10, size=18)


def learn_window():
    screen.fill(pygame.Color(BG_COLOR))

    cont_width, cont_height = 470, 550
    window_content = AreaRect(learn_sprites, cont_width, cont_height,
                              WIDTH // 2 - cont_width // 2,
                              0, "#BFBECD")
    title_width, title_height = 400, 80
    title = Title(learn_sprites, title_width, title_height,
                  WIDTH // 2 - title_width // 2, 1, bg="#CDCDD3",
                  bg_border="#9A999F")
    title.set_text("Мастер турелей", title.x // 7, title.y + 10)

    title_menu_width, title_menu_height = 360, 80
    title_menu = Title(learn_sprites, title_menu_width, title_menu_height,
                       WIDTH // 2 - title_menu_width // 2,
                       100, bg="#CDCDD3", bg_border="#9A999F")
    title_menu.set_text("Руководство", title.x // 3, title.y + 20, size=30)
    for i, row in enumerate(SCENES_TEXT["learn_window"]):
        window_content.add_text(row, 20, 205 + 30 * i, size=15)

    window_content.add_button(cont_width // 2 - LEVELS_BUTTONS_WIDTH * 1.7,
                              500,
                              (LEVELS_BUTTONS_WIDTH + 10) * 3, 35,
                              "Назад в главное меню", 25, 10, border="#9A999F")
    score_width, score_height = 470, 40
    score_content = AreaRect(learn_sprites, score_width, score_height,
                             WIDTH // 2 - score_width // 2,
                             window_content.y + window_content.height + 2,
                             "#BFBECD")
    score_content.add_text(f"Счёт: {SCORE}", score_width - 150, 10, size=18)
    score_content.add_text(PLAYER, 30, 10, size=18)


def game_process_window():
    screen.fill(pygame.Color("#5D5D5C"))

    cont_width, cont_height = WIDTH, 80
    window_content_top = AreaRect(game_process_sprites, cont_width, cont_height,
                                  WIDTH // 2 - cont_width // 2,
                                  0, "#A4A4A2")
    window_content_top.add_text("Мастер турелей", cont_width // 2 - 160, 10,
                                size=35)
    window_content_top.add_button(window_content_top.width - 115, 15,
                                  100, 45, "Пауза", 25, 15, border="#9A999F")

    constants.game_process = "level"
    constants.level_end = False
    constants.pause = False


def update_indicator(procent):
    if not game_process_sprites:
        return
    game_process_indicators.empty()
    cont_width, cont_height = WIDTH, 80
    window_content_bottom = AreaRect(game_process_indicators, cont_width,
                                     cont_height, WIDTH // 2 - cont_width // 2,
                                     HEIGHT - cont_height, "#A4A4A2")
    window_content_bottom.add_rect(10, 10,
                                   120, cont_height - 20, bg="#B7B7B5",
                                   border="#9A999F")
    window_content_bottom.add_text(f"Уровень {CHOOSEN_LEVEL}", 20, 30)

    window_content_bottom.add_rect(cont_width - 130, 10,
                                   120, cont_height - 20, bg="#B7B7B5",
                                   border="#9A999F")
    window_content_bottom.add_text(f"Счёт: {SCORE}", cont_width - 120, 30)

    window_content_bottom.add_rect(cont_width - cont_width // 1.55, 10,
                                   240, cont_height - 20, bg="#B7B7B5",
                                   border="#9A999F")
    window_content_bottom.add_text("Прогресс уровня",
                                   cont_width - cont_width // 1.69, 15)
    window_content_bottom.add_rect(cont_width - cont_width // 1.65, 50,
                                   int(175 * procent), cont_height // 8,
                                   bg="#009113",
                                   border="#9A999F")


def pause_modal():
    cont_width, cont_height = 300, 250
    pause_window = AreaRect(pause_modal_sprites, cont_width, cont_height,
                            WIDTH // 2 - cont_width // 2, 130, "#A4A4A2")
    pause_window.add_rect(10, 10, cont_width - 20, 50, bg="#B7B7B5",
                          border="#9A999F")
    pause_window.add_text("Пауза", cont_width // 3, 20, size=25)
    pause_window.add_button(50, 95, cont_width - 100, 45, "Продолжить", 15, 10,
                            border="#9A999F", size=18)
    pause_window.add_button(50, 150, cont_width - 100, 45, "Главное меню", 15,
                            10, border="#9A999F", size=18)
    constants.pause = True


def end_modal(result):
    if not game_process_sprites:
        return
    text_results = {0: "Уровень провален", 1: "Уровень пройден"}
    cont_width, cont_height = 300, 250
    pause_window = AreaRect(end_modal_sprites, cont_width, cont_height,
                            WIDTH // 2 - cont_width // 2, 130, "#A4A4A2")
    pause_window.add_rect(10, 10, cont_width - 20, 50, bg="#B7B7B5",
                          border="#9A999F")
    pause_window.add_text(text_results[result], cont_width // 6, 20, size=20)
    pause_window.add_rect(50, 100, cont_width - 100, 50, bg="#B7B7B5",
                          border="#9A999F")
    pause_window.add_text(f"Счёт: {SCORE}", cont_width // 3, 120)
    pause_window.add_button(50, 200, cont_width // 4, 35, "Рестарт", 5, 10,
                            border="#9A999F", size=13)

    pause_window.add_button(130, 200, cont_width // 2.5, 35, "Главное меню", 5,
                            10, border="#9A999F", size=13)


def clear_pause():
    pause_modal_sprites.empty()
    game_process_window()
    constants.pause = False


def clear_win():
    end_modal_sprites.empty()
    game_process_window()


def exit_game():
    constants.running = False


def scene_init(scene):
    islevel = scene.split()
    if islevel[0] == "Уровень":
        global CHOOSEN_LEVEL
        CHOOSEN_LEVEL = int(islevel[1])
        constants.initialization = True
        constants.target_level = int(islevel[1])

    scenes = {"Начать игру": menu_window,
              "Выбрать уровень": levels_window,
              "Главное меню": menu_window,
              "Назад в главное меню": menu_window,
              "Уровень 1": game_process_window,
              "Уровень 2": game_process_window,
              "Уровень 3": game_process_window,
              "Уровень 4": game_process_window,
              "Уровень 5": game_process_window,
              "Уровень 6": game_process_window,
              "Создатели": titres_window,
              "Рекорды": records_window,
              "Руководство": learn_window,
              "Выход": exit_game,
              }
    buttons = {
        "Пауза": pause_modal,
        "Продолжить": clear_pause,
    }
    if scene in scenes:
        for group in groups:
            group.empty()
        scenes[scene]()
    if scene in buttons:
        buttons[scene]()


pygame.init()
clock = pygame.time.Clock()
listen_text = False
input_data = ""
screen = pygame.display.set_mode(size)
start_window_sprites = pygame.sprite.Group()
menu_window_sprites = pygame.sprite.Group()
levels_window_sprites = pygame.sprite.Group()
titres_sprites = pygame.sprite.Group()
records_sprites = pygame.sprite.Group()
learn_sprites = pygame.sprite.Group()
game_process_sprites = pygame.sprite.Group()
pause_modal_sprites = pygame.sprite.Group()
end_modal_sprites = pygame.sprite.Group()
game_process_indicators = pygame.sprite.Group()
start_window()
# menu_window()
# levels_window()
# game_process_window()
groups = [start_window_sprites, menu_window_sprites,
          levels_window_sprites, game_process_sprites, pause_modal_sprites,
          end_modal_sprites, titres_sprites, records_sprites, learn_sprites,
          game_process_indicators]
if __name__ == '__main__':
    while running:
        visible = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if listen_text:
                    if input_data:
                        PLAYER = input_data
                    listen_text = False

            if event.type == pygame.MOUSEBUTTONUP:
                for group in groups:
                    for e in group:
                        if visible:
                            if e.__class__.__name__ in ["Button", "TextField"]:
                                res = e.get_event(event)
                                if res:
                                    visible = False

            if event.type == pygame.KEYDOWN:
                if listen_text:
                    data = pygame.key.name(event.key)
                    input_data += data

        for group in groups:
            group.update()
            group.draw(screen)
        clock.tick(constants.FPS)
        pygame.display.flip()
