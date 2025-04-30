import glfw
from OpenGL.GL import *
import math
import random
import time
#from playsound import playsound

# ----------------------------
# Posição e velocidade da nave
x, y = 0.0, 0.0        # posição
angulo = 0.0           # ângulo (graus)
vx, vy = 0.0, 0.0      # velocidade linear
vel_rot = 0.0          # velocidade de rotação

# ----------------------------
# Aceleração (linear e rotacional) e fricção
ACEL_TRANSLACAO = 0.0005
ACEL_ROT = 0.1
FRICCAO = 0.0003
FRICCAO_ROT = 0.05

# ----------------------------
# Limites de velocidade
VEL_MAX = 0.02
VEL_ROT_MAX = 3.0

MODO_FRICCAO = True  # Se True, aplica desaceleração gradualmente

# ----------------------------
# Estrutura para monitorar teclas
key_states = {
    glfw.KEY_UP: False,
    glfw.KEY_DOWN: False,
    glfw.KEY_LEFT: False,
    glfw.KEY_RIGHT: False,
    glfw.KEY_SPACE: False  # Tiro
}

# ----------------------------
# Asteroides
NUM_ASTEROIDES = 5
asteroides = []

# ----------------------------
# Tiros
tiros = []  # cada elemento: {x, y, vx, vy, raio, ativo}

# Parâmetros de tiro
TIRO_VEL = 0.03   # velocidade inicial do projétil
TIRO_RAIO = 0.01  # "tamanho" usado na colisão

# ----------------------------
# Estrelas de enfeite
estrelas = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(100)]

def inicio():
    glClearColor(0, 0, 0, 1)

def inicializa_asteroides():
    """Cria asteroides em posições e velocidades aleatórias."""
    global asteroides
    for _ in range(NUM_ASTEROIDES):
        ax = random.uniform(-0.9, 0.6)
        ay = random.uniform(-0.9, 0.5)
        avx = random.uniform(-0.001, 0.001)
        avy = random.uniform(-0.001, 0.001)
        raio = random.uniform(0.05, 0.125)  # Raio fixo para todos os asteroides
        rotacao = random.uniform(0, 360)
        asteroides.append({'x': ax, 'y': ay, 'vx': avx, 'vy': avy, 'raio': raio, 'rotacao': rotacao})


def desenha_estrelas():
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    for ex, ey in estrelas:
        glVertex2f(ex, ey)
    glEnd()

def desenha_nave():
    """ Desenha a nave na posição (x, y) com ângulo 'angulo'. """
    global x, y, angulo

    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(angulo, 0, 0, 1)
    glScalef(0.5, 0.5, 1.0)

    # Corpo central da nave (amarelo)
    glColor3f(1, 1, 0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0.2)
    glVertex2f(-0.07, -0.1)
    glVertex2f(0.07, -0.1)
    glEnd()

    # Asas (vermelho)
    glColor3f(1, 0, 0)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.05, -0.1)
    glVertex2f(-0.15, -0.15)
    glVertex2f(-0.07, -0.05)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(0.05, -0.1)
    glVertex2f(0.15, -0.15)
    glVertex2f(0.07, -0.05)
    glEnd()

    glPopMatrix()

def desenha_asteroides():
    """Desenha cada asteroide como um polígono com 4 lados e rotação controlada."""
    for ast in asteroides:
        glPushMatrix()
        glTranslatef(ast['x'], ast['y'], 0)
        glRotatef(ast['rotacao'], 0, 0, 1)  # Aplica a rotação do asteroide
        glColor3f(0.6, 0.6, 0.6)

        # Número fixo de lados para o asteroide (agora 4 lados)
        n_lados = 8
        raio = ast['raio']  # Raio fixo para todos os asteroides

        glBegin(GL_POLYGON)
        for i in range(n_lados):
            ang = math.radians(360.0 / n_lados * i)
            px = math.cos(ang) * raio
            py = math.sin(ang) * raio
            glVertex2f(px, py)
        glEnd()

        glPopMatrix()

def desenha_tiros():
    """ Desenha cada tiro como um pequeno círculo ou quadradinho. """
    glColor3f(1, 1, 1)  # branco
    for tiro in tiros:
        if tiro['ativo']:
            glPushMatrix()
            glTranslatef(tiro['x'], tiro['y'], 0)

            # Desenhar um quadradinho simples ou um pequeno círculo
            # Quadrado:
            tam = tiro['raio']
            glBegin(GL_QUADS)
            glVertex2f(-tam, -tam)
            glVertex2f( tam, -tam)
            glVertex2f( tam,  tam)
            glVertex2f(-tam,  tam)
            glEnd()

            glPopMatrix()

def atualiza_nave():
    """
    Atualiza a lógica da nave (movimento e rotação).
    """
    global x, y, angulo, vx, vy, vel_rot

    # 1) Rotação
    if key_states[glfw.KEY_LEFT]:
        vel_rot = min(vel_rot + ACEL_ROT, VEL_ROT_MAX)
    elif key_states[glfw.KEY_RIGHT]:
        vel_rot = max(vel_rot - ACEL_ROT, -VEL_ROT_MAX)
    else:
        # Fricção rotacional
        if MODO_FRICCAO:
            if vel_rot > 0:
                vel_rot = max(0, vel_rot - FRICCAO_ROT)
            elif vel_rot < 0:
                vel_rot = min(0, vel_rot + FRICCAO_ROT)

    angulo += vel_rot

    # 2) Aceleração linear
    rad = math.radians(angulo + 90)
    if key_states[glfw.KEY_UP]:
        vx += math.cos(rad) * ACEL_TRANSLACAO
        vy += math.sin(rad) * ACEL_TRANSLACAO
    elif key_states[glfw.KEY_DOWN]:
        vx -= math.cos(rad) * ACEL_TRANSLACAO
        vy -= math.sin(rad) * ACEL_TRANSLACAO
    else:
        # Fricção linear
        if MODO_FRICCAO:
            if vx > 0:
                vx = max(0, vx - FRICCAO)
            elif vx < 0:
                vx = min(0, vx + FRICCAO)

            if vy > 0:
                vy = max(0, vy - FRICCAO)
            elif vy < 0:
                vy = min(0, vy + FRICCAO)

    # 3) Limite de velocidade
    vel = math.sqrt(vx*vx + vy*vy)
    if vel > VEL_MAX:
        fator = VEL_MAX / vel
        vx *= fator
        vy *= fator

    # 4) Atualiza posição
    x += vx
    y += vy

    # 5) Wrap-around
    if x > 1: x = -1
    elif x < -1: x = 1
    if y > 1: y = -1
    elif y < -1: y = 1



