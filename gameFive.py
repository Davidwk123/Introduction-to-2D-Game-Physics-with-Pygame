import pygame
from pygame.color import THECOLORS

class GameScreen:
    def __init__(self, width_px, height_px):
        self.width_px = width_px
        self.height_px = height_px
        self.leftWall_m = 0.0
        self.rightWall_m = eventConversion.m_from_px(width_px)
        self.gameScreen = pygame.display.set_mode((width_px, height_px))

        self.drawRefresh()
    
    def modeTitle(self, mode):
        pygame.display.set_caption("Mode: " + str(mode))
        self.title = "Mode: " + str(mode)
    
    def drawRefresh(self):
        pygame.display.flip()
        self.gameScreen.fill(THECOLORS['black'])

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
                elif event.key == pygame.K_3:
                    return 3
                elif event.key == pygame.K_s:
                    return 's'
                elif event.key == pygame.K_c:
                    return 'c'
        
class Car:
    def __init__(self, color = THECOLORS['white'], left_px = 400, width_px = 25, v_mps = 0.0):
        self.color = color
        self.width_px = width_px
        self.height_px = 95
        self.left_px = left_px
        self.top_px = screen.height_px - self.height_px

        self.width_m = eventConversion.m_from_px(width_px)
        self.halfWidth_m = self.width_m/2
        self.height_m = eventConversion.m_from_px(self.height_px)
        self.v_mps = v_mps
        self.density_kgpm2 = 600
        self.m_kg = self.width_m * self.height_m * self.density_kgpm2
        self.center_x_m = eventConversion.m_from_px(self.left_px + (self.width_px / 2))

        carTrack.carCount += 1
        self.name = carTrack.carCount 
        self.rect = pygame.Rect(self.left_px, self.top_px, self.width_px, self.height_px)
    
    def drawCar(self):
        self.rect.centerx = eventConversion.px_from_m(self.center_x_m)
        pygame.draw.rect(screen.gameScreen, self.color, self.rect)

