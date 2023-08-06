import cv2
import os
import sys
import numpy as np
from ctypes import cdll, c_int, c_float
from .vectors import *

class Color:
    r = 0
    g = 0
    b = 0

    def __init__(self, r: int=0, g: int=0, b: int=0):
        if r > 255:
            self.r = 255
        elif r < 0:
            self.r = 0
        else:
            self.r = r
            
        if g > 255:
            self.g = 255
        elif g < 0:
            self.g = 0
        else:
            self.g = g
            
        if b > 255:
            self.b = 255
        elif b < 0:
            self.b = 0
        else:
            self.b = b

    def asArray(self):
        array = np.array([self.r, self.g, self.b], dtype=int)
        return array

    def __str__(self):
        s = "R: {0:<5} G: {1:<5} B: {2:<5}".format(self.r, self.g, self.b)
        return s

class Colors(os.abc.ABC):
    White = Color(255, 255, 255)

class DrawMode:
    Top = 0
    Center = 1
    Bottom = 2

class PyRender:
    # Variables
    dimension = None
    fps = None

    frames = None
    currFrame = None
    lib = None

    rotation = None
    translation = None

    bgColor = None

    # Methods
    def __init__(self, dimension, bgColor: Color=Color(0, 0, 0), fps: int=30):
        self.dimension = dimension
        self.fps = fps

        self.rotation = 0
        self.translation = Vector2()

        self.bgColor = bgColor

        self.lib = cdll.LoadLibrary("{0}\\Lib\\site-packages\\pyrender\\libraries\\2d_drawCalls.dll".format(sys.prefix))

        self.lib.clearArray.argtypes = [
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(dimension[0] * dimension[1] * 3,)),
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(3,)),

            c_int, c_int
        ]

        self.lib.drawRect.argtypes = [
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(dimension[0] * dimension[1] * 3,)),
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(3,)),

            Vector2_str,
            Vector2_str,

            c_float,
            c_int, c_int
        ]

        self.lib.drawCircle.argtypes = [
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(dimension[0] * dimension[1] * 3,)),
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(3,)),

            Vector2_str,
            c_int,
            
            c_int, c_int
        ]

        self.lib.drawLine.argtypes = [
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(dimension[0] * dimension[1] * 3,)),
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(3,)),

            Vector2_str,
            Vector2_str,

            c_int,
            c_int, c_int
        ]

        self.lib.drawTriangle.argtypes = [
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(dimension[0] * dimension[1] * 3,)),
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(3,)),

            Vector2_str,
            Vector2_str,
            Vector2_str,

            c_int, c_int
        ]

        self.lib.drawQuad.argtypes = [
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(dimension[0] * dimension[1] * 3,)),
            np.ctypeslib.ndpointer(dtype=int, ndim=1, shape=(3,)),

            Vector2_str,
            Vector2_str,
            Vector2_str,
            Vector2_str,

            c_int, c_int
        ]

        self.frames = []
        self.currFrame = np.zeros((dimension[0] * dimension[1] * 3,), dtype=int)

        self.setBackground(bgColor.asArray())

    def drawQuad(self, point1, point2, point3, point4, color):
        color = color.asArray()

        point1 = Vector2_str(point1)
        point2 = Vector2_str(point2)
        point3 = Vector2_str(point3)
        point4 = Vector2_str(point4)

        self.lib.drawQuad(self.currFrame, color, point1, point2, point3, point4, self.dimension[0], self.dimension[1])

    def drawTriangle(self, point1, point2, point3, color):
        color = color.asArray()

        p1 = point1.asStructure()
        p2 = point2.asStructure()
        p3 = point3.asStructure()

        self.lib.drawTriangle(self.currFrame, color, p1, p2, p3, self.dimension[0], self.dimension[1])

    def drawLine(self, start, end, thickness, color):
        color = color.asArray()

        start += self.translation
        end += self.translation

        if start.sqrMeg() < end.sqrMeg():
            start = start.asStructure()
            end = end.asStructure()

            self.lib.drawLine(self.currFrame, color, start, end, int(thickness), self.dimension[0], self.dimension[1])
        else:
            start = start.asStructure()
            end = end.asStructure()
            
            self.lib.drawLine(self.currFrame, color, end, start, int(thickness), self.dimension[0], self.dimension[1])
        
    def drawCircle(self, pos, r, color, drawMode):
        center = Vector2()

        if drawMode == DrawMode.Top:
            center = pos + r
        elif drawMode == DrawMode.Center:
            center = pos
        elif drawMode == DrawMode.Bottom:
            center = pos - r

        color = color.asArray()
        center = center.asStructure()

        self.lib.drawCircle(self.currFrame, color, center, int(r), self.dimension[0], self.dimension[1])

    def drawRect(self, pos, dimension, color, drawMode):
        center = Vector2(0, 0)

        if drawMode == DrawMode.Top:
            center = pos + Vector2(dimension.x / 2, dimension.y / 2)
        elif drawMode == DrawMode.Center:
            center = pos
        elif drawMode == DrawMode.Bottom:
            center = pos - Vector2(dimension.x / 2, dimension.y / 2)

        color = color.asArray()

        center += self.translation
        center = Vector2_str(center)
        dimension = Vector2_str(dimension)
        
        self.lib.drawRect(self.currFrame, color, center, dimension, self.rotation, self.dimension[0], self.dimension[1])

    def setBackground(self, color):
        self.lib.clearArray(self.currFrame, color, self.dimension[0], self.dimension[1])

    def rotate(self, angle):
        self.rotation = angle

    def translate(self, x, y):
        self.translation.x = x
        self.translation.y = y

    def nextFrame(self, delCurr=False):
        self.frames.append(self.currFrame.reshape((self.dimension[1], self.dimension[0], 3)))

        if delCurr:
            self.currFrame = np.zeros((self.dimension[0] * self.dimension[1] * 3,), dtype=int)
            self.setBackground(self.bgColor.asArray())

    def render(self, renderPath: str, output: str="video"):
        try:
            os.makedirs(renderPath + "\\frames")
        except:
            os.system("del {0}\\frames".format(renderPath))

        renderPath = renderPath + "\\frames"
        for i in range(len(self.frames)):
            cv2.imwrite("{0}\\frame{1:>010d}.png".format(renderPath, i+1), self.frames[i])

        videoWriter = cv2.VideoWriter(
            renderPath + "\\" + output + ".mp4",
            cv2.VideoWriter.fourcc(*'mp4v'),
            self.fps,
            self.dimension
        )

        for frame in os.listdir("{0}".format(renderPath)):
            frame = cv2.imread("{0}\\{1}".format(renderPath, frame))
            videoWriter.write(frame)

        videoWriter.release()
