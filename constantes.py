import pygame
import csv
import button


ANCHO_PANTALLA = 800
ALTO_PANTALLA = 640  #int(ANCHO_PANTALLA * 0.8)
FPS = 60
BLANCO = (255,255,255)
ROJO = (255,0,0)
VERDE = (0,255,0)

SCROLL_UMBRAL = 300

GRAVEDAD = 1

FILAS = 16
COLUMNAS = 150
TILE_SIZE = ALTO_PANTALLA // FILAS
TILE_NUM = 21
NIVELES = 3
screen_scroll = 0
bg_scroll = 0
nivel = 1
start_game = False

mover_left = False
mover_right = False
mover_dash = False
shoot = False

#IMAGENES PARA EL FONDO
cielo_img = pygame.image.load("img/background/cielo3.png")
montaña_img = pygame.image.load("img/background/montaña_lejos.png")
monte_img = pygame.image.load("img/background/montaña_cerca.png")
arbol_lejos_img = pygame.image.load("img/background/arbol_lejos.png")
arbol_img = pygame.image.load("img/background/arbol_cerca.png")


#IMAGEN MENU
oak_menu_img = pygame.image.load("img/oak.png")
oak_menu_img = pygame.transform.scale(oak_menu_img,(int(oak_menu_img.get_width())//2,int(oak_menu_img.get_height())//2 + 50))
cielo_menu_fondo = pygame.image.load("img/fondo_menu.png")
cielo_menu_fondo = pygame.transform.scale(cielo_menu_fondo,(int(cielo_menu_fondo.get_width()),int(cielo_menu_fondo.get_height())+230))
centro_pokemon_img_muerte = pygame.image.load("img/centro_pokemon.png")
centro_pokemon_img_muerte = pygame.transform.scale(centro_pokemon_img_muerte,(int(centro_pokemon_img_muerte.get_width()*2),int(centro_pokemon_img_muerte.get_height()*3)+20))
start_boton_img = pygame.image.load("img/start_boton.png")
exit_boton_img = pygame.image.load("img/exit_btn.png")
restart_boton_img = pygame.image.load("img/restart_btn.png")
diploma_img = pygame.image.load("img/diploma.png")
diploma_img = pygame.transform.scale(diploma_img,(int(diploma_img.get_width())*3.5+100,int(diploma_img.get_height())*2+100))



start_button = button.Button(ANCHO_PANTALLA // 2 - 400, ALTO_PANTALLA // 2 - 150, start_boton_img, 1)
exit_button = button.Button(ANCHO_PANTALLA // 2  - 400, ALTO_PANTALLA // 2 , exit_boton_img, 1)
restart_button = button.Button(ANCHO_PANTALLA // 2 -300, ALTO_PANTALLA // 2 + 50, restart_boton_img, 1)


bullet_grupo = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
decoracion_group = pygame.sprite.Group()
agua_group = pygame.sprite.Group()
pokecenter_group = pygame.sprite.Group()


lista_tile = []
for x in range(TILE_NUM):
    img = pygame.image.load(f"img/tile/{x}.png")
    img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
    lista_tile.append(img)


#CREAMOS LOS NIVELES
data_mundo = []
for columna in range(COLUMNAS):
    r = [-1]* COLUMNAS
    data_mundo.append(r)
# Cargamos la data del nivel
with open(f"level{nivel}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile,delimiter=",")
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):
            data_mundo[x][y] = int(tile)

def reset_level():
    bullet_grupo.empty()
    enemy_group.empty()
    item_group.empty()
    decoracion_group.empty()
    agua_group.empty()
    pokecenter_group.empty()

    data = []
    for columna in range(COLUMNAS):
        r = [-1]* COLUMNAS
        data.append(r)
    
    return data