from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi

def inicio():
    glClearColor(0.5, 0.8, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)

def desenha_casa():
    glColor3f(1, 1, 0)
    glBegin(GL_QUADS)
    glVertex2f(150, 200)
    glVertex2f(650, 200)
    glVertex2f(650, 500)
    glVertex2f(150, 500)
    glEnd()

    glColor3f(1, 0, 0)
    glBegin(GL_TRIANGLES)
    glVertex2f(100, 500)
    glVertex2f(700, 500)
    glVertex2f(400, 600)
    glEnd()

    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex2f(0, 200)
    glVertex2f(800, 200)
    glVertex2f(800, 0)
    glVertex2f(0, 0)
    glEnd()

    glColor3f(0.6, 0.3, 0)
    glBegin(GL_QUADS)
    glVertex2f(350, 200)
    glVertex2f(450, 200)
    glVertex2f(450, 300)
    glVertex2f(350, 300)
    glEnd()

    glColor3f(1, 1, 0)
    desenha_circulo(440, 250, 5)

    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex2f(250, 320)
    glVertex2f(350, 320)
    glVertex2f(350, 420)
    glVertex2f(250, 420)
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(250, 370)
    glVertex2f(350, 370)
    glVertex2f(300, 320)
    glVertex2f(300, 420)
    glEnd()

    glColor3f(1,1,1)
    glBegin(GL_QUADS)
    glVertex2f(450, 320)
    glVertex2f(550, 320)
    glVertex2f(550, 420)
    glVertex2f(450, 420)
    glEnd()

    glColor3f(0,0,0)
    glBegin(GL_LINES)
    glVertex2f(450, 370)
    glVertex2f(550, 370)
    glVertex2f(500, 320)
    glVertex2f(500, 420)
    glEnd()

def desenha_peppa_pig():
    glColor3f(1, 0.4, 0.6)
    desenha_circulo(650, 220, 70)

    desenha_circulo(750, 250, 60)

    glColor3f(1, 0.4, 0.6)
    desenha_circulo(770, 290, 10)
    desenha_circulo(730, 290, 10)

    glColor3f(1, 1, 1)
    desenha_circulo(740, 260, 10)
    desenha_circulo(760, 260, 10)

    glColor3f(0, 0, 0)
    desenha_circulo(740, 265, 4)
    desenha_circulo(760, 265, 4)

    glColor3f(1, 0.2, 0.2)
    desenha_circulo(750, 245, 10)

    glColor3f(0, 0, 0)
    glBegin(GL_LINE_STRIP)
    glVertex2f(750, 220)
    glVertex2f(740, 230)
    glVertex2f(760, 230)
    glVertex2f(750, 220)
    glEnd()

    glColor3f(1, 0.4, 0.6)
    desenha_circulo(680, 140, 20)
    desenha_circulo(730, 170, 20)
    desenha_circulo(620, 140, 20)
    desenha_circulo(780, 170, 20)

def desenha_circulo(x, y, raio):
    num_lados = 100
    glBegin(GL_POLYGON)
    for i in range(num_lados):
        angulo = 2 * pi * i / num_lados
        xi = x + raio * cos(angulo)
        yi = y + raio * sin(angulo)
        glVertex2f(xi, yi)
    glEnd()

def desenha():
    glClear(GL_COLOR_BUFFER_BIT)
    desenha_casa()
    desenha_peppa_pig()
    glFlush()

def main():
    try:
        glutInit()
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowPosition(100, 100)
        glutInitWindowSize(800, 600)
        glutCreateWindow(b"Cena com Casa e Peppa Pig")
    except Exception as e:
        print(f"Erro ao criar contexto OpenGL: {e}")
    
    inicio()
    glutDisplayFunc(desenha)
    glutMainLoop()

if __name__ == '__main__':
    main();
