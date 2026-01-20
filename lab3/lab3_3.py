#!/usr/bin/env python3
import math
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Rozmiar siatki (N x N)
N = 30

# Tablice do przechowywania współrzędnych i kolorów
vertices = [[[0.0] * 3 for i in range(N)] for j in range(N)]
colors = [[[0.0] * 3 for i in range(N)] for j in range(N)]

def create_linspace(start, stop, num):
    if num == 1:
        return [start]
    
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]

def calculate_egg_data():
    global vertices, colors, N

    # Wyznaczenie N-elementowej tablicy wartości dla parametrów u i v
    u_coords = create_linspace(0.0, 1.0, N)
    v_coords = create_linspace(0.0, 1.0, N)

    # Obliczenie współrzędnych i wylosowanie kolorów
    for i in range(N):
        for j in range(N):
            u = u_coords[i]
            v = v_coords[j]

            # Wzory na x, y, z zgodnie z instrukcją
            P = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u)
            
            x = P * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = P * math.sin(math.pi * v)

            vertices[i][j] = [x, y, z]

            # Losowanie koloru dla wierzchołka (raz, aby uniknąć migotania)
            # R, G, B w zakresie [0.0, 1.0]
            colors[i][j] = [random.random(), random.random(), random.random()]

def draw_egg_triangles():
    # Zadanie na 4.0: Rysowanie modelu przy pomocy trójkątów
    glBegin(GL_TRIANGLES)
    
    # Iterujemy do N-1, ponieważ tworzymy trójkąty między i a i+1
    for i in range(N - 1):
        for j in range(N - 1):
            # Pierwszy trójkąt: (i, j) -> (i+1, j) -> (i, j+1)
            glColor3fv(colors[i+1][j])
            glVertex3fv(vertices[i][j])
            
            # glColor3fv(colors[i+1][j])
            glVertex3fv(vertices[i+1][j])
            
            # glColor3fv(colors[i][j+1])
            glVertex3fv(vertices[i][j+1])

            # Drugi trójkąt (dopełniający): (i, j+1) -> (i+1, j) -> (i+1, j+1)
            glColor3fv(colors[i][j+1])
            glVertex3fv(vertices[i][j+1])
            
            # glColor3fv(colors[i+1][j])
            glVertex3fv(vertices[i+1][j])
            
            # glColor3fv(colors[i+1][j+1])
            glVertex3fv(vertices[i+1][j+1])
                
    glEnd()

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST) # Włączenie bufora głębi

def shutdown():
    pass

def spin(angle):
    # Funkcja obracająca obiekt
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def axes():
    # Rysowanie osi współrzędnych
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Animacja obrotu
    spin(time * 180 / math.pi)

    axes()

    # Wywołanie funkcji rysującej trójkąty
    draw_egg_triangles()

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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    if not glfwInit():
        sys.exit(-1)

    # Obliczenie danych (współrzędne + kolory) przed utworzeniem okna lub tuż po
    calculate_egg_data()

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