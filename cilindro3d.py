import math
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# ---------- estado da câmera ----------
distance      = 6.0          # raio da órbita
azim, elev    = 45.0, 25.0   # ângulos em graus
pivot_x, pivot_y = 0.0, 0.0  # deslocamento (pan)
mode = None                  # 'orbit' | 'pan' | None
last_x, last_y = 0, 0

def init_window():
    w, h = 800, 600
    glfw.init()
    win = glfw.create_window(w, h, "Cilindro - Controles estilo Blender", None, None)
    glfw.make_context_current(win)

    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Registra os callbacks do mouse
    glfw.set_mouse_button_callback(win, on_mouse_button)
    glfw.set_cursor_pos_callback(win, on_mouse_move)
    glfw.set_scroll_callback(win, on_scroll)
    return win

# ---------- entrada do usuário ----------
def on_mouse_button(win, button, action, mods):
    global mode
    if action == glfw.PRESS:
        # Órbita ............................ clique esquerdo (ou botão do meio)
        if button in (glfw.MOUSE_BUTTON_LEFT, glfw.MOUSE_BUTTON_MIDDLE) and not (mods & glfw.MOD_SHIFT):
            mode = 'orbit'
        # Panorâmica ......................... Shift + clique (esquerdo ou meio)
        elif button in (glfw.MOUSE_BUTTON_LEFT, glfw.MOUSE_BUTTON_MIDDLE) and (mods & glfw.MOD_SHIFT):
            mode = 'pan'
    elif action == glfw.RELEASE and mode is not None:
        mode = None

def on_mouse_move(win, x, y):
    global last_x, last_y, azim, elev, pivot_x, pivot_y
    dx, dy = x - last_x, y - last_y  # diferença de posição do mouse

    if mode == 'orbit':  # arrastar com clique esquerdo
        azim += dx * 0.4                  # órbita horizontal
        azim = azim % 360                 # mantém dentro de 0–360°
        elev = max(-89, min(89, elev + dy * 0.4))  # órbita vertical (limitada)
    elif mode == 'pan':  # Shift + arrastar
        factor = 0.002 * distance         # fator proporcional à distância
        pivot_x += -dx * factor
        pivot_y +=  dy * factor           # eixo Y da tela é invertido

    last_x, last_y = x, y

def on_scroll(win, xo, yo):
    global distance
    # Aproxima ou afasta (zoom/dolly), limitado entre 1.5 e 20 unidades
    distance = max(1.5, min(distance - yo * 0.6, 20.0))

# ---------- renderização ----------
def draw_cylinder():
    glColor3f(0.6, 0.2, 1.0)
    q = gluNewQuadric()
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)     # gira para que o cilindro fique em pé (eixo Z)
    gluCylinder(q, 1, 1, 2, 32, 32)  # corpo
    gluDisk(q, 0, 1, 32, 1)          # base inferior
    glTranslatef(0, 0, 2)
    gluDisk(q, 0, 1, 32, 1)          # base superior
    glPopMatrix()
    gluDeleteQuadric(q)

# ---------- loop principal ----------
def main():
    win = init_window()
    global azim, elev, distance, pivot_x, pivot_y

    while not glfw.window_should_close(win):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # calcula a posição da câmera em coordenadas esféricas ao redor do pivô
        az, el = math.radians(azim), math.radians(elev)
        cx = pivot_x + distance * math.cos(el) * math.sin(az)
        cy = pivot_y + distance * math.sin(el)
        cz =           distance * math.cos(el) * math.cos(az)
        gluLookAt(cx, cy, cz, pivot_x, pivot_y, 0, 0, 1, 0)

        draw_cylinder()

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
