import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# Variáveis globais
rotacao_x = 0.0
rotacao_y = 0.0
dist_zoom = 8.0  # Distância da câmera
mouse_clicado = False
mouse_pos = (0, 0)

def init_window():
    width, height = 800, 600
    glfw.init()        
    window = glfw.create_window(width, height, "Cubo com Zoom", None, None)
    glfw.make_context_current(window)
    
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Callbacks de entrada
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    return window

# Callback de teclado
def key_callback(window, key, scancode, action, mods):
    global rotacao_x, rotacao_y
    if action in [glfw.PRESS, glfw.REPEAT]:
        if key == glfw.KEY_UP:
            rotacao_x -= 5
        elif key == glfw.KEY_DOWN:
            rotacao_x += 5
        elif key == glfw.KEY_LEFT:
            rotacao_y -= 5
        elif key == glfw.KEY_RIGHT:
            rotacao_y += 5

# Callback de rolagem do mouse (zoom)
def scroll_callback(window, xoffset, yoffset):
    global dist_zoom
    dist_zoom -= yoffset  # Aproxima ou afasta
    dist_zoom = max(2.0, min(dist_zoom, 50.0))  # Limites de zoom

# Callback de clique do mouse
def mouse_button_callback(window, button, action, mods):
    global mouse_clicado
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_clicado = (action == glfw.PRESS)

# Callback de movimento do mouse
def cursor_position_callback(window, xpos, ypos):
    global mouse_pos, rotacao_x, rotacao_y
    if mouse_clicado:
        dx = xpos - mouse_pos[0]
        dy = ypos - mouse_pos[1]
        rotacao_y += dx * 0.5
        rotacao_x += dy * 0.5
    mouse_pos = (xpos, ypos)

# Desenha o cubo
def desenharCubo():
    glBegin(GL_QUADS)

    glColor3f(1, 0, 0)  # Frente
    glVertex3f(-1, -1, 1)
    glVertex3f( 1, -1, 1)
    glVertex3f( 1,  1, 1)
    glVertex3f(-1,  1, 1)

    glColor3f(0, 1, 0)  # Trás
    glVertex3f(-1, -1, -1)
    glVertex3f(-1,  1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1, -1, -1)

    glColor3f(0, 0, 1)  # Esquerda
    glVertex3f(-1, -1, -1)
    glVertex3f(-1, -1,  1)
    glVertex3f(-1,  1,  1)
    glVertex3f(-1,  1, -1)

    glColor3f(1, 1, 0)  # Direita
    glVertex3f(1, -1, -1)
    glVertex3f(1,  1, -1)
    glVertex3f(1,  1,  1)
    glVertex3f(1, -1,  1)

    glColor3f(1, 0, 1)  # Topo
    glVertex3f(-1, 1, -1)
    glVertex3f(-1, 1,  1)
    glVertex3f( 1, 1,  1)
    glVertex3f( 1, 1, -1)

    glColor3f(0, 1, 1)  # Base
    glVertex3f(-1, -1, -1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1, -1,  1)
    glVertex3f(-1, -1,  1)

    glEnd()

# Loop principal
def main():
    global rotacao_x, rotacao_y, dist_zoom
    window = init_window()   

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Define a posição da câmera com base na distância (zoom)
        gluLookAt(
            dist_zoom * 0.5, dist_zoom * 0.4, dist_zoom,
            0, 0, 0,
            0, 1, 0
        )

        # Aplica rotação
        glRotatef(rotacao_x, 1, 0, 0)
        glRotatef(rotacao_y, 0, 1, 0)

        desenharCubo()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
