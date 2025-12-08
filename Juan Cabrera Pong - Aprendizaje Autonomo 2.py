# Proyecto: Aprendizaje Autonomo 2 - Pong 50%
# Requisitos:
#   - Librería pygame-ce (se instala en la terminal con: pip install pygame-ce)

import pygame #libreria util para la interfaz grafica y algunas funciones logicas del juego
import sys #esta libreria sirve para salir del juego
import random #libreria para tener valores random al momento de que la bola sale del centro

pygame.init #Iniciamos la libreria de Pygame

#Creamos la interfaz grafica para poder ver
ancho, alto = 800, 600
ventana = pygame.display.set_mode((ancho,alto)) #Le dice que haga la pantala de las medidas del alto y ancho
pygame.display.set_caption("Pong v.0 Juan Cabrera Aprendizaje Autonomo 2") #Que escriba el titulo en la barra de la ventana

#Aca ponemos los FPS a los que queremos que corra el juego
reloj = pygame.time.Clock()
FPS = 60

#Colores, barras, atributos
negro= (0,0,0)
blanco= (255, 255, 255)
ancho_barra = 10
alto_barra = 100
velocidad_barra = 7
bola = 10
velocidad_bola = 5


#Variable de Barra izquierda, su posicion y medidas
barra_izquierda = pygame.Rect(
    50,                         #posicion de x
    alto // 2 - alto_barra // 2, #posicion de y
    ancho_barra, #ancho de la barra
    alto_barra  #alto de la barra
)

#Variable de Barra derecha, posicion y medidas
barra_derecha = pygame.Rect(
    ancho - 50,
    alto // 2 - alto_barra // 2,
    ancho_barra,
    alto_barra
)

#Variable de Bola, posicion y medidas
bola_centro = pygame.Rect(
    ancho- 400,
    alto - 300,
    bola,
    bola

)
#asignamos la velocidad de la bola en ambas direcciones
velocidad_bola_x = velocidad_bola
velocidad_bola_y = velocidad_bola

#definimos una funcion que se llama reseteo bola y hace esto
def reseteo_bola():
    global velocidad_bola_x, velocidad_bola_y #cambia esta variables globalmente

    #pone la bola en el centro siempre que se resetee
    bola_centro.center = (ancho - 400, alto - 300)
    #elige al azar si salir izq o der
    dir_x = random.choice ([-1,1])
    #elige al azar si salir arriba o abajo
    dir_y = random.choice ([-1,1])
    #asignamos velocidades
    velocidad_bola_x = velocidad_bola * dir_x
    velocidad_bola_y = velocidad_bola * dir_y



#Bucle del juego
correr = True
while correr:

    #Empieza la velocidad del juego en FPS puestos anteriormente
    reloj.tick(FPS)

    #Este bucle permite cerrar el juego
    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            correr = False

    #Leer el teclado
    teclado = pygame.key.get_pressed()
    
    #Aqui el teclado lee que teclas se aplastan y que pasa cuando se aplastan en una direccion x o y (en este caso y)
    if teclado [pygame.K_w]:
        barra_izquierda.y -= velocidad_barra
    if teclado[pygame.K_s]:
        barra_izquierda.y += velocidad_barra  

    if teclado[pygame.K_UP]:
        barra_derecha.y -= velocidad_barra
    if teclado[pygame.K_DOWN]:
        barra_derecha.y += velocidad_barra

    #Protegemos los bordes de la pantalla para que las barras no se salgan del borde, el top y bottom son cordeanas de Y del rectangulo
    #Si el tope sube a 0 para en 0 y si baja mas que alto la regresamos al limite
    if barra_derecha.top < 0:
        barra_derecha.top = 0

    if barra_derecha.bottom > alto:
        barra_derecha.bottom = alto

    if barra_izquierda.top < 0:
        barra_izquierda.top = 0

    if barra_izquierda.bottom > alto:
        barra_izquierda.bottom = alto


    #Movimiento de la bola y se movera con movimiento randomizado
    bola_centro.x += velocidad_bola_x
    bola_centro.y += velocidad_bola_y

    #Rebote con bordes,si la bola toca del borde de arriba o abajo
    if bola_centro.top <= 0 or bola_centro.bottom >= alto: 
        velocidad_bola_y *=-1 #cambia de direccion

    #si la bola toca el borde de derecha o izquierda
    if bola_centro.left <=-100 or bola_centro.right >= ancho+100: 
        reseteo_bola() #Resetea la bola al momento de pasar los bordes

    #COn el colliderect detecta cuando 2 rectangulos se superponen por ende activa el bucle de que cuando choquen con barra cambien de direccion
    if bola_centro.colliderect(barra_izquierda) and velocidad_bola_x < 0:
        velocidad_bola_x *= -1
    if bola_centro.colliderect(barra_derecha) and velocidad_bola_x > 0:
        velocidad_bola_x *= -1


    
    #Pintamos la pantalla, dibujamos barras, dibujamos bola
    ventana.fill(negro)
    

    #dibujar objetos del juego sobre la ventana de que color y las coords de la barra izquierda 
    pygame.draw.rect (ventana, blanco, barra_izquierda) 
    pygame.draw.rect (ventana, blanco, barra_derecha)
    pygame.draw.ellipse (ventana, blanco, bola_centro)

    #Actualizar la pantalla para que aparezca lo que dibujamos arriba
    pygame.display.flip()

#Salir de pygame
pygame.quit()
sys.exit

#   BIBLIOGRAFIA PARA REALIZAR EL CODIGO
#       https://www.pygame.org/docs/
#       https://docs.python.org/es/3.10/library/random.html
#       https://www.w3schools.com/python/python_functions.asp
#       https://docs.python.org/3/library/sys.html
