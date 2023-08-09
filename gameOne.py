import sys, pygame, math
pygame.init()

screen = pygame.display.set_mode((400, 400))

color = (127,255,0)
color2 = (102,205,170)
color3 = (50,205,50)

clock = pygame.time.Clock()

fps = 10
timeS = 0.0
eraseCheck = False
updateCheck = False
mouseCheck = False
while True:
    dtS = float(clock.tick(fps) * 1e-3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                eraseCheck = True
            elif event.key == pygame.K_f:
                updateCheck = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                eraseCheck = False
            elif event.key == pygame.K_f:
                updateCheck = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseCheck = True
            (mouse1, mouse2, mouse3) = pygame.mouse.get_pressed()

            if(mouse1): mouseButton = 1
            elif(mouse2): mouseButton = 2
            elif(mouse3): mouseButton = 3
            else: mouseButton = 4
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseCheck = False

    mousex, mousey = pygame.mouse.get_pos()
    

    if(eraseCheck == True): 
        screen.fill((0,0,0))

    if(mouseCheck == True and mouseButton == 1):
        pygame.draw.circle(screen, color2, (mousex,mousey), 10)
    elif(mouseCheck == True and mouseButton == 3):
        pygame.draw.circle(screen, color3, (mousex,mousey), 10)
    else:
        pygame.draw.circle(screen, color, (mousex,mousey), 10)

    timeS += dtS

    print(timeS, dtS, clock.get_fps())

    if(updateCheck != True):
        pygame.display.flip()


    