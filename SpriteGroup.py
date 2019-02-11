import pygame


class SpriteGroup(pygame.sprite.Group):
    """Надстройка группы спрайтов для игры"""

    def __init__(self):
        """Инициализация группы"""
        super().__init__()

    def get_my_event(self, event):
        """Проверка собственных событий"""
        if event == "check_death":
            for sprite in self:
                sprite.check_death()

    def get_event(self, event):
        """Проверка общих событий"""
        for sprite in self:
            sprite.get_event(event)
