import pygame
pygame.init() #Initialize pygame

#Creating window
screenWidth = 576
screenHeight = 324
win = pygame.display.set_mode((screenWidth, screenHeight)) #Width x Height in the tuple
pygame.display.set_caption("Ashoon game") #Naming the window

#Coordinates and velocity of char (attributes)
#Grid starts from top left (0,0)
x = 250
y = 180
width = 24
height = 48
vel = 5 #Velocity

#Variables for jumping
isJump = False #For jumping
gravity = 2400 #-Because vector, and - in physics is + here cus opposiute
airTime = 0.5 
jumpVelocity = -600

#Variables for animations
left = False
right = False
walkCount = 0

#Loading animations
sprite_sheet = pygame.image.load("assets/warrior_npc.png").convert_alpha()
walkLeft = []
walkRight = []
frameWidth = 24
frameHeight = 48

char = sprite_sheet.subsurface(pygame.Rect(32, 16, 24, 48))
bg = pygame.image.load("assets/bg_28.png")

for i in range(8):
    frame = sprite_sheet.subsurface(pygame.Rect(32 + (80 * i), 80, 24, 48)) #88,32 tell how many pixels to skip in the sprite sheet itself, same coord system as pygame, last 2 number are dimension of rectangle to cut out
    walkLeft.append(frame)
    frame_mirror = pygame.transform.flip(frame, True, False) #Surface, Flipx, Flipy
    walkRight.append(frame_mirror)

#Dont wanna draw anything in main loop
def redrawGameWindow():
    global walkCount
    #Drawing character

    win.blit(bg, (0,0)) #Blit helps us place images, bg is image and 0,0 is where to place it

    if walkCount + 1 >= 40:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount//5], (x,y)) #Walk count is for choosing which step and index frame according to it 
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//5], (x,y)) #x,y is for position of char
        walkCount += 1
    else:
        win.blit(char, (x,y))
    pygame.display.update() #Refresh display cus pygame needs it

clock = pygame.time.Clock() 

#Main movement loop
run = True
while run:
    dt = clock.tick(60)/1000  #/1000 to convert ms to s, this is frame rate

    #Event = what we do
    for event in pygame.event.get(): #To get events from user
        if event.type == pygame.QUIT: #Big red button is quit
            run = False

    #Checking event of movement in diff loop so that if we hold key it continues to move, if in above loop, it will only move once per press
    keys = pygame.key.get_pressed() #List of keys pressed
    #As we go left, x increase, as we go down, y increases
    
    if keys[pygame.K_a] and x > vel : #x > vel such that x - vel>0 so that we can never move off screen
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_d] and x < screenWidth - width - vel: #screenWidth so that not off screen and -width cus pygame has char position at top left, and we want it to look like it on screen, - vel for same reason as top
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    if not(isJump): #Below action should not happen if jumping
        if keys[pygame.K_SPACE]:
            isJump = True
            current_airTime = 0
            startY= y
            velY = -600 #Velocity y

            left = False
            right = False
            walkCount =  0
    else:
        current_airTime += 0.02
        s = (jumpVelocity * current_airTime) + 0.5 * gravity *  (current_airTime**2)
        y = startY + s
        if current_airTime >= airTime:
            isJump = False
            current_airTime = 0

    redrawGameWindow()
    
pygame.quit()
