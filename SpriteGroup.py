import pygame


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
