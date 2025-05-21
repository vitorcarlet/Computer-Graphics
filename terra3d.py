import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import time

# Configuração básica
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Proporções do sistema (arbitrárias para visualização)
# Distâncias (em unidade arbitrária)
SOL_RADIUS = 0.5
TERRA_RADIUS = 0.15
LUA_RADIUS = 0.05

# Órbitas elípticas (semi-eixos)
TERRA_ORBIT_A = 3.0   # eixo maior
TERRA_ORBIT_B = 2.0   # eixo menor

LUA_ORBIT_A = 0.5
LUA_ORBIT_B = 0.3

# Velocidades angulares (rad/s, aceleradas para visualização)
TERRA_ORBITAL_SPEED = 0.5   # velocidade da translação da Terra
TERRA_ROTATION_SPEED = 2.0  # velocidade de rotação da Terra

LUA_ORBITAL_SPEED = 2.0
LUA_ROTATION_SPEED = 5.0

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Luz ambiente, difusa e especular
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.05, 0.05, 0.05, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.0, 1.0, 0.9, 1.0])   # Luz amarelada
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 0.9, 1.0])

    # Posição da luz (sol no centro)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 0.0, 1.0])

def draw_sphere(radius):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 50, 50)
    gluDeleteQuadric(quad)

def main():
    if not glfw.init():
        print("Erro ao iniciar GLFW")
        return

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sistema Sol-Terra-Lua", None, None)
    if not window:
        glfw.terminate()
        print("Erro ao criar janela")
        return

    glfw.make_context_current(window)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    # Configura projeção perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100)

    # Posição da câmera (um pouco afastada para ver o sistema)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(7, 5, 7, 0, 0, 0, 0, 1, 0)

    setup_lighting()

    # Variáveis de tempo para animação
    start_time = time.time()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        elapsed = time.time() - start_time

        # --- Desenha o Sol ---
        glPushMatrix()
        # O Sol é emissivo (fonte de luz)
        glMaterialfv(GL_FRONT, GL_EMISSION, [1.0, 0.9, 0.0, 1.0])  # amarelo forte
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])   # sem cor difusa (apenas emissão)
        draw_sphere(SOL_RADIUS)
        # Remove a emissão para os outros objetos
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glPopMatrix()

        # --- Calcula posição da Terra na órbita elíptica ---
        terra_orbit_angle = elapsed * TERRA_ORBITAL_SPEED
        terra_x = TERRA_ORBIT_A * math.cos(terra_orbit_angle)
        terra_z = TERRA_ORBIT_B * math.sin(terra_orbit_angle)

        # --- Desenha a Terra ---
        glPushMatrix()
        glTranslatef(terra_x, 0.0, terra_z)
        # Rotação da Terra em torno do próprio eixo
        terra_rotation_angle = (elapsed * TERRA_ROTATION_SPEED * 360) % 360
        glRotatef(terra_rotation_angle, 0, 1, 0)

        # Material da Terra
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.2, 0.4, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.6, 0.6, 0.6, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50)
        draw_sphere(TERRA_RADIUS)

        # --- Calcula posição da Lua na órbita elíptica em torno da Terra ---
        lua_orbit_angle = elapsed * LUA_ORBITAL_SPEED
        lua_x = LUA_ORBIT_A * math.cos(lua_orbit_angle)
        lua_z = LUA_ORBIT_B * math.sin(lua_orbit_angle)

        # --- Desenha a Lua ---
        glPushMatrix()
        glTranslatef(lua_x, 0.0, lua_z)
        # Rotação da Lua em torno do próprio eixo
        lua_rotation_angle = (elapsed * LUA_ROTATION_SPEED * 360) % 360
        glRotatef(lua_rotation_angle, 0, 1, 0)

        # Material da Lua
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 10)
        draw_sphere(LUA_RADIUS)
        glPopMatrix()

        glPopMatrix()  # termina a Terra + Lua

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
