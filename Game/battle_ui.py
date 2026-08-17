import pygame


class BattleUI:
    def __init__(self, screen):
        self.screen = screen

        # Background
        self.background = pygame.image.load(
            "assets/bg/bgs_normal/bg_12.png"
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )

        # Enemy Pokémon
        self.enemy_sprite = pygame.image.load(
            "assets/monsters/goblin/goblin_idle.png"
        ).convert_alpha()

        self.enemy_sprite = pygame.transform.scale(
            self.enemy_sprite,
            (200, 200)
        )

    def handle_event(self, event):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Enemy battle platform
        pygame.draw.ellipse(
            self.screen,
            (40, 40, 40),
            (760, 300, 380, 100)
        )

        # Player battle platform
        pygame.draw.ellipse(
            self.screen,
            (40, 40, 40),
            (100, 500, 420, 110)
        )

        # Enemy Pokémon
        self.screen.blit(
            self.enemy_sprite,
            (850, 150)
        )