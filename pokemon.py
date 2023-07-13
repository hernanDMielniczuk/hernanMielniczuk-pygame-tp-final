import pygame
from constantes import *
from bullet import Bullet




class Pokemon(pygame.sprite.Sprite):
    def __init__(self,tipo_poke , x,y,scale,speed,energia):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.tipo_poke = tipo_poke
        self.speed = speed
        self.cooldown_disparo = 0
        self.energia = energia
        self.vida = 100
        self.vida_maxima = self.vida
        self.dash_speed = 8
        self.direction = 1
        self.poder_salto = 0
        self.jump = False
        self.jump_cooldown = True
        self.flip = False
        self.lista_animacion = []
        self.indice_animacion = 0
        self.accion_ocurriendo = 0
        self.update_time = pygame.time.get_ticks()

        #cargar imagenes de jugador
        tipos_animacion = {"IdleP":3,"WalkP":6,"JumpP":4,"DashP":5,"ShootP":3,"DeathP":5}
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




    def movimiento(self, mover_left, mover_right,mover_dash,lista,scroll_total,largo_nivel):

        screen_scroll = 0

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
        

        if self.jump == True and self.jump_cooldown == False:
            self.poder_salto = -20
            self.jump = False
            self.jump_cooldown = True


        #Gravedad
        self.poder_salto += GRAVEDAD
        if self.poder_salto > 10:
            self.poder_salto
        dy += self.poder_salto

        #TEMPORALMENTE CHEQUEAMOS CON EL SUELO (LINEA ROJA)
        for tile in lista:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.ancho, self.alto):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.ancho, self.alto):
                if self.poder_salto < 0:
                    self.poder_salto = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.poder_salto >= 0:
                    self.poder_salto = 0
                    self.jump_cooldown = False
                    dy = tile[1].top - self.rect.bottom

        #Muertes entorno
        if pygame.sprite.spritecollide(self, agua_group, False):
            self.vida = 0
        
        if self.rect.bottom > ALTO_PANTALLA + 100:
            self.vida = 0

        # Salida
        nivel_completado = False
        if pygame.sprite.spritecollide(self, pokecenter_group, False):
            nivel_completado = True
        
        #Limites de la pantalla
        if self.rect.left + dx < 0 or self.rect.right + dx > ANCHO_PANTALLA:
            dx = 0

        #Update de movimiento
        self.rect.x += dx
        self.rect.y += dy

        #Update de scroll
        if (self.rect.right > ANCHO_PANTALLA - SCROLL_UMBRAL and scroll_total < (largo_nivel * TILE_SIZE) - ANCHO_PANTALLA) or (self.rect.left < SCROLL_UMBRAL and scroll_total > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx
    
        return screen_scroll, nivel_completado

    def disparo(self):
        if self.cooldown_disparo == 0 and self.energia > 0:
            self.cooldown_disparo = 50
            bullet = Bullet(self.rect.centerx + (0.9*self.rect.size[0] * -self.direction),self.rect.centery,self.direction,0.3,"Bubble")
            bullet_grupo.add(bullet)
            self.energia -= 1
        

        

    def update_animacion(self):
        #
        ANIMACION_TIEMPO = 200
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
            if self.accion_ocurriendo == 3: # dash
                self.indice_animacion = len(self.lista_animacion[self.accion_ocurriendo]) - 2
            if self.accion_ocurriendo == 4: # shoot
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
            self.update_accion(5) #ANMIACION MUERTE
    
    def draw(self,donde):

        donde.blit(pygame.transform.flip (self.img,self.flip,False), self.rect)

