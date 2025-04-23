from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math


posicao_x, posicao_y = 0.0, 0.0
angulo = 0.0


velocidade = 0.05

def iniciar():
    glClearColor(0.0, 0.0, 0.0, 1.0)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1) 

def desenhar_nave():
    glPushMatrix()
    glTranslatef(posicao_x, posicao_y, 0)
    glRotatef(angulo, 0, 0, 1)

    glColor3f(1.0, 1.0, 1.0)  
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.1)       # Ponta 
    glVertex2f(-0.05, -0.05)   # Base esquerda
    glVertex2f(0.05, -0.05)    # Base direita
    glEnd()

    glPopMatrix()

def desenhar():
    glClear(GL_COLOR_BUFFER_BIT)
    desenhar_nave()
    glFlush()

def teclas_especiais(tecla, x_mouse, y_mouse):
    global posicao_x, posicao_y, angulo

    rad = math.radians(angulo)
    deslocamento_x = velocidade * math.sin(rad)
    deslocamento_y = velocidade * math.cos(rad)

    if tecla == GLUT_KEY_UP:  # mexer pra frente
        if -1.0 < posicao_x + deslocamento_x < 1.0 and -1.0 < posicao_y + deslocamento_y < 1.0: # calculo pra ver se posição nao sai da tela
            posicao_x += deslocamento_x
            posicao_y += deslocamento_y
    elif tecla == GLUT_KEY_DOWN:  # Mexer pra trás
        if -1.0 < posicao_x - deslocamento_x < 1.0 and -1.0 < posicao_y - deslocamento_y < 1.0: # calculo pra ver se a posição nao sai da tela 
            posicao_x -= deslocamento_x
            posicao_y -= deslocamento_y
    elif tecla == GLUT_KEY_LEFT:  # Rotacionar para esquerda
        angulo += 5
    elif tecla == GLUT_KEY_RIGHT:  # Rotacionar para direita
        angulo -= 5

    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Nave Triangular - OpenGL")
    iniciar()
    glutDisplayFunc(desenhar)
    glutSpecialFunc(teclas_especiais)
    glutMainLoop()

main()
