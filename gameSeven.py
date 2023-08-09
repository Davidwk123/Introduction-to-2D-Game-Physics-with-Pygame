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
        self.clients = {'local': Client()}

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.clients['local'].mouseButtonPressed = True
                (mouse1, mouse2, mouse3) = pygame.mouse.get_pressed()

                if(mouse1): self.clients['local'].mouseButton = 1
                elif(mouse2): self.clients['local'].mouseButton = 2
                elif(mouse3): self.clients['local'].mouseButton = 3
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clients['local'].mouseButtonPressed = False
                self.clients['local'].mouseButton = -1
        
class Car:
    def __init__(self, color = THECOLORS['white'], left_px = 10, width_px = 26, v_mps = 6.6):
        self.color = color
        self.width_px = width_px
        self.height_px = 98
        self.left_px = left_px
        self.top_px = screen.height_px - self.height_px

        self.width_m = eventConversion.m_from_px(width_px)
        self.halfWidth_m = self.width_m/2
        self.height_m = eventConversion.m_from_px(self.height_px)
        self.v_mps = v_mps
        self.density_kgpm2 = 600
        self.m_kg = self.width_m * self.height_m * self.density_kgpm2
        self.tetherForce_N = 0.0
        self.dragForce_N = 0.0
        self.center_x_m = eventConversion.m_from_px(self.left_px + (self.width_px / 2))

        carTrack.carCount += 1
        self.name = carTrack.carCount 
        self.carSelected = False
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
        force_of_car_N = (self.gravity_mps2 * car.m_kg) + (car.tetherForce_N + car.dragForce_N)
        
        a_mps2 = force_of_car_N/car.m_kg
        # if car.name == 1:
        #             print("carTop: {:1} carSelect: {:1} ").format(self.gravity_mps2, a_mps2) 
        f_v_mps = car.v_mps + (a_mps2 * dt_s)
        
        car.center_x_m += (f_v_mps + car.v_mps)/2.0 * dt_s
        car.v_mps = f_v_mps
        car.tetherForce_N = 0.0
        car.dragForce_N = 0.0

    def checkMousePosistion(self, mouseX, mouseY):
        for car in self.cars:
            carLeft_px = car.rect.centerx - car.width_px/2
            carRight_px = carLeft_px + car.width_px
            carTop_px = screen.height_px - car.height_px
            carBottom_px = carTop_px + car.height_px
            if((mouseX > carLeft_px and mouseX < carRight_px) and (mouseY > carTop_px and mouseY < carBottom_px)):
                    # print("carTop: {:2} ").format(mouseX) 
                car.carSelected = True
                return car
            
        return None 

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
                    # print("relative_v_mps: {:3.3f} car_v_mps: {:3.3f} nextCar_v: {:3.3f}").format(abs(car.v_mps - nextCar.v_mps), car.v_mps, nextCar.v_mps)
                 
    def carCollisionFormula(self, car, nextCar, CR=None):
        # print("nextCar_v_mps: {:4.1f} nextCar_m_kg: {:3.1f} car_m_kg: {:3.1f}").format(nextCar.v_mps, nextCar.m_kg, car.m_kg)
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
            self.cars.append(Car(THECOLORS['green'], left_px=0, v_mps=1.3))
            # self.cars.append(Car(THECOLORS['red'], left_px=774, v_mps=-4.0))
        elif(mode == 2):
            self.gravity_mps2 = 0.0
            self.cr = 1.0
            self.cars.append(Car(THECOLORS['green'], left_px=0, v_mps=-.5))
            self.cars.append(Car(THECOLORS['orange'], left_px=100, width_px=100, v_mps=5.0))  
        elif(mode == 3):
            self.gravity_mps2 = 9.8/3.0
            self.cr = 0.7
            self.cars.append(Car(THECOLORS['yellow'], left_px= 240, width_px= 26, v_mps=-.6))
            self.cars.append(Car(THECOLORS['red'], left_px=440,width_px= 50, v_mps=-.5)) 