class CarTrack:
    def __init__(self, gravity_mps2 = 9.8/3.0, collisionR = 1.0):
        self.cars = []
        self.gravity_mps2 = gravity_mps2
        self.cr = collisionR
        self.fixCarStickiness = True
        self.fixWallStickiness = True
        self.collisionColorSwitch = False
        self.collisionCount = 0
        self.carCount = 0
        
    def moveCar(self, car, dt_s):
        force_of_car_N = self.gravity_mps2 * car.m_kg + 0.0 + 0.0
        a_mps2 = force_of_car_N/car.m_kg
        f_v_mps = car.v_mps + (a_mps2 * dt_s)
        car.center_x_m += (f_v_mps + car.v_mps)/2.0 * dt_s
        car.v_mps = f_v_mps

    def checkCollision(self):
        for i, car in enumerate(self.cars):
            car_right_m = car.center_x_m + car.halfWidth_m
            car_left_m = car.center_x_m - car.halfWidth_m
           
            if((car_right_m > screen.rightWall_m) or (car_left_m < screen.leftWall_m)):
                if(self.fixWallStickiness == True):
                    self.wallStickinessCorrection(car, car_left_m, car_right_m)
                car.v_mps = -car.v_mps * self.cr
                self.collisionCount += 1

            for nextCar in self.cars[i+1:]:
                if(abs(car.center_x_m - nextCar.center_x_m) < (car.halfWidth_m + nextCar.halfWidth_m)):
                    if(self.fixCarStickiness == True):
                        self.carStickinessCorrection(car, nextCar)
                    if(self.collisionColorSwitch == True): 
                        carColor = car.color 
                        car.color = nextCar.color 
                        nextCar.color = carColor
                    (car.v_mps, nextCar.v_mps) = self.carCollisionFormula(car, nextCar)
                    self.collisionCount += 1
                         
    def carCollisionFormula(self, car, nextCar, CR=None):
        if(CR == None):
            CR = self.cr 
        car_f_v_mps = (CR * nextCar.m_kg * (nextCar.v_mps - car.v_mps) 
                     + car.m_kg * car.v_mps + nextCar.m_kg * nextCar.v_mps)/(car.m_kg  + nextCar.m_kg)                    
        nextCar_f_v_mps = (CR * car.m_kg * (car.v_mps - nextCar.v_mps) 
                     + car.m_kg * car.v_mps + nextCar.m_kg * nextCar.v_mps)/(car.m_kg  + nextCar.m_kg) 
        
        return (car_f_v_mps, nextCar_f_v_mps)
           
    def carStickinessCorrection(self, car, nextCar):
        relative_v_mps = abs(car.v_mps - nextCar.v_mps)
        
        overlap_m = (car.halfWidth_m + nextCar.halfWidth_m) - abs(car.center_x_m - nextCar.center_x_m)
        t_pen = overlap_m/relative_v_mps

        car.center_x_m -= car.v_mps * t_pen 
        nextCar.center_x_m -= nextCar.v_mps * t_pen
        (adjustedCar_v_mps, adjustedNextCar_v_mps) = self.carCollisionFormula(car, nextCar, 1.0)
        car.center_x_m += adjustedCar_v_mps * t_pen 
        nextCar.center_x_m += adjustedNextCar_v_mps * t_pen

    def wallStickinessCorrection(self, car, car_left_m, car_right_m):
        if(car_left_m < screen.leftWall_m):
            overlap_m = car_left_m
        elif(car_right_m > screen.rightWall_m):
            overlap_m = car_right_m - screen.rightWall_m
        
        car.center_x_m -= overlap_m * 2

    def carMode(self, mode):
        self.cars = []
        screen.modeTitle(mode)
        self.carCount = 0
        self.collisionCount = 0
        if(mode == 1):
            self.gravity_mps2 = 0.0
            self.cr = 1.0
            self.cars.append(Car(THECOLORS['green'], left_px=0, v_mps=.5))
            self.cars.append(Car(THECOLORS['red'], left_px=774, v_mps=-4.0))
        elif(mode == 2):
            self.gravity_mps2 = 0.0
            self.cr = 1.0
            self.cars.append(Car(THECOLORS['green'], left_px=0, v_mps=-.5))
            self.cars.append(Car(THECOLORS['orange'], left_px=100, width_px=100, v_mps=5.0))  
        elif(mode == 3):
            self.gravity_mps2 = 9.8/3.0
            self.cr = 0.7
            self.cars.append(Car(THECOLORS['yellow'], left_px= 300, width_px= 25, v_mps=1.0))
            self.cars.append(Car(THECOLORS['red'], left_px=200,width_px= 50, v_mps=.5)) 

def main():
    global screen, eventConversion, carTrack 

    pygame.init()

    width_px = 800
    height_px = 200
    
    eventConversion = EventConversion(width_px, 10.0)
    screen = GameScreen(width_px, height_px)
    carTrack = CarTrack(collisionR=1.0)

    carTrack.carMode(1)
    clock = pygame.time.Clock()
    fps = 60.0
    userDone = False

    while not userDone:
        userInput = eventConversion.userInput()
        if(userInput == 'quit'):
            userDone = True
        elif(userInput == 1):
            carTrack.carMode(1)
        elif(userInput == 2):
            carTrack.carMode(2)
        elif(userInput == 3):
            carTrack.carMode(3)
        elif(userInput == 's'):
            carTrack.fixCarStickiness = not carTrack.fixCarStickiness
            carTrack.fixWallStickiness = not carTrack.fixWallStickiness
        elif(userInput == 'c'):
            carTrack.collisionColorSwitch = not carTrack.collisionColorSwitch

        dt_s = clock.tick(fps) * 1e-3
        while(dt_s > 0.0):
            deltaTime_s = min(dt_s, 1/fps)
            dt_s -= deltaTime_s
            for car in carTrack.cars:
                carTrack.moveCar(car, deltaTime_s)
                    
        carTrack.checkCollision()        
        print("collisionCount: {:2} SC: {} collisionColorSwtich: {}").format(carTrack.collisionCount, carTrack.fixWallStickiness, carTrack.collisionColorSwitch) 
        
        for car in carTrack.cars:
            car.drawCar()
        screen.drawRefresh()
        
main()