import pygame
import csv
from constantes import *
from mundo import Mundo



def draw_bg(pantalla):
    pantalla.fill((0,0,0))
    width = cielo_img.get_width()
    for x in range(5):
        pantalla.blit(cielo_img.convert_alpha(),((x * width) - bg_scroll * 0.2, ALTO_PANTALLA - cielo_img.get_height()-250))
        pantalla.blit(montaña_img.convert_alpha(),((x * width) - bg_scroll * 0.5, ALTO_PANTALLA - montaña_img.get_height()-200))
        pantalla.blit(monte_img.convert_alpha(),((x * width) - bg_scroll *0.6, ALTO_PANTALLA - monte_img.get_height()-70))
        pantalla.blit(arbol_lejos_img.convert_alpha(),((x * width) - bg_scroll*0.6, ALTO_PANTALLA - arbol_lejos_img.get_height()-30))
        pantalla.blit(arbol_img.convert_alpha(),((x * width) - bg_scroll*0.8, ALTO_PANTALLA - arbol_img.get_height()-50))

pygame.init()




pantalla = pygame.display.set_mode((ALTO_PANTALLA,ALTO_PANTALLA))
pygame.display.set_caption("Pokemon Shootout")

# Frames
clock = pygame.time.Clock()


mundo = Mundo()
pokemon_ini, pokemon_2,largo_nivel  = mundo.procesar_data(data_mundo)

run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        pantalla.blit(cielo_menu_fondo.convert_alpha(),(0,0))
        pantalla.blit(oak_menu_img.convert_alpha(),(ANCHO_PANTALLA//2-oak_menu_img.get_width()+200,ALTO_PANTALLA- oak_menu_img.get_height()+50))
        if start_button.draw(pantalla):
            start_game = True
        if exit_button.draw(pantalla):
            run = False
    else:
        draw_bg(pantalla)
        mundo.draw_mundo(pantalla,screen_scroll)
        #ENERGIA
        font = pygame.font.SysFont("Arial Narrow", 30)
        texto = font.render(f"ENERGIA : {pokemon_ini.energia}", True, (255,255,255))
        pantalla.blit(texto,(10,35))
        #VIDA
        pygame.draw.rect(pantalla,ROJO,(10,75,150,30))
        pygame.draw.rect(pantalla,VERDE,(10,75,150 * (pokemon_ini.vida/pokemon_ini.vida_maxima),30))

        pokemon_ini.update()
        pokemon_ini.draw(pantalla)
        
        for enemy in enemy_group:
            enemy.movimiento_ia(pokemon_ini,pantalla,mundo.lista_obstaculos,screen_scroll)
            enemy.update()
            enemy.draw(pantalla)

        
        #update y dibujar grupos
        item_group.update(pokemon_ini,screen_scroll)
        bullet_grupo.update(pokemon_ini,pokemon_2,enemy_group,mundo.lista_obstaculos,screen_scroll)
        decoracion_group.update(screen_scroll)
        agua_group.update(screen_scroll)
        pokecenter_group.update(screen_scroll)


        item_group.draw(pantalla)
        bullet_grupo.draw(pantalla)
        decoracion_group.draw(pantalla)
        agua_group.draw(pantalla)
        pokecenter_group.draw(pantalla)


        if pokemon_ini.alive:
            if shoot:
                pokemon_ini.disparo()
                pokemon_ini.update_accion(4) #DISPARO
            elif pokemon_ini.jump_cooldown       :
                pokemon_ini.update_accion(2) # SALTAR
            elif (mover_left or mover_right) and mover_dash:
                pokemon_ini.update_accion(3) #DASH
            elif mover_left or mover_right:
                pokemon_ini.update_accion(1) # MOVER
            else: 
                pokemon_ini.update_accion(0) #Idle
            screen_scroll, nivel_completado = pokemon_ini.movimiento(mover_left,mover_right,mover_dash,mundo.lista_obstaculos,bg_scroll,largo_nivel)
            bg_scroll -= screen_scroll
            if nivel_completado:
                nivel += 1
                bg_scroll = 0
                data_mundo = reset_level()
                if nivel <= NIVELES:
                    with open(f"level{nivel}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile,delimiter=",")
                        for x,row in enumerate(reader):
                            for y,tile in enumerate(row):
                                data_mundo[x][y] = int(tile)     
                    mundo = Mundo()
                    pokemon_ini, pokemon_2,largo_nivel  = mundo.procesar_data(data_mundo)  
            if nivel > NIVELES:
                screen_scroll = 0
                pantalla.blit(diploma_img,(0,0))
                    
        else:
            screen_scroll = 0
            pantalla.blit(centro_pokemon_img_muerte,(0,0))
            if restart_button.draw(pantalla):
                bg_scroll = 0
                data_mundo = reset_level()
                # Cargamos la data del nivel
                with open(f"level{nivel}_data.csv", newline="") as csvfile:
                    reader = csv.reader(csvfile,delimiter=",")
                    for x,row in enumerate(reader):
                        for y,tile in enumerate(row):
                            data_mundo[x][y] = int(tile)     
                mundo = Mundo()
                pokemon_ini, pokemon_2,largo_nivel  = mundo.procesar_data(data_mundo)           

    for event in pygame.event.get():
        #Cerrar el juego
        if event.type == pygame.QUIT:
            run = False
        #Controles cuando apreta
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_left = True
            if event.key == pygame.K_d:
                mover_right = True
            if event.key == pygame.K_LSHIFT:
                mover_dash = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w and pokemon_ini.alive:
                pokemon_ini.jump = True
        #Controles cuando suelta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_left = False
            if event.key == pygame.K_d:
                mover_right = False
            if event.key == pygame.K_LSHIFT:
                mover_dash = False
            if event.key == pygame.K_SPACE:
                shoot = False




    pygame.display.update()

pygame.quit