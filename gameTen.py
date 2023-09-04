# gameTen.py
# David Welch Keliihoomalu
# 9/3/2023

# 2D-Physics Engine Framework assignment: https://pet.timetocode.org/

import sys, os
import pygame
import math

from pygame.locals import *
from pygame.color import THECOLORS

from vector import Vector

class GameWindow():
    def __init__(self, window_size_px, title):
        self.width_px = window_size_px[0]
        self.height_px = window_size_px[1]
        self.width_m = enviornment.m_from_px(self.width_px)
        self.height_m = enviornment.m_from_px(self.height_px)  
        self.title = title
        self.gameScreen = pygame.display.set_mode((self.width_px, self.height_px))
        self.refreshUpdate()

    def set_title(self, mode):
        pygame.display.set_caption(self.title + "Mode: " + str(mode))

    def refreshUpdate(self):
        pygame.display.flip()
        self.gameScreen.fill(THECOLORS["black"])
        
class Enviornment():
    # used for conversions between meters and pixels, and gets user input 
    def __init__(self, screenSize_px, length_m):
        self.screenSize_px = Vector(screenSize_px[0], screenSize_px[1])
        # offset used to help convert coords between meters and pixels
        self.screenOffset_px = Vector(0,0)

        self.m_to_px = float(self.screenSize_px.x)/length_m
        self.px_to_m = length_m/float(self.screenSize_px.x)

        self.freeze = False

        self.cursor_location_m = Vector(0,0)
        self.mouseButton = 1
        self.mousePressed = False

        self.dt_s = 0

    def px_from_m(self, value_m):
        return value_m * self.m_to_px
    
    def m_from_px(self, value_px):
        return float(value_px) * self.px_to_m  
    
    # converts pixel coords into meters 
    def m_from_px_coord(self, coord_px):
        value_x_m = (coord_px.x + self.screenOffset_px.x) / (self.m_to_px)
        value_y_m = (self.screenSize_px.y - coord_px.y + self.screenOffset_px.y) / (self.m_to_px)
        return Vector(value_x_m, value_y_m)
    
    # converts meter coords into pixels 
    def px_from_m_coord(self, coord_m):
        value_x_px = (coord_m.x * self.m_to_px) - self.screenOffset_px.x
        value_y_px = (coord_m.y * self.m_to_px) - self.screenOffset_px.y
        value_y_px = self.screenSize_px.y - value_y_px 
        return Vector(value_x_px, value_y_px, "int").tuple()
    
    def getUserInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_f:
                    self.freeze = not self.freeze
                    if(self.freeze):
                        airTable.gravityVector_m = airTable.gravityVector_m.set_magnitude(0)
                        airTable.stop_puck()
                    else:
                        airTable.gravityVector_m.y = -airTable.gravity_mps2
                elif event.key == pygame.K_s:
                    airTable.stickinessCorrection = not airTable.stickinessCorrection
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePressed = True
                (mouse1, mouse2, mouse3) = pygame.mouse.get_pressed()

                if(mouse1): self.mouseButton = 1
                elif(mouse2): self.mouseButton = 2
                elif(mouse3): self.mouseButton = 3
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mousePressed = False
      
        self.cursor_location_m = enviornment.m_from_px_coord(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))   

class Puck():
    def __init__(self, color, locationVector_m, radius_m=0.5, v_mps=0.0):
        # baseVector_m used to set vectors to an intial position on the screen(bottom left)
        self.baseVector_m = Vector(0,0)
        self.position_vector_m = self.baseVector_m + Vector(locationVector_m.x,locationVector_m.y)
        self.color = color
        self.v_mps = v_mps
        self.v_vector_m = Vector(v_mps, 0.0)
        self.radius_m = radius_m
        self.selected = False

        self.density_kgpm2 = .3
        self.m_kg = self.density_kgpm2 * (math.pi * self.radius_m**2)

        self.drag_vector_m = Vector(0,0)
        self.spring_vector_m = Vector(0,0)
        
    def drawPuck(self):
        radius_px = int(round(enviornment.px_from_m(self.radius_m)))
        puck_line_thickness = 1
        pygame.draw.circle(gameWindow.gameScreen, self.color, (enviornment.px_from_m_coord(self.position_vector_m)), radius_px, puck_line_thickness)

