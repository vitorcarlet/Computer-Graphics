import glfw
from OpenGL.GL import *
import math

# Tamanho da janela
WIDTH, HEIGHT = 800, 600

# Quadrado (vermelho)
quadrado_x = -0.5
quadrado_y = -0.5
tam_quadrado = 0.1
vel = 0.01

# Círculo (azul)
circulo_x = 0.2
circulo_y = -0.2
raio_circulo = 0.05

#desenhado a partir do centro
def desenharQuadrado(x, y, tam, color):
    glColor3f(*color)
    metade = tam / 2
    glBegin(GL_QUADS)
    glVertex2f(x - metade, y - metade)
    glVertex2f(x + metade, y - metade)
    glVertex2f(x + metade, y + metade)
    glVertex2f(x - metade, y + metade)
    glEnd()

def desenharCirculo(x, y, radius, color, segments=50):
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
    glEnd()

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def checarColisao(quad_x, quad_y, s_tam, cx, cy, raio):
    metade = s_tam / 2
    x_prox = clamp(cx, quad_x - metade, quad_x + metade)
    y_prox = clamp(cy, quad_y - metade, quad_y + metade)    
    distance = math.hypot(x_prox - cx, y_prox - cy)
    return distance < raio

def verificarColisao(quad_x, quad_y):
    return checarColisao(quad_x, quad_y, tam_quadrado, circulo_x, circulo_y, raio_circulo)

def main():
    global quadrado_x, quadrado_y

    glfw.init()        
    window = glfw.create_window(WIDTH, HEIGHT, "Colisão Quadrado e Círculo", None, None)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Simula movimento e verifica colisão
        x = quadrado_x
        y = quadrado_y

        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            y += vel
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            y -= vel
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            x -= vel
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            x += vel

        # Só move se não colidir
        if not verificarColisao(x, y):
            quadrado_x = x
            quadrado_y = y

        # Renderização
        glClear(GL_COLOR_BUFFER_BIT)

        desenharQuadrado(quadrado_x, quadrado_y, tam_quadrado, (1.0, 0.0, 0.0))
        desenharCirculo(circulo_x, circulo_y, raio_circulo, (0.0, 0.0, 1.0))

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
