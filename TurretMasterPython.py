import pygame

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Turret Master")


def render():
    screen.fill(pygame.Color("black"))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    render()
    pygame.display.flip()
