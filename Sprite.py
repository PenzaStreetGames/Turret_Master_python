import pygame


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group, pos, size, image=None, game_controller=None):
        super().__init__(group)
        self.rect = pygame.Rect(*pos, *size)
        self.rect.center = pos
        self.rect.size = size
        self.center = [pos[0] + size[0] // 2, pos[1] + size[1] // 2]
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
        self.start_frame = game_controller.frames
        self.pos = pos
        self.size = size
        self.game_controller = game_controller

    def get_event(self, event):
        pass