#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *

#0-obracanie objektu, 1 - obracanie kamery
movement_mode = 0 

#parametry camery
c_R = 10.0
c_theta = 0.0
c_phi = 0.0

#parametru objektu
o_theta = 0.0
o_phi = 0.0
o_scale = 1.0

#zmienne myszy
pix2angle = 1.0
left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

def shutdown():
    pass

def axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0); glVertex3f(-5.0, 0.0, 0.0); glVertex3f(5.0, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0); glVertex3f(0.0, -5.0, 0.0); glVertex3f(0.0, 5.0, 0.0)
    glColor3f(0.0, 0.0, 1.0); glVertex3f(0.0, 0.0, -5.0); glVertex3f(0.0, 0.0, 5.0)
    glEnd()

def example_object():
    glColor3f(1.0, 1.0, 1.0)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    
    #obracanie oraz scale objekta w trybie objekta
    glRotatef(o_theta, 0.0, 1.0, 0.0)
    glRotatef(o_phi, 1.0, 0.0, 0.0)
    glScalef(o_scale, o_scale, o_scale)


    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)
    gluSphere(quadric, 1.5, 10, 10)
    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)
    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)
    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)
    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)
    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)

def render(time):
    global c_theta, c_phi, c_R
    global o_theta, o_phi, o_scale

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # --- ЛОГИКА ОБНОВЛЕНИЯ ДАННЫХ ---
    if left_mouse_button_pressed:
        #kamera
        if movement_mode == 0:
            c_theta += delta_x * pix2angle
            c_phi += delta_y * pix2angle
        #objekt
        else:
            o_theta += delta_x * pix2angle
            o_phi += delta_y * pix2angle
    
    if right_mouse_button_pressed:
        #kamera zoom
        if movement_mode == 0:
            c_R += delta_x * 0.1
        #objekt scale
        else:
            o_scale += delta_x * 0.01

    #ograniczenia kamery
    c_theta = c_theta % 360.0
    if c_phi > 89.0: c_phi = 89.0
    if c_phi < -89.0: c_phi = -89.0
    if c_R < 2.0: c_R = 2.0
    if c_R > 50.0: c_R = 50.0

    #współrzędne kamery na sferze w radianach(stopnie*pi/180)
    x_eye = c_R * math.cos(c_theta * math.pi / 180) * math.cos(c_phi * math.pi / 180)
    y_eye = c_R * math.sin(c_phi * math.pi / 180)
    z_eye = c_R * math.sin(c_theta * math.pi / 180) * math.cos(c_phi * math.pi / 180)

    #ustawienie kamery 
    gluLookAt(x_eye, y_eye, z_eye,
              0.0, 0.0, 0.0,   #punkt patrzenia (do srodka)
              0.0, 1.0, 0.0)   #wektor gory

    axes()
    
    example_object()
    
    glFlush()

def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0, 0.1, 300.0)
    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard_key_callback(window, key, scancode, action, mods):
    global movement_mode
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
        
    #obsluga przycisku TAb 
    if key == GLFW_KEY_TAB and action == GLFW_PRESS:
        movement_mode = 1 - movement_mode
        mode_name = "OBJECT" if movement_mode == 1 else "CAMERA"
        print(f"Mode switched to: {mode_name}")

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, mouse_x_pos_old
    global delta_y, mouse_y_pos_old
    
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed
    
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_RELEASE:
        left_mouse_button_pressed = 0
        
    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    elif button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_RELEASE:
        right_mouse_button_pressed = 0

def main():
    if not glfwInit():
        sys.exit(-1)
    window = glfwCreateWindow(400, 400, "Nacisnij TAB do zmiany trybu pracy", None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)
    
    startup()
    
    print("Program uruchomiony")
    print("Sterowanie:")
    print("  LPM (przeciąganie): Obrót (Kamera lub Obiekt)")
    print("  PPM (przeciąganie): Przybliżanie (Kamera) lub Skalowanie (Obiekt)")
    print("  TAB: Zmiana trybu (Kamera lub Obiekt)")
    
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()
    glfwTerminate()

if __name__ == '__main__':
    main()