def atualiza_asteroides():
    """
    Move os asteroides e aplica wrap-around.
    """
    for ast in asteroides:
        ast['x'] += ast['vx']
        ast['y'] += ast['vy']

        ast['rotacao'] += 1

        if ast['rotacao'] >= 360:
            ast['rotacao'] -= 360

        # Wrap-around
        if ast['x'] > 1: ast['x'] = -1
        elif ast['x'] < -1: ast['x'] = 1
        if ast['y'] > 1: ast['y'] = -1
        elif ast['y'] < -1: ast['y'] = 1

def cria_tiro():
    """
    Cria um novo tiro na posição da nave, com velocidade direcionada
    pelo ângulo da nave.
    """
    rad = math.radians(angulo + 90)
    # Posição inicial um pouco à frente do centro da nave
    tx = x + math.cos(rad) * 0.05
    ty = y + math.sin(rad) * 0.05

    # Velocidade do tiro = TIRO_VEL + velocidade da nave (se quiser)
    tvx = math.cos(rad) * TIRO_VEL
    tvy = math.sin(rad) * TIRO_VEL

    tiros.append({
        'x': tx,
        'y': ty,
        'vx': tvx,
        'vy': tvy,
        'raio': TIRO_RAIO,
        'ativo': True
    })

def atualiza_tiros():
    """
    Move os tiros. Desativa caso saiam da tela.
    Depois verifica colisão com asteroides.
    """
    # 1) Atualiza posição
    for tiro in tiros:
        if tiro['ativo']:
            tiro['x'] += tiro['vx']
            tiro['y'] += tiro['vy']

            # Se sair muito da tela, desativa
            if (abs(tiro['x']) > 1.2) or (abs(tiro['y']) > 1.2):
                tiro['ativo'] = False

    # 2) Checa colisão com asteroides
    for tiro in tiros:
        if not tiro['ativo']:
            continue
        for ast in asteroides:
            # Verifica distância entre tiro e asteroide
            dx = tiro['x'] - ast['x']
            dy = tiro['y'] - ast['y']
            #dist = math.sqrt((tiro['x'] - ast['x'])**2 + (tiro['y'] - ast['y'])**2)
            #dist = math.sqrt(dx**2 + dy**2)
            dist = math.hypot(dx, dy)
            if dist < (tiro['raio'] + ast['raio']):
                # Colisão
                tiro['ativo'] = False
                # Remove (ou "destrói") o asteroide
                ast['x'] = 9999  # manda pra longe, será removido depois
                break

    # 3) Remove da lista os tiros inativos
    vivos = [t for t in tiros if t['ativo']]
    tiros[:] = vivos

    # 4) Remove asteroides "destruídos" (aqueles com x = 9999, por ex.)
    ast_vivos = [a for a in asteroides if a['x'] != 9999]
    asteroides[:] = ast_vivos

def verifica_colisao_nave(window):
    for ast in asteroides:
        dx = x - ast['x']
        dy = y - ast['y']
        dist = math.hypot(dx, dy)
        raio_nave = 0.05

        if dist < (raio_nave + ast['raio']):
            print("💥 Colisão detectada! Fechando o jogo.")

            # 1. Som de explosão
            # try:
            #     playsound("explosao.wav")
            # except:
            #     print("⚠️ Erro ao tocar som (verifique o arquivo).")

            # 2. Efeito visual
            explosao_visual()

            # 3. Fecha a janela
            glfw.set_window_should_close(window, True)
            return
        
def explosao_visual():
    for raio in [0.05, 0.07, 0.1]:
        glClear(GL_COLOR_BUFFER_BIT)

        # Redesenha toda a cena primeiro
        desenha_estrelas()
        desenha_asteroides()
        desenha_tiros()
        desenha_nave()  # se quiser que a nave ainda apareça

        # Desenha a explosão por cima
        glColor3f(1, 0.3, 0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for i in range(31):
            ang = 2 * math.pi * i / 30
            glVertex2f(x + math.cos(ang) * raio, y + math.sin(ang) * raio)
        glEnd()

        glfw.swap_buffers(glfw.get_current_context())
        time.sleep(1)



def tecla_callback(window, key, scancode, action, mods):
    if key in key_states:
        # Se pressionar a tecla SPACE, cria tiro
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            cria_tiro()

        # Salva o estado da tecla (pressionada/solta)
        key_states[key] = (action != glfw.RELEASE)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(1280, 900, "Nave estilo Asteroids", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, tecla_callback)

    inicio()
    inicializa_asteroides()

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # 1) Atualiza lógicas
        atualiza_nave()
        atualiza_asteroides()
        atualiza_tiros()
        verifica_colisao_nave(window)

        # 2) Desenha cena
        desenha_estrelas()
        desenha_asteroides()
        desenha_tiros()
        desenha_nave()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
