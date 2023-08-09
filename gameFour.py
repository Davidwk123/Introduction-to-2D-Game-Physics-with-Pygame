import pygame
from pygame.color import THECOLORS

class GameScreen:
    def __init__(self, width_px, height_px):
        self.width_px = width_px
        self.height_px = height_px
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
            
        
class Car:
    def __init__(self, color = THECOLORS['white'], left_px = 400, width_px = 25, v_mps = 0.0):
        self.color = color
        self.width_px = width_px
        self.height_px = 95
        self.left_px = left_px
        self.top_px = screen.height_px - self.height_px

        self.width_m = eventConversion.m_from_px(width_px)
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
        self.carCount = 0
        
    def moveCar(self, car, dt_s):
        dt_s = dt_s
        force_of_car_N = self.gravity_mps2 * car.m_kg + 0.0 + 0.0
        a_mps2 = force_of_car_N/car.m_kg
        f_v_mps = car.v_mps + a_mps2 * dt_s
        car.center_x_m += (f_v_mps + car.v_mps)/2 * dt_s
        car.v_mps = f_v_mps

        if car.name == 1:
            print("x_m: {:5.2f} v_mps: {:5.3f} dt_s: {:5.3f}".format(car.center_x_m, car.v_mps, dt_s))


    def trackCollision(self):
        for car in self.cars:
            car_right_m = car.center_x_m + eventConversion.m_from_px((car.width_px / 2))
            car_left_m = car.center_x_m - eventConversion.m_from_px((car.width_px / 2))
            rightWall_m = eventConversion.m_from_px(screen.width_px)
            leftWall_m = 0.0
            collision = False
            if(car_right_m > rightWall_m):
                overlap_m = car_right_m - rightWall_m
                # x_coll_m = car_right_m
                # x_coll_v = car.v_mps
                # self.x_wall_v = (x_coll_v**2 - 2.0 * self.a_mps2 * overlap_m)**0.5
                # self.x_coll_t = 2.0 * overlap_m/(x_coll_v + self.x_wall_v)
                # self.x_wall_v *= -1 * self.cr
                # self.x_bounce = self.x_wall_v * self.x_coll_t + (self.a_mps2 * self.x_coll_t**2)/2.0
                # if self.x_bounce > 0.0: self.x_bounce = 0.0
                # car.center_x_m -= overlap_m + self.x_bounce 
                # car.v_mps = self.x_wall_v + self.a_mps2 * self.x_coll_t
                collision = True
            if(car_left_m < leftWall_m):
                overlap_m = car_left_m
                collision = True
            if(collision == True):
                car.center_x_m -= overlap_m * 2
                car.v_mps *= -1 * self.cr
            else:
                pass

    def carMode(self, mode):
        self.cars = []
        screen.modeTitle(mode)
        self.carCount = 0
        if(mode == 1):
            self.gravity_mps2 = 0.0
            self.cars.append(Car(THECOLORS['green'], left_px=0, v_mps=.5))
            self.cars.append(Car(THECOLORS['red'], left_px=774, v_mps=-4.0))
        elif(mode == 2):
            self.gravity_mps2 = 0.0
            self.cars.append(Car(THECOLORS['green'], left_px=0, v_mps=1.0))
            self.cars.append(Car(THECOLORS['orange'], left_px=0, v_mps=1.5))  
        elif(mode == 3):
            self.gravity_mps2 = 9.8/3.0
            self.cr = 0.7
            self.cars.append(Car(THECOLORS['yellow'], left_px= 475, width_px= 25, v_mps=1.5))
            self.cars.append(Car(THECOLORS['red'], left_px=500,width_px= 50, v_mps=1.5)) 

def main():
    global screen, eventConversion, carTrack 

    pygame.init()

    width_px = 800
    height_px = 200
    screen = GameScreen(width_px, height_px)
    eventConversion = EventConversion(width_px, 10.0)
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

        dt_s = clock.tick(fps) * 1e-3
        while(dt_s > 0.0):
            deltaTime_s = min(dt_s, 1/fps)
            dt_s -= deltaTime_s
            for car in carTrack.cars:
                carTrack.moveCar(car, deltaTime_s)
                
        carTrack.trackCollision()
        for car in carTrack.cars:
            car.drawCar()
        screen.drawRefresh()
        
main()