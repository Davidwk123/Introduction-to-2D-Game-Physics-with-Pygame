# vector.py
# David Welch Keliihoomalu
# 9/3/2023

# Vector class based off the The Vector Class Module assignment: https://pet.timetocode.org/

import math

class Vector:
    def __init__(self, x, y, int_flag = "not_int"):
        if(int_flag == "int"):
            self.x = int(round(x))
            self.y = int(round(y))
        else:
            self.x = float(x)
            self.y = float(y)

    def __str__(self):
        return "Vector({}, {})".format(self.x, self.y)
    
    def __add__(self, vector):
        x = self.x + vector.x 
        y = self.y + vector.y 
        return Vector(x, y)
    
    def addition(self, vector):
        x = self.x + vector.x 
        y = self.y + vector.y 
        return Vector(x, y)
    
    def __sub__(self, vector):
        x = self.x - vector.x 
        y = self.y - vector.y 
        return Vector(x, y)
    
    def subtraction(self, vector):
        x = self.x - vector.x 
        y = self.y - vector.y 
        return Vector(x, y)
    
    def __mul__(self, r):
        x = r * self.x
        y = r * self.y 
        return Vector(x, y)
    
    def multiplyFactor(self, vector, r):
        x = r * vector.x 
        y = r * vector.y 
        return Vector(x, y)
    
    def __div__(self, r):
        x = self.x / r
        y = self.y / r 
        return Vector(x, y)
    
    def divisionFactor(self, r):
        x = self.x / r
        y = self.y / r 
        return Vector(x, y)

    def equal(self, vector):
        if(self.x == vector.x and self.y == vector.y):
            return True
    
    def not_equal(self, vector):
         if(self.x != vector.x or self.y != vector.y):
            return True

    def dotProduct(self, vector, vectorTwo):
        x = vector.x * vectorTwo.x
        y = vector.y * vectorTwo.y 
        return x + y
    
    def projection(self, vector):
        a = self
        b = Vector(vector.x, vector.y)
        a_times_b = (self.dotProduct(a, b))
        b_times_b = self.dotProduct(b, b)
        if(b_times_b > 0):
            r_factor = (a_times_b/b_times_b)
            return b * r_factor
        else:
            return self * 0
    
    def length(self):
        return (self.x*self.x + self.y*self.y)**0.5
    
    def lengthSquared(self):
        return (self.x*self.x + self.y*self.y)
    
    def unitVector(self):
        return self/self.length()
    
    def set_magnitude(self, length):
        return self.unitVector() * length

    def rotate(self, degree, sameVector = False):
        x = self.x * math.cos(math.radians(degree)) - self.y * math.sin(math.radians(degree))
        y = self.x * math.sin(math.radians(degree)) + self.y * math.cos(math.radians(degree))
        if(sameVector == True):
            self.x = x
            self.y = x
            return self
        else:
            return Vector(x, y)
    
    def setAngle(self, degree):
        self = Vector(self.length(), 0)
        return self.rotate(degree)
    
    def getDegree(self):
        if (self.lengthSquared() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    
    def getAngleBetween(self, vector):
        cross = self.x*vector.y - self.y*vector.x 
        dot = self.x*vector.x + self.y*vector.y
        return math.degrees(math.atan2(cross, dot))
    
    def rotate90(self):
       return Vector(-self.y, self.x)
    
    def rotate180(self):
        return Vector(-self.x, -self.y)
    
    def tuple(self):
        return (self.x, self.y)



