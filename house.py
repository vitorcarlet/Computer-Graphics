from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi  # Importando as funções trigonométricas

# Função de inicialização
def inicio():
    glClearColor(0.5, 0.8, 1, 1)  # Cor de fundo azul claro
    glMatrixMode(GL_PROJECTION)  # Muda para a matriz de projeção
    glLoadIdentity()  # Reseta a matriz de projeção
    gluOrtho2D(0, 800, 0, 600)  # Define a visão ortográfica 2D


# Função para desenhar a casa
def desenha_casa():
    # Corpo da casa (retângulo) - Amarelo
    glColor3f(1, 1, 0)  # Cor amarela
    glBegin(GL_QUADS)
    glVertex2f(150, 200)  # Inferior esquerdo
    glVertex2f(650, 200)  # Inferior direito
    glVertex2f(650, 500)  # Superior direito (aumento da altura)
    glVertex2f(150, 500)  # Superior esquerdo (aumento da altura)
    glEnd()

    # Teto da casa (triângulo) - Vermelho
    glColor3f(1, 0, 0)  # Cor vermelha
    glBegin(GL_TRIANGLES)
    glVertex2f(100, 500)  # Ponto inferior esquerdo
    glVertex2f(700, 500)  # Ponto inferior direito
    glVertex2f(400, 600)  # Ponto do topo
    glEnd()

    # Chão da casa - Verde
    glColor3f(0, 1, 0)  # Cor verde
    glBegin(GL_QUADS)
    glVertex2f(0, 200)  # Inferior esquerdo
    glVertex2f(800, 200)  # Inferior direito
    glVertex2f(800, 0)  # Inferior direito (piso)
    glVertex2f(0, 0)  # Inferior esquerdo (piso)
    glEnd()

    # Porta (marrom)
    glColor3f(0.6, 0.3, 0)  # Cor marrom
    glBegin(GL_QUADS)
    glVertex2f(350, 200)
    glVertex2f(450, 200)
    glVertex2f(450, 300)
    glVertex2f(350, 300)
    glEnd()

    # Fechadura da porta (círculo pequeno)
    glColor3f(1, 1, 0)  # Cor amarela (para a fechadura)
    desenha_circulo(440, 250, 5)

    # Janelas (brancas) com Xanfro (detalhes nas janelas)
    glColor3f(1, 1, 1)  # Cor branca
    glBegin(GL_QUADS)
    glVertex2f(250, 320)  # Mover para baixo
    glVertex2f(350, 320)
    glVertex2f(350, 420)
    glVertex2f(250, 420)
    glEnd()

    # Adicionando Xanfro (cruzamento de linhas)
    glColor3f(0, 0, 0)  # Cor preta
    glBegin(GL_LINES)
    glVertex2f(250, 370)
    glVertex2f(350, 370)  # Linha horizontal
    glVertex2f(300, 320)
    glVertex2f(300, 420)  # Linha vertical
    glEnd()

    glColor3f(1,1,1)
    glBegin(GL_QUADS)
    glVertex2f(450, 320)  # Mover para baixo
    glVertex2f(550, 320)
    glVertex2f(550, 420)
    glVertex2f(450, 420)
    glEnd()

    # Adicionando Xanfro na outra janela
    glColor3f(0,0,0)
    glBegin(GL_LINES)
    glVertex2f(450, 370)
    glVertex2f(550, 370)  # Linha horizontal
    glVertex2f(500, 320)
    glVertex2f(500, 420)  # Linha vertical
    glEnd()


# Função para desenhar a Peppa Pig simplificada
def desenha_peppa_pig():
    # Corpo da Peppa (círculo rosa) - Movido para a direita
    glColor3f(1, 0.4, 0.6)  # Cor rosa
    desenha_circulo(650, 220, 70)  # Corpo movido para a direita (aumentado)

    # Cabeça da Peppa (círculo rosa) - Movido para a direita
    desenha_circulo(750, 250, 60)

    # Orelhas
    glColor3f(1, 0.4, 0.6)  # Cor rosa
    desenha_circulo(770, 290, 10)
    desenha_circulo(730, 290, 10)

    # Olhos
    glColor3f(1, 1, 1)  # Cor branca
    desenha_circulo(740, 260, 10)
    desenha_circulo(760, 260, 10)

    # Pupilas
    glColor3f(0, 0, 0)  # Cor preta
    desenha_circulo(740, 265, 4)
    desenha_circulo(760, 265, 4)

    # Nariz (Xanfro)
    glColor3f(1, 0.2, 0.2)  # Cor do nariz (rosa)
    desenha_circulo(770, 245, 10)  # Aumentado para um xanfro maior

    # Boca (uma linha curva simples)
    glColor3f(0, 0, 0)  # Cor preta
    glBegin(GL_LINE_STRIP)
    glVertex2f(775, 240)
    glVertex2f(775, 230)
    glVertex2f(780, 225)
    glEnd()

    # Patas da Peppa (círculos pequenos)
    glColor3f(1, 0.4, 0.6)  # Cor rosa
    desenha_circulo(630, 170, 20)  # Pata frente esquerda
    desenha_circulo(670, 170, 20)  # Pata frente direita
    desenha_circulo(620, 120, 20)  # Pata traseira esquerda
    desenha_circulo(680, 120, 20)  # Pata traseira direita


# Função para desenhar círculos
def desenha_circulo(x, y, raio):
    num_lados = 100
    glBegin(GL_POLYGON)
    for i in range(num_lados):
        angulo = 2 * pi * i / num_lados  # Usando pi da biblioteca math
        xi = x + raio * cos(angulo)
        yi = y + raio * sin(angulo)
        glVertex2f(xi, yi)
    glEnd()


# Função de desenho
def desenha():
    glClear(GL_COLOR_BUFFER_BIT)  # Limpa a tela
    desenha_casa()  # Desenha a casa
    desenha_peppa_pig()  # Desenha a Peppa Pig
    glFlush()  # Renderiza a tela


# Função principal
def main():
    try:
        glutInit()  # Inicializa o GLUT
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)  # Modo de exibição
        glutInitWindowPosition(100, 100)  # Posição da janela
        glutInitWindowSize(800, 600)  # Tamanho da janela
        glutCreateWindow(b"Cena com Casa e Peppa Pig")  # Cria a janela
    except Exception as e:
        print(f"Erro ao criar contexto OpenGL: {e}")
    
    inicio()  # Chama a função de inicialização
    glutDisplayFunc(desenha)  # Função de exibição
    glutMainLoop()  # Inicia o loop principal do GLUT


if __name__ == '__main__':
    main()
