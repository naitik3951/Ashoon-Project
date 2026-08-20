import sys
import pygame

from pygame_scripts.entities import physicsEntity

class Game:
    def __init__(self):
        pygame.init()
        screenWidth = 1920
        screenHeight = 1080
        pygame.display.set_caption("Ashoon Project")
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()


        self.player = physicsEntity(self, "player", (50,50), (8,15))
        self.movement = [False, False]

        #Collision
        self.collision_area = pygame.Rect(50,50, 100,200)

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
            self.win.fill((0,0,0)) 

            self.player.update((self.movement[1] - self.movement[0]) * 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #Exit application

                #Self movement tracks if key is held down or not
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement_x[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement_x[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement_x[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement_x[1] = False
                    
            pygame.display.update()
            self.clock.tick(60)

Game().run()