#!/usr/bin/env python3
import math
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

# Rozmiar siatki (N x N)
N = 30
vertices = [[[0.0] * 3 for i in range(N)] for j in range(N)]

def create_linspace(start, stop, num):
    if num == 1:
        return [start]
    
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]

def calculate_egg_vertices():
    global vertices, N

    # Wyznaczenie N-elementowej tablicy wartości dla parametrów u i v
    # (przedział od 0.0 do 1.0) [cite: 269, 270]
    u_coords = create_linspace(0.0, 1.0, N)
    v_coords = create_linspace(0.0, 1.0, N)

    # Obliczenie współrzędnych x, y, z dla każdej pary (u, v) [cite: 271]
    for i in range(N):
        for j in range(N):
            u = u_coords[i]
            v = v_coords[j]

            # Wzory na x, y, z zgodnie z instrukcją [cite: 136, 137]
            P = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u)
            
            x = P * math.cos(math.pi * v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            z = P * math.sin(math.pi * v)

            # Zapisanie [x, y, z] do tablicy 3D [cite: 266]
            vertices[i][j] = [x, y, z]

def draw_egg_lines():
    # Zadanie na 3.5: Rysowanie modelu przy pomocy linii [cite: 277]
    glBegin(GL_LINES)
    
    glColor3f(1.0, 1.0, 0.0) # Żółty kolor linii

    # Iteracja po tablicy wierzchołków
    for i in range(N):
        for j in range(N):
            # Element (i, j) połączyć z elementem (i+1, j) - linia pionowa
            # Sprawdzamy zakres, aby nie wyjść poza tablicę (i < N-1) 
            if i < N - 1:
                glVertex3fv(vertices[i][j])
                glVertex3fv(vertices[i+1][j])
            
            # Element (i, j) połączyć z elementem (i, j+1) - linia pozioma
            # Sprawdzamy zakres (j < N-1) 
            if j < N - 1:
                glVertex3fv(vertices[i][j])
                glVertex3fv(vertices[i][j+1])
                
    glEnd()

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST) # Włączenie bufora głębi [cite: 176]

def shutdown():
    pass

def spin(angle):
    # Funkcja obracająca obiekt [cite: 250, 256]
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def axes():
    # Rysowanie osi współrzędnych [cite: 177]
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
    
    # Animacja obrotu: time traktowany jako kąt w radianach, zamiana na stopnie [cite: 283]
    spin(time * 180 / math.pi)

    axes()

    # Wywołanie funkcji rysującej linie (zamiast punktów)
    draw_egg_lines()

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

    calculate_egg_vertices()

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