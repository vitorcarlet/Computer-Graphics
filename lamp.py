import glfw                           # Biblioteca para criar janela e lidar com mouse e teclado
from OpenGL.GL import *              # Comandos básicos de OpenGL
from OpenGL.GLU import *             # Utilitários como câmera e formas (esfera, cilindro)
import sys                           # Para passar argumentos ao glutInit

# Dimensões da janela
width, height = 800, 600

# Ângulos de rotação da cena (controlados com o mouse)
angulo_x, angulo_y = 25, 30

# Controle do mouse
mouse_down = False       # True se o botão do mouse estiver pressionado
last_x, last_y = 0, 0    # Últimas posições do mouse

# Controle da luz
luz_ativa = True         # Variável que ativa ou desativa a luz

# ------------------------- CONFIGURAÇÃO DA ILUMINAÇÃO -------------------------
def configurarIluminacao():
    glEnable(GL_LIGHTING)            # Ativa o sistema de iluminação da OpenGL
    glEnable(GL_NORMALIZE)           # Garante que normais sejam reescaladas automaticamente
    glEnable(GL_COLOR_MATERIAL)      # Permite que cores definidas afetem o material

    # Configurações da luz (GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.05, 0.05, 0.05, 1.0])   # Luz ambiente (fraca e constante)
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.0, 1.0, 0.9, 1.0])      # Luz difusa (ilumina objetos)
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])      # Luz especular (reflexos)

    # Tipo "spotlight" (foco de luz)
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 20.0)                           # Abertura do cone da luz
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, -1.0, 0.0])          # Direção da luz (para baixo)
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 40.0)                        # Intensidade no centro do cone

    # Propriedades do material da lâmpada
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 100)  # Brilho do material

# ------------------------- DESENHA A LÂMPADA -------------------------
def desenharLampada():
    posicao_luz = [0.0, 0.0, 0.0, 1.0]               # Posição da luz (no centro da lâmpada)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)  # Define onde a luz está

    # Ativa ou desativa a luz com base na variável
    if luz_ativa:
        glEnable(GL_LIGHT0)
        glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 1.0, 0.8, 1.0])   # Lâmpada acesa: emite luz
    else:
        glDisable(GL_LIGHT0)
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # Lâmpada apagada

    # Desenha a esfera (parte principal da lâmpada)
    glPushMatrix()
    quad = gluNewQuadric()
    gluSphere(quad, 0.3, 48, 48)      # Esfera de raio 0.3
    gluDeleteQuadric(quad)
    glPopMatrix()

    # Desenha o suporte da lâmpada (um cilindro)
    glPushMatrix()
    glTranslatef(0.0, 0.3, 0.0)       # Move o cilindro acima da lâmpada
    glRotatef(-90, 1, 0, 0)           # Rotaciona para ficar na vertical
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # Sem emissão no suporte
    glColor3f(0.1, 0.1, 0.4)          # Cor azul escuro
    quad = gluNewQuadric()
    gluCylinder(quad, 0.15, 0.15, 0.3, 32, 1)  # Cilindro com base e topo do mesmo tamanho
    gluDeleteQuadric(quad)
    glPopMatrix()

# ------------------------- DESENHA O CHÃO -------------------------
def desenharCena():
    glPushMatrix()
    glTranslatef(0, -1.0, 0)         # Move para baixo
    glScalef(6, 0.2, 6)              # Achata e estica (forma tipo "piso")
    glColor3f(0.2, 0.2, 0.2)         # Cor cinza escuro
    quad = gluNewQuadric()
    gluSphere(quad, 1.0, 32, 32)     # Um "chão" em forma de esfera achatada
    gluDeleteQuadric(quad)
    glPopMatrix()

# ------------------------- CALLBACKS -------------------------
def mouse_button_callback(window, button, action, mods):
    global mouse_down
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_down = action == glfw.PRESS  # True se o botão esquerdo for pressionado

def cursor_position_callback(window, xpos, ypos):
    global angulo_x, angulo_y, last_x, last_y, mouse_down
    if mouse_down:
        dx = xpos - last_x
        dy = ypos - last_y
        angulo_x += dy * 0.5  # Roda a cena no eixo X
        angulo_y += dx * 0.5  # Roda a cena no eixo Y
    last_x = xpos
    last_y = ypos

def key_callback(window, key, scancode, action, mods):
    global luz_ativa
    if key == glfw.KEY_L and action == glfw.PRESS:
        luz_ativa = not luz_ativa  # Alterna a luz ligada/desligada ao pressionar 'L'

# ------------------------- FUNÇÃO PRINCIPAL -------------------------
def main():
    if not glfw.init():
        return

    # Cria a janela
    window = glfw.create_window(width, height, "Lâmpada", None, None)
    glfw.make_context_current(window)

    # Registra os callbacks
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_key_callback(window, key_callback)

    # Configurações iniciais de OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Cor de fundo preta

    glViewport(0, 0, width, height)  # Área de renderização
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height), 0.1, 100.0)  # Projeção perspectiva
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)  # Ativa teste de profundidade

    configurarIluminacao()  # Chama a função que configura a luz

    # Loop principal
    while not glfw.window_should_close(window):
        glfw.poll_events()  # Processa eventos do sistema
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpa tela

        glLoadIdentity()
        gluLookAt(2, 2, 4, 0, 0, 0, 0, 1, 0)  # Define posição da câmera
        glRotatef(angulo_x, 1, 0, 0)         # Roda a cena em X
        glRotatef(angulo_y, 0, 1, 0)         # Roda a cena em Y

        desenharLampada()  # Desenha a lâmpada
        desenharCena()     # Desenha o chão

        glfw.swap_buffers(window)  # Mostra a imagem na tela

    glfw.terminate()  # Fecha tudo

# ------------------------- EXECUÇÃO DO PROGRAMA -------------------------
if __name__ == "__main__":
    from OpenGL.GLUT import glutInit  # Necessário para evitar erros com quadrics
    glutInit(sys.argv)
    main()