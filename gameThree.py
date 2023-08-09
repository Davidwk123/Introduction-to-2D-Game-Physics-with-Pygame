import pygame, time
from pygame.locals import *
from pygame.color import THECOLORS

class Screen:
    def __init__(self, width_px = 800, height_px = 200):
        self.width_px = width_px
        self.height_px = height_px
        self.screen = pygame.display.set_mode((self.width_px, self.height_px))
        self.updateRefresh()

    def updateTitle(self, mode):
        pygame.display.set_caption("mode: " + str(mode))
        self.title = ("mode: " + str(mode))
    
    def updateRefresh(self):
        pygame.display.flip()
        self.screen.fill(THECOLORS['black'])

class EventConversion:
    def __init__(self, screen_width_px, length_m = 10):
        self.screen_width_px = screen_width_px
        self.m_to_px = screen_width_px/length_m
        self.px_to_m = float(length_m)/screen_width_px

    def px_from_m(self, x_m):
        return int(round(x_m * self.m_to_px))
    
    def m_from_px(self, x_px):
        return float(x_px) * self.px_to_m
    
    def userInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit' 
                elif event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2

class Car:
    def __init__(self, color = THECOLORS['white'], left_px = 400, width_px = 25, speed_mps = 0.0):
        self.color = color
        self.width_px = width_px
        self.height_px = 75
        self.left_px = left_px
        self.top_px = screen.height_px - self.height_px
        self.speed_mps = speed_mps
        self.center_x_m = eventConversion.m_from_px(self.left_px + (self.width_px / 2))
        self.rect = pygame.Rect(self.left_px, self.top_px, self.width_px, self.height_px)
    
    def drawCar(self):
        self.rect.centerx = eventConversion.px_from_m(self.center_x_m)
        pygame.draw.rect(screen.screen, self.color, self.rect)
    
    def moveCar(self, dt_s):
        self.center_x_m += self.speed_mps * dt_s

class CarTrack:
    def __init__(self):
        self.cars = []

    def carMode(self, mode):
        self.cars = []
        screen.updateTitle(mode)
        if(mode == 1):
            self.cars.append(Car(THECOLORS['green'], left_px=0, speed_mps=.5))
            self.cars.append(Car(THECOLORS['red'], left_px=800, speed_mps=-1.0))
        elif(mode == 2):
            self.cars.append(Car(THECOLORS['green'], left_px=0, speed_mps=1.0))
            self.cars.append(Car(THECOLORS['orange'], left_px=0, speed_mps=1.5))  
            
        
def main():

    global screen, eventConversion, carTrack

    pygame.init()

    (width_px, height_px) = (800, 200)
    eventConversion = EventConversion(width_px, 10)
    screen = Screen(width_px, height_px)
    carTrack = CarTrack()

    carTrack.carMode(1)

    userDone = False
    clock = pygame.time.Clock()
    fps = 144.0

    while not userDone:
        screen.screen.fill(THECOLORS['black'])

        userInput = eventConversion.userInput()

        if(userInput == 'quit'):
            userDone = True
        elif(userInput == 1):
            carTrack.carMode(1)
        elif(userInput == 2):
            carTrack.carMode(2)

        dt_s = float(clock.tick(fps) * 1e-3)
        while dt_s > 0.0:
            deltaTime_s = min(dt_s, 1/fps)
            dt_s -= deltaTime_s
        
            for car in carTrack.cars:
                car.moveCar(deltaTime_s)  

        for car in carTrack.cars:
            car.drawCar()
        screen.updateRefresh()

main()
