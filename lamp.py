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
    # Ativa o sistema de iluminação geral da OpenGL
    glEnable(GL_LIGHTING)

    # Garante que vetores normais sejam automaticamente normalizados (evita bugs com escala)
    glEnable(GL_NORMALIZE)

    # Permite que chamadas a glColor* também afetem as propriedades do material
    # Útil quando você quer controlar a cor do objeto com glColor em vez de glMaterial
    glEnable(GL_COLOR_MATERIAL)

    # ---------- PROPRIEDADES DA LUZ (GL_LIGHT0) ----------

    # Luz ambiente: ilumina de forma uniforme e fraca toda a cena (sem direção específica)
    # Ideal para dar um mínimo de visibilidade mesmo em áreas sombreadas
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])  # Cinza escuro, bem sutil

    # Luz difusa: simula a luz direta batendo nos objetos e variando com o ângulo da superfície
    # Essa é a principal luz responsável pela "forma visível" dos objetos
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.9, 1.0])     # Luz branca-amarelada (quente)

    # Luz especular: cria reflexos brilhantes nos objetos (como brilhos metálicos ou de vidro)
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])    # Branco puro, reflexo forte

    # ---------- DEFINIÇÃO DE SPOTLIGHT (FOCO DE LUZ) ----------

    # Define o ângulo de abertura do cone de luz (em graus)
    # Um valor menor → foco mais concentrado, tipo lanterna ou abajur
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 60.0)  # Cone estreito de 20°

    # Define a direção em que o cone de luz está apontando (vetor)
    # Neste caso, a luz está apontando para baixo (eixo Y negativo)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0.0, -1.0, 0.0])

    # Controla a concentração da luz no centro do cone (exponencial)
    # Valores maiores tornam o centro mais brilhante (mais concentrado)
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 2.0)

    # ---------- MATERIAL DA FONTE DE LUZ (ex: a lâmpada física em si) ----------

    # Componente ambiente do material (influenciada pela luz ambiente)
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  # Cinza leve

    # Componente difusa do material (principal cor visível sob luz direta)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0])  # Amarelo claro (tom de luz quente)

    # Componente especular do material (brilho/reflexo da superfície)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Reflexo forte e branco

    # "Brilho" do material (0 a 128): controla o tamanho e intensidade do reflexo especular
    # Quanto maior, mais concentrado e realista o reflexo (ideal para metais, vidro etc.)
    glMaterialf(GL_FRONT, GL_SHININESS, 128)

# ------------------------- DESENHA A LÂMPADA -------------------------
def desenharLampada():
    # Define a posição da luz GL_LIGHT0 no mundo
    # O quarto parâmetro 1.0 indica que é uma luz pontual (posição no espaço, e não direção)
    posicao_luz = [0.0, 64, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)

    # Verifica se a luz está ligada (variável externa 'luz_ativa')
    if luz_ativa:
        glEnable(GL_LIGHT0)  # Ativa a luz GL_LIGHT0
        # Simula que a lâmpada está "acesa" com emissão de luz amarela clara
        glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 1.0, 0.8, 1.0])
    else:
        glDisable(GL_LIGHT0)  # Desliga a luz (não emite mais iluminação na cena)
        # Retira a emissão da esfera (ela fica "apagada" visualmente)
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    # ----------- PARTE VISUAL DA LÂMPADA (ESFERA) -----------

    glPushMatrix()  # Salva a matriz de transformação atual
    glTranslatef(0.0,64,0.0) # move toda a lampada para y = 14

    # Cria uma esfera que representa a lâmpada em si
    quad = gluNewQuadric()
    gluSphere(quad, 0.3, 48, 48)  # Esfera lisa com raio 0.3 e alta resolução
    gluDeleteQuadric(quad)       # Libera o objeto quadric após uso

    glPopMatrix()  # Restaura a matriz anterior

    # ----------- SUPORTE DA LÂMPADA (CILINDRO) -----------

    glPushMatrix()  # Nova transformação isolada

    # Move o cilindro para cima da esfera para parecer um suporte pendurado no teto
    glTranslatef(0.0, 0.3, 0.0)

    # Roda o cilindro para que seu eixo fique na vertical (por padrão ele cresce no eixo Z)
    glRotatef(-90, 1, 0, 0)

    # Remove emissão para que o suporte não brilhe
    glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])

    # Define a cor do suporte (somente se glColorMaterial estiver habilitado)
    glColor3f(0.1, 0.1, 0.4)  # Azul escuro

    # Cria um cilindro fixo (raio base = topo = 0.15, altura = 0.3)
    quad = gluNewQuadric()
    gluCylinder(quad, 0.15, 0.15, 0.3, 32, 1)
    gluDeleteQuadric(quad)

    glPopMatrix()  # Finaliza as transformações do suporte
    posicao_luz = [0.0, 3.0, 0.0, 1.0]               # Posição da luz (no centro da lâmpada)
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

def draw_sphere(radius):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 50, 50)
    gluDeleteQuadric(quad)

def desenha_esfera():
    glPushMatrix()
    glTranslatef(0,-1,0)
    
    # Material da Terra
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.2, 0.4, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.6, 0.6, 0.6, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50)
    draw_sphere(0.4)
    glPopMatrix()


# ------------------------- DESENHA O CHÃO -------------------------
def desenharCena():
    glPushMatrix()
    glTranslatef(0, -2.0, 0)      # Move a base para baixo
    glScalef(6, 0.2, 6)           # Achata e estica como um piso

    # MATERIAL REFLEXIVO: como mármore polido ou piso encerado
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,  [0.1, 0.1, 0.1, 1.0])  # Pouca luz ambiente
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,  [0.3, 0.3, 0.3, 1.0])  # Cinza escuro moderado
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Reflexo branco intenso
    glMaterialf (GL_FRONT_AND_BACK, GL_SHININESS, 80.0)                # Brilho concentrado

    # Usando esfera achatada para simular um chão polido curvo
    quad = gluNewQuadric()
    gluSphere(quad, 1.0, 32, 32)
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
        desenha_esfera()
        desenharCena()     # Desenha o chão

        glfw.swap_buffers(window)  # Mostra a imagem na tela

    glfw.terminate()  # Fecha tudo

# ------------------------- EXECUÇÃO DO PROGRAMA -------------------------
if __name__ == "__main__":
    from OpenGL.GLUT import glutInit  # Necessário para evitar erros com quadrics
    glutInit(sys.argv)
    main()