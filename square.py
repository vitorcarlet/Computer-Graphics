from OpenGL.GL import *
from OpenGL.GLUT import *

def inicio():
    glClearColor(0,255,0)

def desenha():
    #limpa a tela e mantem a cor definida no inicio
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()

def main():
    try:
        #Inicialização do glut; tbm inicializa a máquina de estados do OpenGL
        glutInit()
        #Define modo de exibição
        glutInitDisplayMode(GLUT_SINGEL | GLUT_RGB)
        #Posição na tela
        glutInitWindowsPosition(100,100)
        #tamanho na janela
        glutInitWindowsSize(600,600)
        glutCreateWindow(b"Ola mundo grafico")
    except Exception as e:
        printf("Erro ao criar contexto OpenGL: {e}")
    
    inicio()
    glutDisplayFunc(desenha)
    glutMainLoop()


if __name__ == '__main__':
    main()
