import glfw
from OpenGL.GL import *
import math

# Inicializando as variáveis globais para a raquete
vel = 0.02  # Velocidade de movimento da raquete
y = 0.0  # Posição inicial de y da raquete
x = -0.95  # Posição de x da raquete (fixa, ou seja, na borda esquerda)

x_ball = 0.0  # Posição inicial de x da bola
y_ball = 0.0  # Posição inicial de y da bola
vel_ball = 0.01  # Velocidade de movimento da bola  
num_segments = 100  # Número de segmentos para o círculo
radius = 0.05  # Raio da bola


# Estado das teclas
key_states = {
    glfw.KEY_W: False,  # Tecla W para mover para cima
    glfw.KEY_S: False,  # Tecla S para mover para baixo
}

# Função de inicialização do OpenGL
def inicio():
    glClearColor(0, 0, 0, 1)  # Define o fundo da tela como preto

def draw_ball():
    glPushMatrix()
    glTranslatef(x_ball, y_ball, 0)  # Aplica a transformação de movimento da bola

    glBegin(GL_POLYGON)  # Inicia o desenho de um polígono
    glColor3f(1, 0, 0)  # Cor vermelha para a bola
    for i in range(num_segments):
        angle = 2 * 3.1415926 * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()
    glPopMatrix()

def update_ball():
    global x_ball, y_ball, vel_ball

    # Atualiza a posição da bola
    x_ball += vel_ball
    y_ball += vel_ball

    # Verifica se a bola colidiu com as bordas superior ou inferior
    if y_ball > 1 - radius or y_ball < -1 + radius:
        vel_ball = -vel_ball  # Inverte a direção vertical

    # Verifica se a bola colidiu com a raquete (player1)
    if x_ball <= x + 0.05 and x_ball >= x - 0.05 and y_ball <= y + 0.15 and y_ball >= y - 0.15:
        vel_ball = -vel_ball  # Inverte a direção horizontal

        # Ajuste para a direção vertical após o impacto
        # Dependendo da posição da bola na raquete, ajusta a direção vertical
        dy = y_ball - y  # Distância entre o centro da raquete e o ponto de impacto
        vel_ball = 0.01 * dy  # A velocidade vertical da bola depende da posição do impacto na raquete



# Função para desenhar o jogador 1 (a raquete)
def desenha_player1():
    glPushMatrix()
    glTranslatef(x, y, 0)  # Aplica a transformação de movimento da raquete

    glBegin(GL_QUADS)  # Inicia o desenho de um quadrado
    glColor3f(1, 1, 1)  # Cor branca para a raquete
    glVertex2f(-0.05, -0.15)  # Vértice inferior esquerdo
    glVertex2f(-0.05, 0.15)   # Vértice superior esquerdo
    glVertex2f(0.05, 0.15)    # Vértice superior direito
    glVertex2f(0.05, -0.15)   # Vértice inferior direito
    glEnd()

    glPopMatrix()

# Função para atualizar a posição da raquete (player1)
def atualiza_player1():
    global y

    # Movimento para cima (se a tecla W for pressionada)
    if key_states[glfw.KEY_W]:
        y += vel

    # Movimento para baixo (se a tecla S for pressionada)
    if key_states[glfw.KEY_S]:
        y -= vel

    # Impede que a raquete saia da tela
    if y > 1 - 0.2:  # Limite superior
        y = 1 - 0.2
    if y < -1 + 0.2:  # Limite inferior
        y = -1 + 0.2

# Função de callback para capturar o estado das teclas (W e S)
def tecla_callback(window, key, scancode, action, mods):
    if key in key_states:
        key_states[key] = action != glfw.RELEASE  # Atualiza o estado da tecla (pressionada ou liberada)

# Função principal do jogo
def main():
    # Inicializa o GLFW
    if not glfw.init():
        return

    # Criação da janela
    window = glfw.create_window(1280, 900, "Desenhando o Quadrado", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # Configuração inicial
    inicio()

    # Define a função de callback para as teclas
    glfw.set_key_callback(window, tecla_callback)

    # Loop principal de renderização
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)  # Limpa a tela

        # Atualiza a posição do jogador (raquete)
        atualiza_player1()
        update_ball()
        # Desenha o jogador (raquete)
        desenha_player1()
        draw_ball()

        glfw.swap_buffers(window)  # Troca os buffers
        glfw.poll_events()  # Processa eventos de entrada (teclado, mouse)

    glfw.terminate()  # Finaliza o GLFW

if __name__ == "__main__":
    main()  # Chama a função principal
