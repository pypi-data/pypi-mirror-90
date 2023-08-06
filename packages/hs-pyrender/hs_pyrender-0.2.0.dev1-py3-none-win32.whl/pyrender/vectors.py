import math
import numpy as np
from ctypes import Structure, c_int

class Vector2:
    # Variabls
    x = float()
    y = float()

    # Methods
    def __init__(self, x: float=0, y: float=0):
        self.x = x
        self.y = y

    # Math
    def __add__(self, other):
        v = Vector2()

        if type(other) == int or type(other) == float or type(other) == np.int or type(other) == np.float:
            v.x = self.x + other
            v.y = self.y + other

        elif type(other) == tuple or type(other) == list or type(other) == np.ndarray:
            v.x = self.x + other[0]
            v.y = self.y + other[1]

        elif type(other) == Vector2:
            v.x = self.x + other.x
            v.y = self.y + other.y

        else:
            v.x = self.x
            v.y = self.y

        return v

    def __iadd__(self, other):
        if type(other) == int or type(other) == float or type(other) == np.int or type(other) == np.float:
            self.x += other
            self.y += other

        elif type(other) == tuple or type(other) == list or type(other) == np.ndarray:
            self.x += other[0]
            self.y += other[1]

        elif type(other) == Vector2:
            self.x += other.x
            self.y += other.y

        return self
    
    def __sub__(self, other):
        v = Vector2()

        if type(other) == int or type(other) == float or type(other) == np.int or type(other) == np.float:
            v.x = self.x - other
            v.y = self.y - other

        elif type(other) == tuple or type(other) == list or type(other) == np.ndarray:
            v.x = self.x - other[0]
            v.y = self.y - other[1]

        elif type(other) == Vector2:
            v.x = self.x - other.x
            v.y = self.y - other.y

        else:
            v.x = self.x
            v.y = self.y

        return v

    def __isub__(self, other):
        if type(other) == int or type(other) == float or type(other) == np.int or type(other) == np.float:
            self.x -= other
            self.y -= other

        elif type(other) == tuple or type(other) == list or type(other) == np.ndarray:
            self.x -= other[0]
            self.y -= other[1]

        elif type(other) == Vector2:
            self.x -= other.x
            self.y -= other.y

        return self
    
    def __mul__(self, other):
        v = Vector2()

        if type(other) == int or type(other) == float or type(other) == np.int or type(other) == np.float:
            v.x = self.x * other
            v.y = self.y * other

        elif type(other) == tuple or type(other) == list or type(other) == np.ndarray:
            other = np.array(other)

            if other.shape == (2, 2):
                v.x = self.x*other[0][0] + self.y*other[0][1]
                v.x = self.x*other[1][0] + self.y*other[1][1]

            elif other.shape == (2,):
                return self.x*other[0] + self.y*other[1]

            else:
                v.x = self.x
                v.y = self.y

        elif type(other) == Vector2:
            return self.x*other.x + self.y*other.y

        else:
            v.x = self.x
            v.y = self.y

        return v

    def __imul__(self, other):
        if type(other) == int or type(other) == float or type(other) == np.int or type(other) == np.float:
            self.x *= other
            self.y *= other

        elif type(other) == tuple or type(other) == list or type(other) == np.ndarray:
            other = np.array(other)

            if other.shape == (2, 2):
                self.x = self.x*other[0][0] + self.y*other[0][1]
                self.y = self.x*other[1][0] + self.y*other[1][1]

            elif other.shape == (2,):
                return self.x*other[0] + self.y*other[1]

            else:
                return self

        elif type(other) == Vector2:
            return self.x*other.x + self.y*other.y

        return self

    def scale(self, scaler):
        self.x *= scaler
        self.y *= scaler

    def normalize(self):
        angle = self.angle_x()
        self.x = math.sin(angle)
        self.y = math.cos(angle)
    
    def setMeg(self, meg):
        self.normalize()
        self.scale(meg)

    def meg(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def sqrMeg(self):
        return (self.x*self.x + self.y*self.y)

    def dist(self, other):
        return math.sqrt((other.x-self.x)*(other.x-self.x) + (other.y-self.y)*(other.y-self.y))

    def sqrDist(self, other):
        return ((other.x-self.x)*(other.x-self.x) + (other.y-self.y)*(other.y-self.y))

    def angle_x(self):
        if self.y == 0:
            return math.atan(0)
        return math.atan(self.x / self.y)

    def angle_y(self):
        if self.x == 0:
            return math.atan(0)
        return math.atan(self.y / self.x)

    def rotate(self, angle) -> None:
        matrix = [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle),  math.cos(angle)]
        ]

        self *= matrix

    # Conversion
    def __str__(self) -> str:
        s = "X: {0:<5}\nY: {1:<5}\n".format(self.x, self.y)
        return s

    def getInt(self):
        return Vector2(int(self.x), int(self.y))

    def asStructure(self):
        return Vector2_str(self)

class Vector2_str(Structure):
    _fields_ = [
        ("x", c_int),
        ("y", c_int)
    ]
    
    def __init__(self, v: Vector2):
        self.x = int(v.x)
        self.y = int(v.y)    
