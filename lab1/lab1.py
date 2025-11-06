#!C:/Users/koles/AppData/Local/Programs/Python/Python314/python.exe
import sys
import time

import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def trojkat(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()


def prostokat(x,y,a,b):
    half_a = a / 2
    half_b = b / 2

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(x - half_a, y - half_b)
    glVertex2f(x + half_a, y - half_b)
    glVertex2f(x + half_a, y + half_b)
    glEnd()

    glBegin(GL_TRIANGLES)
    # glColor3f(0.0, 1.0, 0.0)    #zeby nie bylo zmiany koloru w prostokacie serpinskiego
    glVertex2f(x - half_a, y - half_b)
    glVertex2f(x + half_a, y + half_b)
    glVertex2f(x - half_a, y + half_b)
    glEnd()
    
def prostokat_random(x, y, a, b, d):
    half_a = a / 2
    half_b = b / 2

    d = 0

    v1_x = x - half_a + random.randint(-d, d)
    v1_y = y - half_b + random.randint(-d, d)

    v2_x = x + half_a + random.randint(-d, d)
    v2_y = y - half_b + random.randint(-d, d)

    v3_x = x + half_a + random.randint(-d, d)
    v3_y = y + half_b + random.randint(-d, d)

    v4_x = x - half_a + random.randint(-d, d)
    v4_y = y + half_b + random.randint(-d, d)
    

    glBegin(GL_TRIANGLES)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(v1_x, v1_y)
    glVertex2f(v2_x, v2_y)
    glVertex2f(v3_x, v3_y)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(v1_x, v1_y)
    glVertex2f(v3_x, v3_y)
    glVertex2f(v4_x, v4_y)
    glEnd()

    glFlush()

def draw_sierpinski_carpet(x, y, a, b, level):
    if level == 0:
        prostokat(x, y, a, b)
    else:
        new_a = a / 3.0
        new_b = b / 3.0
        for i in range(-1, 2):  # i = -1 (lewo), 0 (środek), 1 (prawo)
            for j in range(-1, 2):  # j = -1 (dół), 0 (środek), 1 (góra)
                # Pomijamy rysowanie środkowego prostokąta (i=0, j=0)
                if not (i == 0 and j == 0):
                    # Obliczamy nowe współrzędne środka dla 8 mniejszych prostokątów
                    new_x = x + (i * new_a)
                    new_y = y + (j * new_b)
                    # Wywołujemy funkcję rekurencyjnie dla 8 mniejszych prostokątów,
                    # zmniejszając poziom (level) o 1.
                    draw_sierpinski_carpet(new_x, new_y, new_a, new_b, level - 1)

def draw_sierpinski_trojkat(x1, y1, x2, y2, x3, y3, level):
    if level == 0:
        trojkat(x1, y1, x2, y2, x3, y3)
    else:
        # Obliczanie środków boków trójkąta
        m1 = ((x1 + x2) / 2, (y1 + y2) / 2)
        m2 = ((x2 + x3) / 2, (y2 + y3) / 2)
        m3 = ((x1 + x3) / 2, (y1 + y3) / 2)
        # Wywołanie rekurencyjne dla trzech mniejszych trójkątów
        draw_sierpinski_trojkat(x1, y1, m1[0], m1[1], m3[0], m3[1], level - 1)
        draw_sierpinski_trojkat(x2, y2, m1[0], m1[1], m2[0], m2[1], level - 1)
        draw_sierpinski_trojkat(x3, y3, m2[0], m2[1], m3[0], m3[1], level - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # zad1
    # glBegin(GL_TRIANGLES)
    # glColor3f(1.0, 0.0, 0.0)
    # glVertex2f(-50.0, -50.0)
    # glColor3f(0.0, 1.0, 0.0)
    # glVertex2f(50.0, -50.0)
    # glColor3f(0.0, 0.0, 1.0)
    # glVertex2f(0.0, 50.0)
    # glEnd()

    # zad2
    # prostokat(0,0,100,50)

    # zad3
    # prostokat_random(0, 0, 100, 100, 100)

    # zad4
    # draw_sierpinski_carpet(0, 0, 200, 200, 3)

    # zad5
    draw_sierpinski_trojkat(-75, -65, 75, -65, 0, 75, 5)
    
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
