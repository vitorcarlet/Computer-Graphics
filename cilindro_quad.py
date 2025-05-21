import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

width, height = 800, 600

def desenharCilindro():
    glRotatef(90, 1, 0, 0)  # Rotaciona o cilindro para ficar em pé
    glColor3f(0.2, 0.2, 0.2)  # cor da base
    quad = gluNewQuadric()    
    # gluQuadricTexture(quadric, GL_TRUE)
    # raio, raio, altura, segmentos, segmentos verticais
    gluCylinder(quad, 1, 1, 2.0, 64, 1)

    #Desenha a tampa inferior
    glPushMatrix()
    # glColor3f(0.2, 0.8, 0.4)  # cor da base
    glRotatef(180, 1, 0, 0)   # inverte eixo Y para desenhar voltado para baixo
    gluDisk(quad, 0, 1.0, 64, 1)
    glPopMatrix()

    # Desenha a tampa superior
    glPushMatrix()
    # glColor3f(0.2, 0.4, 0.8)  # cor do topo
    glTranslatef(0, 0, 2.0)   # move para o topo do cilindro
    gluDisk(quad, 0, 1.0, 64, 1)
    glPopMatrix()
    gluDeleteQuadric(quad)

def setupLighting():
    
    # --- Configura iluminação básica ---
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Luz branca, posicionada no canto superior direito
    light_pos = [1.0, 1.0, 1.0, 1.0]    
    light_diffuse = [1.0, 1.0, 1.0, 1.0]#branca
    light_ambient = [0.2, 0.2, 0.2, 1.0]#branca
    light_specular = [1.0, 1.0, 1.0, 1.0]#branca
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        
    # glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    # glMateriali(GL_FRONT, GL_SHININESS, 50)  # Brilho
    mat_ambiente = [0.2, 0.2, 0.5, 1.0]
    mat_difusa = [0.8, 0.8, 0.8, 1.0]
    mat_especular = [1.0, 1.0, 1.0, 1.0]
    mat_brilho = [50]

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambiente)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_difusa)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_especular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_brilho)

    # Permite usar glColor como material
    # glEnable(GL_COLOR_MATERIAL)
    # glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def main():    
    glfw.init()            
    window = glfw.create_window(800, 600, "Cilindro com OpenGL + GLFW", None, None)    
    glfw.make_context_current(window)    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height or 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)    
    glEnable(GL_DEPTH_TEST)

    setupLighting()

    angulo = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()
        gluLookAt(5, 3, 2, 0, 0, 0, 0, 1, 0)  # Câmera fixa
        glRotatef(angulo, 1, 1, 1)
        
        desenharCilindro()

        glfw.swap_buffers(window)
        angulo += 0.5

    glfw.terminate()

if __name__ == "__main__":
    main()