class AirTable():
    # applies forces/movement/collisions to all pucks and sets demo modes 
    def __init__(self):
        self.pucks = []
        self.walls_m = {'left': 0.0, 'right': gameWindow.width_m,
                               'bottom':  0.0, 'top':  gameWindow.height_m}
        self.baseGravity_mps2 = 9.8
        self.gravity_mps2 = self.baseGravity_mps2/2.0
        self.gravityVector_m = Vector(0.0, -self.gravity_mps2)
        # collision restitution
        self.cr = 1.0
        self.stickinessCorrection = True

    def move_puck(self, puck):
        force_vector_m = (self.gravityVector_m * puck.m_kg) + (puck.drag_vector_m + puck.spring_vector_m)
        a_vector_m = force_vector_m / puck.m_kg
        puck.v_vector_m = puck.v_vector_m + (a_vector_m * enviornment.dt_s)
        puck.position_vector_m = puck.position_vector_m + (puck.v_vector_m  * enviornment.dt_s)
        puck.spring_vector_m = Vector(0,0)
        puck.drag_vector_m = Vector(0,0)

    def stop_puck(self):
        for puck in self.pucks:
            puck.v_vector_m = Vector(0,0)

    def check_collision(self):
        for i, puck in enumerate(self.pucks):
            # top and bottom collisions 
            if((puck.position_vector_m.y - puck.radius_m) < self.walls_m['bottom'] or (puck.position_vector_m.y + puck.radius_m) > self.walls_m['top']):
                bottom_difference_m = (puck.position_vector_m.y - puck.radius_m) - self.walls_m['bottom']
                top_difference_m = (puck.position_vector_m.y + puck.radius_m) - self.walls_m['top']

                if(self.stickinessCorrection == True):
                    if((puck.position_vector_m.y - puck.radius_m) < self.walls_m['bottom']):
                        puck.position_vector_m.y -= bottom_difference_m * 2
                    
                    if((puck.position_vector_m.y + puck.radius_m) > self.walls_m['top']):
                        puck.position_vector_m.y -= top_difference_m * 2
            
                puck.v_vector_m.y *= -self.cr

            # left and right collisions 
            if((puck.position_vector_m.x - puck.radius_m) < self.walls_m['left'] or (puck.position_vector_m.x + puck.radius_m) > self.walls_m['right']):
                left_difference_m = (puck.position_vector_m.x - puck.radius_m) - self.walls_m['left']
                right_difference_m = (puck.position_vector_m.x + puck.radius_m) - self.walls_m['right']

                if(self.stickinessCorrection == True):
                    if((puck.position_vector_m.x - puck.radius_m) < self.walls_m['bottom']):
                        puck.position_vector_m.x -= left_difference_m * 2
                    
                    if((puck.position_vector_m.x + puck.radius_m) > self.walls_m['top']):
                        puck.position_vector_m.x -= right_difference_m * 2
            
                puck.v_vector_m.x *= -self.cr
            
            # puck on puck collisions 
            for nextPuck in self.pucks[i+1:]:
                # get normal and tangential length(difference) between pucks 
                normal_difference_vector_m = puck.position_vector_m - nextPuck.position_vector_m
                tangent_difference_vector_m = normal_difference_vector_m.rotate90()
                # squared used to improve speed of program
                difference_m2 = normal_difference_vector_m.lengthSquared()
                radius_sum_m2 = (puck.radius_m+nextPuck.radius_m)**2
                # if pucks intersect
                if(difference_m2 < radius_sum_m2):
                    # project velocity vectors of each puck onto the difference vectors so that new vectors are pointing in the same direction 
                    normal_v_vector_m = puck.v_vector_m.projection(normal_difference_vector_m)
                    tangent_v_vector_m = puck.v_vector_m.projection(tangent_difference_vector_m)

                    other_normal_v_vector_m = nextPuck.v_vector_m.projection(normal_difference_vector_m)
                    other_tangent_v_vector_m = nextPuck.v_vector_m.projection(tangent_difference_vector_m)

                    relative_v_vector_m = normal_v_vector_m - other_normal_v_vector_m
    
                    if(self.stickinessCorrection == True):
                        relative_v_mps = relative_v_vector_m.length()
                        pen_m = (puck.radius_m+nextPuck.radius_m)**0.5 - difference_m2**0.5
                        # avoids division by 0 error 
                        if(relative_v_mps > 0.0000001):
                            pen_s = pen_m/relative_v_mps

                            puck.position_vector_m -= normal_v_vector_m * pen_s
                            nextPuck.position_vector_m -= other_normal_v_vector_m * pen_s

                            after_normal_v_vector_m, after_other_normal_v_vector_m = self.puck_collision_formula(normal_v_vector_m, other_normal_v_vector_m, puck, nextPuck, CR=1.0)
                            
                            puck.position_vector_m += after_normal_v_vector_m * pen_s
                            nextPuck.position_vector_m += after_other_normal_v_vector_m * pen_s

                    after_normal_v_vector_m, after_other_normal_v_vector_m = self.puck_collision_formula(normal_v_vector_m, other_normal_v_vector_m, puck, nextPuck)
                    
                    puck.v_vector_m = after_normal_v_vector_m + tangent_v_vector_m
                    nextPuck.v_vector_m = after_other_normal_v_vector_m + other_tangent_v_vector_m

    # calculates new velocity vectors for collided pucks              
    def puck_collision_formula(self, before_normal_v_vector_m, before_other_normal_v_vector_m, puck, nextPuck, CR=None):
        if(CR == None):
            CR = self.cr 

        puck_f_v_vector_m = ((before_other_normal_v_vector_m - before_normal_v_vector_m) * (CR * nextPuck.m_kg)  +  (before_normal_v_vector_m * puck.m_kg  + before_other_normal_v_vector_m * nextPuck.m_kg) )/(puck.m_kg  + nextPuck.m_kg)   
        
        nextPuck_f_v_vector_m = ((before_normal_v_vector_m - before_other_normal_v_vector_m) * (CR * puck.m_kg)  +  (before_normal_v_vector_m * puck.m_kg  + before_other_normal_v_vector_m * nextPuck.m_kg) )/(puck.m_kg  + nextPuck.m_kg)
                       
        return (puck_f_v_vector_m, nextPuck_f_v_vector_m)


    def puck_modes(self, mode):
        self.pucks = []
        gameWindow.set_title(mode)
        if(mode == 1):
            self.cr = .5
            self.gravityVector_m.y = -self.gravity_mps2
            self.pucks.append(Puck(THECOLORS['white'], Vector(2,4)))
            self.pucks.append(Puck(THECOLORS['red'], Vector(2,2)))

