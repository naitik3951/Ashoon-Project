import pygame
pygame.init() #Initialize pygame

#Creating window
screenWidth = 1280
screenHeight = 720
win = pygame.display.set_mode((screenWidth, screenHeight)) #Width x Height in the tuple
pygame.display.set_caption("Ashoon game") #Naming the window

#Coordinates and velocity of char (attributes)
#Grid starts from top left (0,0)
x = 700
y = 360
width = 20
height = 60
vel = 10 #Velocity

isJump = False #For jumping
gravity = 10 #-Because vector, and - in physics is + here cus opposiute
airTime = 0.5 
jumpVelocity = -20

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

    if keys[pygame.K_a] and x > vel : #x > vel such that x - vel>0 so that we can never move off screen
        x -= vel
    if keys[pygame.K_d] and x < screenWidth - width - vel: #screenWidth so that not off screen and -width cus pygame has char position at top left, and we want it to look like it on screen, - vel for same reason as top
        x += vel
    if not(isJump): #Below action should not happen if jumping
        if keys[pygame.K_w] and y > vel:
            y -= vel
        if keys[pygame.K_s] and y < screenHeight - height - vel:
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        current_airTime = 0
        startY = 0
        s = (jumpVelocity * current_airTime) + 0.5 * gravity *  (current_airTime**2)
        current_airTime += 0.1
        y = startY + s
        if current_airTime >= airTime:
            isJump = False


    #Drawing character
    win.fill((0,0,0)) #Filling colour every loop so rectangle doesnt copy
    pygame.draw.rect(win, (128,0,128), (x , y, width, height)) #Win = surface, Color tupple in RGB, x and y are starting point, width and height are dimensions of rectangle  
    pygame.display.update() #Refresh display cus pygame needs it

pygame.quit()
