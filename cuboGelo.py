import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import trimesh

# --------------------------------------------------
# Variáveis de câmera
# --------------------------------------------------
# Define posição inicial, direção (front) e “up vector” da câmera,
# além da velocidade de movimento.
camera_pos = np.array([2.5, 2.5, 2.5], dtype=np.float32)
camera_front = np.array([0.0, 0.0, 0.0], dtype=np.float32) - camera_pos
camera_front = camera_front / np.linalg.norm(camera_front)  # normaliza o vetor
camera_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
camera_speed = 0.05

# --------------------------------------------------
# Criação de um cubo arredondado (usando trimesh)
# --------------------------------------------------
def create_rounded_cube(radius=0.2, size=1.0):
    """
    Gera um cubo subdividido e empurra cada vértice ao longo da
    sua direção radial para criar bordas arredondadas.
    """
    cube = trimesh.creation.box(extents=[size, size, size])
    # Subdivide para adicionar mais triângulos (suavização)
    cube = cube.subdivide()
    cube = cube.subdivide()

    # Centraliza vértices em torno da origem
    verts = cube.vertices - cube.center_mass
    # Calcula norma e direção de cada vértice
    norms = np.linalg.norm(verts, axis=1, keepdims=True)
    direction = verts / np.maximum(norms, 1e-6)
    # Move cada vértice ao longo da direção para criar o arredondamento
    smoothed_verts = verts + direction * radius
    cube.vertices = smoothed_verts
    return cube

# --------------------------------------------------
# Inicialização da janela com GLFW
# --------------------------------------------------
def init_window(width, height, title):
    """
    Cria a janela GLFW, configura o contexto OpenGL e ativa
    teste de profundidade e normalização de normais.
    """
    if not glfw.init():
        raise Exception("GLFW não pôde ser inicializado")

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Janela não pôde ser criada")

    glfw.make_context_current(window)
    # Ativa depth test para renderizar faces ocultas corretamente
    glEnable(GL_DEPTH_TEST)
    # Normaliza automaticamente normais após transformações
    glEnable(GL_NORMALIZE)
    return window

# --------------------------------------------------
# Callback de teclado para movimentar/rotacionar câmera
# --------------------------------------------------
def key_callback(window, key, scancode, action, mods):
    """
    Captura teclas W/A/S/D/Q/E para movimentação e
    setas esquerda/direita para girar a câmera no eixo Y.
    """
    global camera_pos, camera_front, camera_up, camera_speed

    if action == glfw.PRESS or action == glfw.REPEAT:
        # Move para frente (W)
        if key == glfw.KEY_W:
            camera_pos += camera_speed * camera_front
        # Move para trás (S)
        elif key == glfw.KEY_S:
            camera_pos -= camera_speed * camera_front
        # Strafe esquerda (A)
        elif key == glfw.KEY_A:
            right = np.cross(camera_front, camera_up)
            right /= np.linalg.norm(right)
            camera_pos -= camera_speed * right
        # Strafe direita (D)
        elif key == glfw.KEY_D:
            right = np.cross(camera_front, camera_up)
            right /= np.linalg.norm(right)
            camera_pos += camera_speed * right
        # Sobe (Q)
        elif key == glfw.KEY_Q:
            camera_pos += camera_speed * camera_up
        # Desce (E)
        elif key == glfw.KEY_E:
            camera_pos -= camera_speed * camera_up
        # Gira câmera para a esquerda (←)
        elif key == glfw.KEY_LEFT:
            angle = np.radians(2.0)
            x = camera_front[0] * np.cos(angle) - camera_front[2] * np.sin(angle)
            z = camera_front[0] * np.sin(angle) + camera_front[2] * np.cos(angle)
            camera_front[0], camera_front[2] = x, z
            camera_front /= np.linalg.norm(camera_front)
        # Gira câmera para a direita (→)
        elif key == glfw.KEY_RIGHT:
            angle = np.radians(-2.0)
            x = camera_front[0] * np.cos(angle) - camera_front[2] * np.sin(angle)
            z = camera_front[0] * np.sin(angle) + camera_front[2] * np.cos(angle)
            camera_front[0], camera_front[2] = x, z
            camera_front /= np.linalg.norm(camera_front)

# --------------------------------------------------
# Configuração de material e luz para efeito “vidro”
# --------------------------------------------------
def setup_material_glass():
    """
    Configura uma luz pontual (GL_LIGHT0) e define
    propriedades de material translúcido para simular vidro.
    """
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
 
   # ----------------------------
# Propriedades da luz (GL_LIGHT0)
# ----------------------------

light_pos = [2.0, 2.0, 2.0, 1.0]
glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
#   • GL_POSITION: define a posição da fonte de luz.
#     - [x, y, z, w]: se w = 1.0, a luz é pontual em (x,y,z);
#       se w = 0.0, a luz é direcional vindo da direção (x,y,z).

glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
#   • GL_AMBIENT: componente de luz ambiente.
#     - [r, g, b, a]: cor que ilumina uniformemente toda a cena,
#       simulando luz refletida indiretamente.

glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.7, 0.7, 1.0, 1.0])
#   • GL_DIFFUSE: componente de luz difusa.
#     - [r, g, b, a]: cor que incide diretamente nos objetos;
#       depende do ângulo entre a fonte e a normal da superfície,
#       criando sombreamento.

glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
#   • GL_SPECULAR: componente de luz especular.
#     - [r, g, b, a]: realça o brilho (reflexo especular) nos pontos
#       onde a luz reflete diretamente no observador.

# ----------------------------
# Propriedades do material “vidro” (transparente)
# ----------------------------

glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,   [0.6, 0.8, 1.0, 0.5])
#   • GL_AMBIENT: refletância ambiente do material.
#     - [r, g, b, a]: define como o objeto reflete a luz ambiente.
#     - Aqui, um tom azul claro com alpha = 0.5 para translucidez.

glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,   [0.7, 0.9, 1.0, 0.5])
#   • GL_DIFFUSE: refletância difusa do material.
#     - [r, g, b, a]: controla a cor sob luz direta,
#       também com alpha = 0.5 para transparência.

glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR,  [1.0, 1.0, 1.0, 1.0])
#   • GL_SPECULAR: refletância especular do material.
#     - [r, g, b, a]: cor do brilho especular.
#     - Alpha = 1.0 (opaco) para que o brilho não seja afetado pela translucidez.

glMaterialf (GL_FRONT_AND_BACK, GL_SHININESS, 100.0)
#   • GL_SHININESS: expoente do brilho especular.
#     - Valores altos (até 128) tornam o destaque mais apertado e intenso,
#       simulando superfícies muito polidas como vidro.

# --------------------------------------------------
# Função genérica para desenhar um mesh trimesh
# --------------------------------------------------
def draw_trimesh(mesh):
    """
    Itera sobre cada face do mesh, calcula a normal
    e emite os vértices para o pipeline OpenGL.
    """
    glBegin(GL_TRIANGLES)
    for face in mesh.faces:
        v1, v2, v3 = mesh.vertices[face]
        # Calcula normal da face
        n = np.cross(v2 - v1, v3 - v1)
        n /= np.linalg.norm(n)
        glNormal3fv(n)
        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v3)
    glEnd()

# --------------------------------------------------
# Alternativa: criação de cubo chanfrado aproximado
# --------------------------------------------------
def create_beveled_cube_approx(size=1.0, bevel=0.15, subdivisions=3):
    """
    Semelhante a create_rounded_cube, mas permite controlar
    nível de subdivisão e profundidade do chanfro (bevel).
    """
    cube = trimesh.creation.box(extents=[size]*3)
    for _ in range(subdivisions):
        cube = cube.subdivide()

    verts = cube.vertices - cube.center_mass
    norms = np.linalg.norm(verts, axis=1, keepdims=True)
    dirs = verts / np.maximum(norms, 1e-8)
    cube.vertices = cube.vertices + dirs * bevel

    return cube

# --------------------------------------------------
# Função principal: setup, loop de renderização
# --------------------------------------------------
def main():
    global camera_pos, camera_front

    # 1) Cria a janela e registra callback de teclado
    window = init_window(800, 600, "Cubo de Gelo Arredondado")
    glfw.set_key_callback(window, key_callback)

    # 2) Prepara material/luz para renderizar o “vidro”
    setup_material_glass()

    # 3) Configura perspectiva da câmera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 100.0)

    # 4) Gera o mesh do cubo chanfrado
    cube_mesh = create_beveled_cube_approx()
    angle = 0

    # Exibe controles no terminal
    print("Controles de câmera:")
    print("W/S: Avançar/Retornar")
    print("A/D: Strafe esquerda/direita")
    print("Q/E: Sobe/Desce")
    print("Setas ← →: Rotacionar câmera")

    # 5) Loop até a janela ser fechada
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 6) Define matriz de modelo e view (posição da câmera)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        target = camera_pos + camera_front
        gluLookAt(
            camera_pos[0], camera_pos[1], camera_pos[2],
            target[0],     target[1],     target[2],
            camera_up[0],  camera_up[1],  camera_up[2]
        )

        # 7) Roda lentamente o cubo para melhor visualização
        glRotatef(angle, 1, 1, 0)

        # 8) Desenha o mesh utilizando draw_trimesh
        draw_trimesh(cube_mesh)

        # 9) Troca buffers (double buffering)
        glfw.swap_buffers(window)
        angle += 0.4

    # 10) Limpa e fecha GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()
