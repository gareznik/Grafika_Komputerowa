# #!C:/Users/koles/AppData/Local/Programs/Python/Python314/python.exe
# import math
# import sys
# import random

# from glfw.GLFW import *

# from OpenGL.GL import *
# from OpenGL.GLU import *

# N = 30
# vertices = [[[0.0] * 3 for i in range(N)] for j in range(N)]

# def create_linspace(start, stop, num):
#     if num == 1:
#         return [start]
    
#     step = (stop - start) / (num - 1)
#     return [start + step * i for i in range(num)]

# def calculate_egg_vertices():
#     global vertices, N

#     # wyznaczyć N-elementowe tablice wartości dla parametrów u i v
#     # (от 0.0 до 1.0)
#     u_coords = create_linspace(0.0, 1.0, N)
#     v_coords = create_linspace(0.0, 1.0, N)

#     # dla każdej pary u i v obliczyć i zapisać w tablicy wartości x, y i z
#     for i in range(N):
#         for j in range(N):
#             u = u_coords[i]
#             v = v_coords[j]

#             # Формулы для x, y, z из PDF
#             P = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u)
            
#             x = P * math.cos(math.pi * v)
#             y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
#             z = P * math.sin(math.pi * v)

#             # Сохраняем [x, y, z] в 3D-список
#             vertices[i][j] = [x, y, z]

# def draw_egg_points():
#     # posłużyć się prymitywem GL_POINTS
#     glBegin(GL_POINTS)
    
#     # Установим один цвет для всех точек
#     glColor3f(1.0, 1.0, 0.0) # Желтый

#     for i in range(N):
#         for j in range(N):
#             # elementy tablicy będą stanowiły wejście funkcji glVertex()
#             # Функция glVertex3fv прекрасно работает и с обычными списками Python
#             glVertex3fv(vertices[i][j])
#     glEnd()
    
# def startup():
#     update_viewport(None, 400, 400)
#     glClearColor(0.0, 0.0, 0.0, 1.0)
#     glEnable(GL_DEPTH_TEST)


# def shutdown():
#     pass

# def spin(angle):
#     glRotatef(angle, 1.0, 0.0, 0.0)
#     glRotatef(angle, 0.0, 1.0, 0.0)
#     glRotatef(angle, 0.0, 0.0, 1.0)

# def axes():
#     glBegin(GL_LINES)

#     glColor3f(1.0, 0.0, 0.0)
#     glVertex3f(-5.0, 0.0, 0.0)
#     glVertex3f(5.0, 0.0, 0.0)

#     glColor3f(0.0, 1.0, 0.0)
#     glVertex3f(0.0, -5.0, 0.0)
#     glVertex3f(0.0, 5.0, 0.0)

#     glColor3f(0.0, 0.0, 1.0)
#     glVertex3f(0.0, 0.0, -5.0)
#     glVertex3f(0.0, 0.0, 5.0)

#     glEnd()


# def render(time):
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     spin(time * 180 / 3.1415)

#     axes()

#     draw_egg_points()

#     glFlush()


# def update_viewport(window, width, height):
#     if width == 0:
#         width = 1
#     if height == 0:
#         height = 1
#     aspect_ratio = width / height

#     glMatrixMode(GL_PROJECTION)
#     glViewport(0, 0, width, height)
#     glLoadIdentity()

#     if width <= height:
#         glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
#     else:
#         glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()


# def main():
#     if not glfwInit():
#         sys.exit(-1)

#     calculate_egg_vertices()

#     window = glfwCreateWindow(400, 400, __file__, None, None)
#     if not window:
#         glfwTerminate()
#         sys.exit(-1)

#     glfwMakeContextCurrent(window)
#     glfwSetFramebufferSizeCallback(window, update_viewport)
#     glfwSwapInterval(1)

#     startup()
#     while not glfwWindowShouldClose(window):
#         render(glfwGetTime())
#         glfwSwapBuffers(window)
#         glfwPollEvents()
#     shutdown()

#     glfwTerminate()


# if __name__ == '__main__':
#     main()


#!/usr/bin/env python3
import sys
import math
import random

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Deklaracja rozmiaru tablicy wierzchołków (gęstość siatki)
N = 50 

# Tablice do przechowywania współrzędnych i kolorów
tab = [[[0] * 3 for _ in range(N)] for _ in range(N)]
colors = [[[0] * 3 for _ in range(N)] for _ in range(N)]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)  # Włączenie bufora głębi [cite: 176]

    # Obliczanie wierzchołków modelu jajka i losowanie kolorów
    # Zakres u i v to [0, 1] [cite: 138]
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)

            # Wzory z instrukcji 
            # Obliczenie x(u,v)
            x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi * v)
            # Obliczenie y(u,v)
            y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
            # Obliczenie z(u,v)
            z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi * v)

            tab[i][j] = [x, y, z]

            # Losowy kolor dla każdego wierzchołka (wymóg na 4.0) 
            colors[i][j] = [random.random(), random.random(), random.random()]

def shutdown():
    pass

def axes():
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

# Funkcja spin realizująca obrót [cite: 251]
def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0) # Obrót wokół osi X dla lepszej widoczności
    glRotatef(angle, 0.0, 1.0, 0.0) # Dodatkowy obrót wokół Y

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Obracanie obiektu (wymóg na 3.5/4.0)
    # Kąt w stopniach = time * 180 / pi [cite: 283]
    spin(time * 180 / math.pi)

    axes()

    # Rysowanie modelu jajka za pomocą trójkątów (GL_TRIANGLES) 
    glBegin(GL_TRIANGLES)
    
    # Iterujemy do N-1, ponieważ łączymy element i z i+1
    for i in range(N - 1):
        for j in range(N - 1):
            # Trójkąt 1: (i, j), (i+1, j), (i, j+1) 
            glColor3fv(colors[i][j])
            glVertex3fv(tab[i][j])
            
            glColor3fv(colors[i+1][j])
            glVertex3fv(tab[i+1][j])
            
            glColor3fv(colors[i][j+1])
            glVertex3fv(tab[i][j+1])

            # Trójkąt 2 (dopełniający): (i, j+1), (i+1, j), (i+1, j+1) 
            glColor3fv(colors[i][j+1])
            glVertex3fv(tab[i][j+1])
            
            glColor3fv(colors[i+1][j])
            glVertex3fv(tab[i+1][j])
            
            glColor3fv(colors[i+1][j+1])
            glVertex3fv(tab[i+1][j+1])
            
    glEnd()

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