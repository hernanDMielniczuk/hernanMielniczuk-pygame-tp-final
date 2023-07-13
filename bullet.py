import pygame
from constantes import *



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x,y,direction,scale,tipo_disparo):
        pygame.sprite.Sprite.__init__(self)

        self.speed = 13
        self.tipo_disparo = tipo_disparo
        self.image = pygame.image.load(f"img/icons/{tipo_disparo}.png").convert_alpha() # AGREUGUE EL TIPO DISPARO CAMBIAR EN ENEMIGO Y POKEMON
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self,player,enemy,enemy_g,lista,screen_scroll):
        #movimiento de la bala
        self.rect.x += (-self.direction * self.speed) + screen_scroll

        #eliminar balas si salen de la pantalla
        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA:
            self.kill()

        for tile in lista:
            if tile[1].colliderect(self.rect):
                self.kill()
        

        #Colision
        if pygame.sprite.spritecollide(player,bullet_grupo,False):
            if player.alive:
                player.vida -= 15
                self.kill()
        for enemy in enemy_g:
            if pygame.sprite.spritecollide(enemy,bullet_grupo,False):
                if enemy.alive:
                    enemy.vida -= 25
                    self.kill()