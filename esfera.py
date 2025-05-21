import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

on = True
def iluminar():
    # Configuração da iluminação
    glEnable(GL_LIGHTING) # Habilita a iluminação
    glEnable(GL_LIGHT0) # Habilita a luz 0            

    # Posição da luz
    # Luz direcional vinda do topo
    # A última coordenada (0) indica que a luz é direcional
    # Se fosse 1, a luz seria pontual
    luz_pos = [1.0, 1.0, 1.0, 0]
    glLightfv(GL_LIGHT0, GL_POSITION, luz_pos)

    # Cor da luz ambiente
    luz_ambiente = [0.2, 0.2, 0.2, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)

    # # Cor da luz difusa
    luz_difusa = [1, 1, 1, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)

    # # Cor da luz especular
    luz_especular = [0.5, 0.5, 0.5, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)

    # Propriedades do material
    mat_ambiente = [0.2, 0.2, 0.2, 1.0]
    mat_difusa = [0.8, 0.8, 0.8, 1.0]
    mat_especular = [0.8, 0.8, 0.8, 1.0]
    mat_brilho = [50]
    

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambiente)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_difusa)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_especular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_brilho)    

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def iluminacaoAmbiente():
    # Configuração da iluminação
    glEnable(GL_LIGHTING) # Habilita a iluminação
    glEnable(GL_LIGHT0) # Habilita a luz 0        

    # Cor da luz ambiente
    luz_ambiente = [1, 1, 1, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)

    # # Cor da luz difusa
    luz_difusa = [0, 0, 0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)

    # # Cor da luz especular
    luz_especular = [0, 0, 0, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)

    # Propriedades do material
    mat_ambiente = [1, 1, 1, 1.0]
        
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambiente)    

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def iluminacaoDifusa():
    # Configuração da iluminação
    glEnable(GL_LIGHTING) # Habilita a iluminação
    glEnable(GL_LIGHT0) # Habilita a luz 0        

    # Cor da luz ambiente
    luz_ambiente = [0.2, 0.2, 0.2, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)

    # # Cor da luz difusa
    luz_difusa = [1, 1, 1, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)

    # # Cor da luz especular
    luz_especular = [0, 0, 0, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)

    # Propriedades do material
    mat_ambiente = [0.2, 0.2, 0.2, 1.0]
    mat_difusa = [0.8, 0.8, 0.8, 1.0]
        
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambiente)    
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_difusa)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def iluminacaoEspecular():
    # Configuração da iluminação
    glEnable(GL_LIGHTING) # Habilita a iluminação
    glEnable(GL_LIGHT0) # Habilita a luz 0        

    # Cor da luz ambiente
    luz_ambiente = [0, 0, 0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)

    # # Cor da luz difusa
    luz_difusa = [0, 0, 0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)

    # # Cor da luz especular
    luz_especular = [0.5, 0.5, 0.5, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)

    # Propriedades do material
    mat_especular = [1, 1, 1, 1.0]
    mat_brilho = [50]
        
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_especular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_brilho)    

# Função para desenhar uma esfera
def desenharEsfera(raio=1.0):
    quadric = gluNewQuadric()
    glColor3f(0.4, 0, 0)  # Cor da esfera
    gluSphere(quadric, raio, 40, 40)
    gluDeleteQuadric(quadric)
    
def tecladoDesligarIluminacao(window, key, scancode, action, mods):
    global on
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        on = not on        

def main():
    # Inicialização do GLFW
    glfw.init()
    # Configuração da janela
    window = glfw.create_window(800, 600, "Esfera com Iluminação - OpenGL Legacy", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, tecladoDesligarIluminacao)

    # Configuração da viewport
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(1, 0, 5, 0, 0, 0, 0, 1, 0)
    # Variáveis para controle de rotação
    rotation_x = 0
    rotation_y = 0

    iluminar()
    # iluminacaoAmbiente()
    # iluminacaoDifusa()
    # iluminacaoEspecular()

    # Loop principal
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        # Limpa os buffers de cor e profundidade
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Habilita o teste de profundidade
        glEnable(GL_DEPTH_TEST)
        
        # Aplica rotação
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 1, 0, 0)

        if on:
            glEnable(GL_LIGHT0) # Habilita a luz 0    
        else:
            glDisable(GL_LIGHT0)
        
        # Desenha a esfera        
        desenharEsfera()
        
        
        # Atualiza a rotação
        # rotation_x += 0.5
        # rotation_y += 0.3
        
        # Troca os buffers
        glfw.swap_buffers(window)

    # Finalização
    glfw.terminate()

if __name__ == "__main__":
    main()