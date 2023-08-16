import math

class Vector:
    def __init__(self, x, y):
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
        x = r / self.x
        y = r / self.y 
        return Vector(x, y)
    
    def divisionFactor(self, r):
        x = r / self.x
        y = r / self.y 
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
        r_factor = (a_times_b/b_times_b)
        return b * r_factor
    
    def length(self):
        return (self.x**2 + self.y**2)**0.5
    
    def lengthSquared(self):
        return (self.x**2 + self.y**2)
    
    def unitVector(self):
        return self/self.length()
    
    def set_magnitude(self, length):
        self.unitVector() * length

    def rotate(self, degree):
        x = self.x * math.cos(math.radians(degree)) - self.y * math.sin(math.radians(degree))
        y = self.x * math.sin(math.radians(degree)) + self.y * math.cos(math.radians(degree))
        return Vector(x, y)
    
    def rotate90(self):
        x = self.x * math.cos(math.radians(90)) - self.y * math.sin(math.radians(90))
        y = self.x * math.sin(math.radians(90)) + self.y * math.cos(math.radians(90))
        return Vector(x, y)
    
    def rotate180(self):
        x = self.x * math.cos(math.radians(180)) - self.y * math.sin(math.radians(180))
        y = self.x * math.sin(math.radians(180)) + self.y * math.cos(math.radians(180))
        return Vector(x, y)



