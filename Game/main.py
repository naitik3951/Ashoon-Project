import pygame
from battle_ui import BattleUI


pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pokémon Battle")

clock = pygame.time.Clock()

ui = BattleUI(screen)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ui.handle_event(event)

    screen.fill((30, 30, 30))

    ui.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()