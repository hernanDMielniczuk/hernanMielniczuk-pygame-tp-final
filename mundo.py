import pygame
from constantes import *
from pokemon import Pokemon
from enemigo import Enemigo
from item import Item
from item import Decoracion
from item import Agua
from item import Pokecenter


class Mundo():
    def __init__(self) -> None:
        self.lista_obstaculos = []

    
    def procesar_data(self, data):
        self.largo_nivel = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = lista_tile[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile  <= 8:
                        self.lista_obstaculos.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        agua = Agua(x *TILE_SIZE,y * TILE_SIZE, img)
                        agua_group.add(agua)
                    elif tile >= 11 and tile <= 14:
                        decoracion = Decoracion(x *TILE_SIZE,y * TILE_SIZE,img)
                        decoracion_group.add(decoracion)
                    elif tile == 15: # jugador
                        pokemon_ini = Pokemon("player",x *TILE_SIZE,y * TILE_SIZE ,0.5,5,10)
                    elif tile == 16: # enemigo
                        pokemon_2 = Enemigo("enemy",x *TILE_SIZE,y * TILE_SIZE,0.5,3)
                        enemy_group.add(pokemon_2)
                    elif tile == 17: # pocion de vida
                        item_1 = Item(x *TILE_SIZE,y * TILE_SIZE,"Pocion")
                        item_group.add(item_1)
                    elif tile == 18: # pocion de energia
                        item_2 = Item(x *TILE_SIZE,y * TILE_SIZE,"Energia")
                        item_group.add(item_2)
                    elif tile == 20:
                        pokecenter = Pokecenter(x *TILE_SIZE,y * TILE_SIZE,img)
                        pokecenter_group.add(pokecenter)
                        pass
        return pokemon_ini, pokemon_2, self.largo_nivel

    def draw_mundo(self,donde,screen_scroll):
        for tile in self.lista_obstaculos:
            tile[1][0] += screen_scroll
            donde.blit(tile[0],tile[1])


