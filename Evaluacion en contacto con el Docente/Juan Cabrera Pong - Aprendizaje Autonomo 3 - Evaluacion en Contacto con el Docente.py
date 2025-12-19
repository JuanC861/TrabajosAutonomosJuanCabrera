# Proyecto: Aprendizaje Autonomo 2 - Pong 50%
# Requisitos:
#   - Librería pygame-ce (se instala en la terminal con: pip install pygame-ce)

import pygame #libreria util para la interfaz grafica y algunas funciones logicas del juego
import sys #esta libreria sirve para salir del juego
import random #libreria para tener valores random al momento de que la bola sale del centro
import os #util para poder dar direcciones a archivos mas facil

pygame.init() #Inicia el pygame
pygame.font.init() #Iniciamos las fuentes

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
corazon_altura = 16
corazon_esp = 10
boton_reiniciar = pygame.Rect(250, 350, 250, 60) #x,y,largo,alto
boton_salir = pygame.Rect(275, 420, 200, 60) #x,y,largo,alto
fuente = pygame.font.SysFont("consolas", 40)

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

#Creamos variables de las vidas
vidas_derecha = 3
vidas_izquierda = 3

#El os nos sirve para poder poner el directorio de un archivo mas facil
ruta_base = os.path.dirname(__file__)
ruta_corazon = os.path.join(ruta_base, "corazon.png")

#Nos carga la imagen
corazon = pygame.image.load(ruta_corazon).convert_alpha()
corazon = pygame.transform.scale(corazon,(corazon_altura, corazon_altura))

#Variable de mensaje para poner luego
mensaje=""

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

#Definimos funciona para dibujar corazones
def dibujar_cora():
    for i in range(vidas_izquierda):
        x=150+i * (corazon_altura + corazon_esp)
        y=20
        ventana.blit(corazon, (x,y))

    for i in range(vidas_derecha):
        x = ancho - 150 - corazon_altura - i * (corazon_altura + corazon_esp)
        y=20
        ventana.blit(corazon, (x,y))

#Bucle del inicio y juego
correr = True
juego_empezado = False

while correr:

    reloj.tick(FPS)

    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            correr = False
        elif not juego_empezado:
            if eventos.type == pygame.MOUSEBUTTONDOWN and eventos.button == 1:
                juego_empezado = True
                reseteo_bola()

    if not juego_empezado:
        ventana.fill(negro)
        texto_inicio = fuente.render("Clic para empezar", True, blanco)
        ventana.blit(
            texto_inicio,
            (
                ancho // 2 - texto_inicio.get_width() // 2,
                alto // 2 - texto_inicio.get_height() // 2
            )
        )
        pygame.display.flip()
        continue

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

    #Si la bola pasa perdemos vidas
    if bola_centro.left <=0:
        vidas_izquierda -=1
        reseteo_bola()

    elif  bola_centro.right >= ancho:
        vidas_derecha -=1
        reseteo_bola()

    #COn el colliderect detecta cuando 2 rectangulos se superponen por ende activa el bucle de que cuando choquen con barra cambien de direccion
    if bola_centro.colliderect(barra_izquierda) and velocidad_bola_x < 0: 
        velocidad_bola_x *= -1
        velocidad_bola_x += 1
    if bola_centro.colliderect(barra_derecha) and velocidad_bola_x > 0:
        velocidad_bola_x += 1
        velocidad_bola_x *= -1
        
        
    #Que pasa cuando llegas a 0 vidas?
    if vidas_izquierda <=0 or vidas_derecha <=0:
        if vidas_izquierda <=0:
            mensaje = "Jugador de la Derecha ganó!"
        elif vidas_derecha <=0:
            mensaje = "Jugador de la Izquierda ganó!"
        else:
            mensaje = "Ups.... esto no deberia pasar.."



        if vidas_izquierda <= 0 and vidas_derecha <= 0:
            mensaje = "Empate"
        elif vidas_izquierda <=0:
            mensaje = "Jugador de la Derecha ganó!"
        else:
            mensaje = "Jugador de la Izquierda ganó!"

    #Bucle: Entrar a pantalla Final
        esperando = True 
        while esperando:
            for eventos in pygame.event.get():
                if eventos.type == pygame.QUIT:
                    correr = False
                    esperando = False

                elif eventos.type == pygame.MOUSEBUTTONDOWN and eventos.button == 1:
                    if boton_reiniciar.collidepoint(eventos.pos):
                        # Reiniciar juego
                        vidas_izquierda = 3
                        vidas_derecha   = 3
                        barra_izquierda.y = alto // 2 - alto_barra // 2
                        barra_derecha.y   = alto // 2 - alto_barra // 2
                        reseteo_bola()
                        mensaje = ""
                        esperando = False  # salir de la pantalla de menu

                    elif boton_salir.collidepoint(eventos.pos):
                        correr = False      # cerrar juego
                        esperando = False

            # Dibujar pantalla de menu
            ventana.fill(negro)
            dibujar_cora()

            # Mensaje de quien gano
            texto = fuente.render(mensaje, True, blanco)
            ventana.blit(
                texto, #se centra
                (
                    ancho // 2 - texto.get_width() // 2,
                    alto  // 2 - texto.get_height() // 2 - 40
                )
            )

            # Botones dibujados
            pygame.draw.rect(ventana, blanco, boton_reiniciar, 2)
            pygame.draw.rect(ventana, blanco, boton_salir, 2)

            #texto de botones
            texto_reiniciar = fuente.render("Reiniciar", True, blanco)
            texto_salir     = fuente.render("Salir", True, blanco)

            ventana.blit(
                texto_reiniciar,
                (
                    boton_reiniciar.centerx - texto_reiniciar.get_width() // 2,
                    boton_reiniciar.centery - texto_reiniciar.get_height() // 2
                )
            )

            ventana.blit(
                texto_salir,
                (
                    boton_salir.centerx - texto_salir.get_width() // 2,
                    boton_salir.centery - texto_salir.get_height() // 2
                )
            )

            pygame.display.flip()
            reloj.tick(FPS)

        # Si eligió salir o cerró la ventana, salimos del while principal
        if not correr:
            break

        # Si eligió reiniciar, volvemos al ciclo del while
        continue


    #Pintamos la pantalla, dibujamos barras, dibujamos bola
    ventana.fill(negro)
    
    #dibujar objetos del juego sobre la ventana de que color y las coords de la barra izquierda 
    pygame.draw.rect (ventana, blanco, barra_izquierda) 
    pygame.draw.rect (ventana, blanco, barra_derecha)
    pygame.draw.ellipse (ventana, blanco, bola_centro)
    dibujar_cora()
    
    #Actualizar la pantalla para que aparezca lo que dibujamos arriba
    pygame.display.flip()

#Salir de pygame
pygame.quit()
sys.exit()

#   BIBLIOGRAFIA PARA REALIZAR EL CODIGO
#       https://www.pygame.org/docs/
#       https://docs.python.org/es/3.10/library/random.html
#       https://www.w3schools.com/python/python_functions.asp
#       https://docs.python.org/3/library/sys.html
#       https://docs.python.org/3/library/os.path.html