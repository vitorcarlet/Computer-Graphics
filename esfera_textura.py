import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

def init_window(width, height, title):
    glfw.init()    
    window = glfw.create_window(width, height, title, None, None)    
    glfw.make_context_current(window)
    return window

def load_texture(path):
    #Carregar a imagem usando PIL e converter para o formato necessário para OpenGL
    image = Image.open(path)
    width, height = image.size
    #Corrige a origem da imagem no sistema de coordenadas OpenGL
    # OpenGL considera a origem no canto inferior esquerdo, enquanto PIL considera no canto superior esquerdo
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # Obtém os dados da imagem em bytes convertendo para RGB
    img_data = image.convert("RGB").tobytes()

    # Gera identificador para 1 textura e vincula a textura ao contexto atual
    tex_id = glGenTextures(1)
    # Atualiza o contexto atual (máquina de estados) para a textura
    glBindTexture(GL_TEXTURE_2D, tex_id)
    # Define o formato da textura, largura, altura, e os dados da imagem, inclusive o tamanho de borda
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    # Configura os parâmetros da textura para filtro de minification e magnification
    # Ou seja, como a textura deve ser exibida quando é reduzida ou ampliada
    # GL_LINEAR: interpolação linear
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex_id

def iluminar():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMateriali(GL_FRONT, GL_SHININESS, 50)

def desenharEsfera(textura_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, 1.0, 50, 50)
    gluDeleteQuadric(quad)

    glDisable(GL_TEXTURE_2D)

def main():
    window = init_window(800, 600, "Esfera com Textura e Iluminação")
    glEnable(GL_DEPTH_TEST)
    iluminar()

    textura_id = load_texture("textura.jpg")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)
    rotacao_x = 0
    rotacao_y = 0

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(2, 2, 4, 0, 0, 0, 0, 1, 0)
        glRotatef(rotacao_x, 1, 0, 0)
        glRotatef(rotacao_y, 0, 1, 0)

        # Incrementa os ângulos de rotação
        rotacao_x += 0.5
        rotacao_y += 0.5

        desenharEsfera(textura_id)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()