class Client:
    def __init__(self):
        pass
        self.mouseButtonPressed = False
        self.carSelected = None
        self.mouseButton = -1
        self.tetherSettings = {'1':{'spring_k': 400.0, 'drag_cd': 13.3},
                               '2':{'spring_k': 13.3 , 'drag_cd':1.3},
                               '3':{'spring_k': 6666.6 , 'drag_cd': 133.3}
                               }
        # self.tetherSettings = {'1':{'spring_k': 60.0, 'drag_cd': 2.0},
        #                        '2':{'spring_k': 2.0 , 'drag_cd':.2},
        #                        '3':{'spring_k': 1000.0 , 'drag_cd': 20.0}
        #                        }

    def getMousePos(self):
        self.mousePosition = [self.mouseX, self.mouseY] = pygame.mouse.get_pos()
        self.mouseX_m = eventConversion.m_from_px(self.mouseX)
        self.mouseY_m = eventConversion.m_from_px(self.mouseY)
    
    def calc_tether_forces_on_cars(self):
        # for car in carTrack.cars:
        self.getMousePos()
        # carLeft_px = car.rect.centerx - car.width_px/2
        # carRight_px = carLeft_px + car.width_px
        # carTop_px = screen.height_px - car.height_px
        # carBottom_px = carTop_px + car.height_px
        # if car.name == 1:
        #     print("carTop: {:2} ").format(carBottom) 
        if(self.carSelected == None):
            if(self.mouseButtonPressed == True):
                self.carSelected = carTrack.checkMousePosistion(self.mouseX, self.mouseY)
        else:
            if(self.mouseButtonPressed == False):
                self.carSelected.carSelected = False
                self.carSelected = None
            else:
                # print("yes")
                mouseDisplacement = self.mouseX_m - self.carSelected.center_x_m 
                # if(self.mouseButton == 1): 
                #     tetherCoefficient = 3000.0
                #     dragCoefficient = 500.0
                # if(self.mouseButton == 2):
                #     tetherCoefficient = 600.0
                #     dragCoefficient = 60.0
                # if(self.mouseButton == 3): 
                #     tetherCoefficient = 100000.0
                #     dragCoefficient = 4000.0

                self.carSelected.tetherForce_N += self.tetherSettings[str(self.mouseButton)]['spring_k'] * mouseDisplacement
                self.carSelected.dragForce_N += -self.tetherSettings[str(self.mouseButton)]['drag_cd'] * self.carSelected.v_mps
                 

    def drawTetherLine(self):
        carMiddle_px = [self.carSelected.rect.centerx, self.carSelected.top_px + self.carSelected.height_px/2]
        # if(car.name == 1):
        #         print("carMid: {:2} mousePo : {:2}").format(carMiddle_px, self.mousePosition) 
        pygame.draw.line(screen.gameScreen, THECOLORS['green'], carMiddle_px, [self.mouseX,self.mouseY])


def main():
    global screen, eventConversion, carTrack

    pygame.init()

    width_px = 950
    height_px = 120
    
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
        for clientName in eventConversion.clients:
            eventConversion.clients[clientName].calc_tether_forces_on_cars()
        # client.calc_tether_forces_on_cars()
        while(dt_s > 0.0):
            deltaTime_s = min(dt_s, 1/fps)
            dt_s -= deltaTime_s
            for car in carTrack.cars:
                
                # if(car.name == 2):
                #     print("test: {:2} ").format(client.tetherForce) 
                carTrack.moveCar(car, deltaTime_s)
        # for car in carTrack.cars:
                
        #         # if(car.name == 2):
        #         #     print("test: {:2} ").format(client.tetherForce) 
        #         carTrack.moveCar(car, deltaTime_s)           
        carTrack.checkCollision()        
        # print("collisionCount: {:2} SC: {} collisionColorSwtich: {}").format(carTrack.collisionCount, carTrack.fixWallStickiness, carTrack.collisionColorSwitch) 
        
        for car in carTrack.cars:
            car.drawCar()

        for clientName in eventConversion.clients:
            if(eventConversion.clients[clientName].carSelected != None):
                eventConversion.clients[clientName].drawTetherLine()
        
        screen.drawRefresh()
        
main()