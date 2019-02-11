import pygame


class Sprite(pygame.sprite.Sprite):
    """Надстройка спрайта для игры"""

    def __init__(self, group, pos, size, image=None, game_controller=None):
        """Инициализация спрайта"""
        super().__init__(group)
        self.rect = pygame.Rect(*pos, *size)
        self.rect.center = pos
        self.rect.size = size
        self.center = [pos[0] + size[0] // 2, pos[1] + size[1] // 2]
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
        self.reserve_image = self.image
        self.start_frame = game_controller.frames
        self.pos = pos
        self.size = size
        self.game_controller = game_controller

    def get_event(self, event):
        """Не будем удалять, от греха подальше"""
        pass

    def set_image(self, image, pos, size):
        """Задание картинки спрайта"""
        self.center = [pos[0] + size[0] // 2, pos[1] + size[1] // 2]
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
        self.reserve_image = self.image
        self.pos = pos
        self.size = size
