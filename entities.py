import pygame

class physicsEntity:
    def __init__(self, game, e_type, pos, size): #Game as parameter so that naything in game is accesibly in this
        self.game = game
        self.type = e_type
        self.pos = list(pos) #Call list here and not above cus otherwise multiple entities at same spot, and we can mutate this
        self.size = size
        self.vel = [0,0]

    def update(self, movement = (0,0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) #How much movement per frame, this is like a vector

        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]   

    def render(self, surface):
        surface.blit(self.game.asesets["Player"], self.pos)