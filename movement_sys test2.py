import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        screenWidth = 1920
        screenHeight = 1080
        pygame.display.set_caption("Ashoon Project")
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()

        #Background
        self.clouds_1 = pygame.image.load("assets/night_1/night_1_1.png")
        self.cloud_1_pos = [0,0]

        self.clouds_2 = pygame.image.load("assets/night_1/night_1_2.png")
        self.cloud_2_pos = [0,0]

        self.mountain_1 = pygame.image.load("assets/night_1/night_1_3.png")
        self.mountain_1_pos = [0,0]

        self.mountain_2 = pygame.image.load("assets/night_1/night_1_4.png")
        self.mountain_2_pos = [0,0]

        self.mountain_3 = pygame.image.load("assets/night_1/night_1_5.png")
        self.mountain_3_pos = [0,0]

        self.grass_1 = pygame.image.load("assets/night_1/night_1_6.png")
        self.grass_1_pos = [0,0]

        self.sky_1 = pygame.image.load("assets/night_1/night_1_7.png")
        self.sky_1_pos = [0,0]

        self.sky_2 = pygame.image.load("assets/night_1/night_1_8.png")
        self.sky_2_pos = [0,0]

    def draw_background(self):
        self.win.blit(self.sky_1, self.sky_1_pos)
        self.win.blit(self.sky_2, self.sky_2_pos)

        self.win.blit(self.clouds_1, self.cloud_1_pos)
        self.win.blit(self.clouds_2, self.cloud_2_pos)

        self.win.blit(self.mountain_1, self.mountain_1_pos)
        self.win.blit(self.mountain_2, self.mountain_2_pos)
        self.win.blit(self.mountain_3, self.mountain_3_pos)

        self.win.blit(self.grass_1, self.grass_1_pos)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #Exit application

            self.draw_background()

            pygame.display.update()
            self.clock.tick(60)

Game().run()
