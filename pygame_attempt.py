import pygame
pygame.init() #Initialize pygame

#Creating window
win = pygame.display.set_mode((1280,720)) #Width x Height in the tuple
pygame.display.set_caption("Ashoon game") #Naming the window

#Coordinates and velocity of char (attributes)
#Grid starts from top left (0,0)
x = 50
y = 50
width = 20
height = 60
vel = 5 #Velocity

#Main loop
run = True
while run:
    pygame.time.delay(100) #So not too fast, 100ms

    #Event = what we do
    for event in pygame.event.get(): #To get events from user
        if event.type == pygame.QUIT: #Big red button is quit
            run = False

    #Checking event of movement in diff loop so that if we hold key it continues to move, if in above loop, it will only move once per press
    keys = pygame.key.get_pressed() #List of keys pressed
    #As we go left, x increase, as we go down, y increases

    if keys[pygame.K_a]:
        x -= vel
    if keys[pygame.K_d]:
        x += vel
    if keys[pygame.K_w]:
        y -= vel
    if keys[pygame.K_s]:
        y += vel

    #Drawing character
    win.fill((0,0,0)) #Filling colour every loop so rectangle doesnt copy
    pygame.draw.rect(win, (128,0,128), (x , y, width, height)) #Win = surface, Color tupple in RGB, x and y are starting point, width and height are dimensions of rectangle  
    pygame.display.update() #Refresh display cus pygame needs it

pygame.quit()