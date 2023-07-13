import pygame
from constantes import *




class Item(pygame.sprite.Sprite):
    def __init__(self, x,y,tipo_item):
        pygame.sprite.Sprite.__init__(self)
        pocion_image = pygame.image.load("img/icons/pocion_pokemon.png").convert_alpha()
        pocion_energia = pygame.image.load("img/icons/PP.png").convert_alpha()
        pocion_image = pygame.transform.scale(pocion_image,(int(pocion_image.get_width())*0.8, int(pocion_image.get_height())*0.8))
        pocion_energia = pygame.transform.scale(pocion_energia,(int(pocion_energia.get_width())*0.7, int(pocion_energia.get_height())*0.7))
        items = {"Pocion": pocion_image, "Energia": pocion_energia}
        self.tipo_item = tipo_item
        self.image = items[self.tipo_item]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self,player,screen_scroll):

        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self,player):
            if self.tipo_item == "Pocion":
                player.vida += 25
                if player.vida > player.vida_maxima:
                    player.vida = player.vida_maxima
            elif self.tipo_item == "Energia":
                player.energia += 10
                print(player.energia)
            
            self.kill()

class Decoracion(pygame.sprite.Sprite):
    def __init__(self, x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self,screen_scroll):
        self.rect.x += screen_scroll

class Agua(pygame.sprite.Sprite):
    def __init__(self, x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self,screen_scroll):
        self.rect.x += screen_scroll

class Pokecenter(pygame.sprite.Sprite):
    def __init__(self, x,y,img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()+2))

    def update(self,screen_scroll):
        self.rect.x += screen_scroll