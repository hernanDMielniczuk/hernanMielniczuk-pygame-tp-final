import pygame
import random
from constantes import *
from bullet import Bullet




class Enemigo(pygame.sprite.Sprite):
    def __init__(self,tipo_poke , x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.tipo_poke = tipo_poke
        self.speed = speed
        self.cooldown_disparo = 0
        self.vida = 100
        self.vida_maxima = self.vida
        self.dash_speed = 10
        self.direction = 1
        self.poder_salto = 0
        self.jump = False
        self.jump_cooldown = True
        self.flip = False
        self.lista_animacion = []
        self.indice_animacion = 0
        self.accion_ocurriendo = 0
        self.update_time = pygame.time.get_ticks()
        self.rango_movimiento = 0
        self.quieto = False
        self.tiempo_quieto = 0
        self.vision = pygame.Rect(0,0,230,20)

        #cargar imagenes de jugador
        tipos_animacion = {"IdleP":6,"WalkP":8,"JumpP":0,"DashP":0,"ShootP":10,"DeathP":3}
        for animacion in tipos_animacion:
            cantidad_fotos = tipos_animacion[animacion]

            lista_aux = []
            for i in range(cantidad_fotos):
                img = pygame.image.load("img/{0}/{1}/{2}.png".format(self.tipo_poke,animacion,i))
                img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
                lista_aux.append(img)
            self.lista_animacion.append(lista_aux)


        self.img = self.lista_animacion[self.accion_ocurriendo][self.indice_animacion]
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.ancho = self.img.get_width()
        self.alto = self.img.get_height()

    def update(self):
        self.update_animacion()
        self.check_vivo()
        
        if self.cooldown_disparo > 0:
            self.cooldown_disparo -= 1

    def movimiento(self, mover_left, mover_right,mover_dash,lista):
        dx = 0
        dy = 0

        #Chequeamos el movimineto

        if mover_left:
            dx =  -self.speed
            self.flip = False
            self.direction = 1
            if mover_dash:
                dx = -self.dash_speed

        if mover_right:
            dx = self.speed
            self.flip = True
            self.direction = -1
            if mover_dash:
                dx = self.dash_speed
        

        #Gravedad
        self.poder_salto += GRAVEDAD
        if self.poder_salto > 10:
            self.poder_salto
        dy += self.poder_salto

        #CHEQUEAMOS CON EL SUELO 
        for tile in lista:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.ancho, self.alto):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.ancho, self.alto):
                if self.poder_salto < 0:
                    self.poder_salto = 0
                    dy = tile[1].bottom - self.rect.top
                if self.poder_salto >= 0:
                    self.poder_salto = 0
                    dy = tile[1].top - self.rect.bottom
                    self.jump_cooldown = False

        #Update de movimiento
        self.rect.x += dx
        self.rect.y += dy



    def disparo(self):
        if self.cooldown_disparo == 0:
            self.cooldown_disparo = 50
            bullet = Bullet(self.rect.centerx + (0.6*self.rect.size[0] * -self.direction),self.rect.centery,self.direction,0.3,"Fuego")
            bullet_grupo.add(bullet)

    def movimiento_ia(self,player, pantalla,lista,screen_scroll):
        if self.alive and player.alive:
            if random.randint(1,300) == 3:
                self.update_accion(0)
                self.quieto = True
                self.tiempo_quieto = 50
            if self.vision.colliderect(player.rect):
                self.update_accion(4) # DISPARAR
                self.disparo()
            else:
                if self.quieto == False:
                    if self.direction == 1:
                        ia_movimiento_derecha = False
                    else:
                        ia_movimiento_derecha = True 

                    ia_movimiento_izquierda = not ia_movimiento_derecha
                    self.movimiento(ia_movimiento_izquierda,ia_movimiento_derecha,False,lista)
                    self.update_accion(1)
                    self.rango_movimiento += 1
                    self.vision.center = (self.rect.centerx + 120 * -self.direction, self.rect.centery)
                    if self.rango_movimiento > TILE_SIZE:
                        self.direction *= -1
                        self.rango_movimiento *= -1
                else:
                    self.tiempo_quieto -= 1
                    if self.tiempo_quieto == 0:
                        self.quieto = False
        elif player.alive == False:
            self.update_accion(0)

        #scroll
        self.rect.x += screen_scroll


    


    def update_animacion(self):
        #
        ANIMACION_TIEMPO = 100
        #
        self.img = self.lista_animacion[self.accion_ocurriendo][self.indice_animacion]

        # Chequeamos el reloj para ver cada cuanto cambiamos la animacion

        if pygame.time.get_ticks() - self.update_time > ANIMACION_TIEMPO:
            self.update_time = pygame.time.get_ticks()
            self.indice_animacion += 1
        # Restarteamos la animacion
        if self.indice_animacion >= len(self.lista_animacion[self.accion_ocurriendo]):
            if self.accion_ocurriendo == 5: #muerte
                self.indice_animacion = len(self.lista_animacion[self.accion_ocurriendo]) - 1                    
            else:
                self.indice_animacion = 0


    def update_accion(self,accion_nueva):
        if accion_nueva != self.accion_ocurriendo:
            self.accion_ocurriendo = accion_nueva
            self.indice_animacion = 0
            self.update_time = pygame.time.get_ticks()


    def check_vivo(self):
        if self.vida <= 0:
            self.vida = 0
            self.speed = 0
            self.alive = False
            self.update_accion(5) #ANIMACION MUERTE
    
    def draw(self,donde):
        donde.blit(pygame.transform.flip (self.img,self.flip,False), self.rect)