class TetherForces():
    # used to apply drag and spring forces when user clicks and moves a puck 
    def __init__(self):
        self.puckSelected = None
        self.tetherSettings = {'spring_k': 60.0 , 'drag_cd': 2.0}

    def cursor_in_puck(self):
        for puck in airTable.pucks:
            normal_difference_vector_m = enviornment.cursor_location_m - puck.position_vector_m
            difference_m = normal_difference_vector_m.lengthSquared()
            if(difference_m < puck.radius_m**2):
                puck.selected = True
                return puck
        return None
    
    def apply_tether_forces(self):
        if(self.puckSelected == None):
            if(enviornment.mousePressed == True):
                self.puckSelected = self.cursor_in_puck()
        else:
            if(enviornment.mousePressed == False):
                self.puckSelected.selected = False
                self.puckSelected = None
            else:
                normal_difference_vector_m = enviornment.cursor_location_m - self.puckSelected.position_vector_m
                
                self.puckSelected.spring_vector_m += normal_difference_vector_m * self.tetherSettings['spring_k'] 
                self.puckSelected.drag_vector_m += self.puckSelected.v_vector_m * -self.tetherSettings['drag_cd']
                 
    def draw_tether_line(self, puck):
        position_px = enviornment.px_from_m_coord(puck.position_vector_m)
        cursor_location_px = enviornment.px_from_m_coord(enviornment.cursor_location_m)
        pygame.draw.line(gameWindow.gameScreen, THECOLORS['green'], position_px, cursor_location_px)

def main():
    global enviornment, gameWindow, airTable

    pygame.init()

    myclock = pygame.time.Clock()
    fps = 60.0

    window_size_px = (800, 700)

    enviornment = Enviornment(window_size_px, 10.0)
    gameWindow = GameWindow(window_size_px, "2D-Physics Engine Framework: ")
    tetherForces = TetherForces()

    airTable = AirTable()
    airTable.puck_modes(1)

    while True:
        enviornment.dt_s = float(myclock.tick(fps) * 1e-3)
        userInput = enviornment.getUserInput()

        if(userInput == 1):
            airTable.puck_modes(1)
        tetherForces.apply_tether_forces()
        for puck in airTable.pucks:
            airTable.move_puck(puck)
        airTable.check_collision()

        for puck in airTable.pucks:
            puck.drawPuck()
            if(puck.selected == True):
                tetherForces.draw_tether_line(puck)
        
        gameWindow.refreshUpdate() 

main()