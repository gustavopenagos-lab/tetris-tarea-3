import pygame
import random
from tetris import *
from interfaz import crear_pantalla, dibujar_grid, mostrar_puntaje, mostrar_pausa, mostrar_game_over

def main():

    # ==========================================================
    # INTERFAZ GRÁFICA
    # ==========================================================

    # ==========================================================
    # CONFIGURACIÓN DE LA INTERFAZ GRÁFICA

    pygame.init()
    pantalla = crear_pantalla()
    reloj = pygame.time.Clock()

    grid = crear_grid()
    pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
    game_over = False   # Variable de gameover
    pausado = False     # Variable de pausa
    score = 0       # Inicializar score/puntaje
    contador_caida = 0  ########################################################################### 
    velocidad_caida = 30    # Cuanto menor, más rapido cae

    # ==========================================================
    # BUCLE PRINCIPAL DEL JUEGO
    while True:
        pantalla.fill(NEGRO)

        # ==========================================================
        # PAUSA DEL JUEGO
        # ==========================================================
        if pausado:
            mostrar_pausa(pantalla)
            pausando = True
            
            # Mientras está pausado, espera eventos (para poder reanudar con 'P')   
            while pausando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:    # Reanudar con 'P'
                        pausado = False
                        pausando = False
                        break
                reloj.tick(10)  # controla la velocidad del bucle en pausa
            continue  # evita que se ejecute el resto del bucle mientras está en pausa

        # ==========================================================
        # CAÍDA AUTOMÁTICA DE LOS TETROMINOS
        # ==========================================================

        if not game_over:
            contador_caida += 1
            if contador_caida >= velocidad_caida:
                pieza.y += 1
                # Si colisiona, fijar pieza y generar otra
                if colision(pieza, grid):
                    pieza.y -= 1
                    fijar_pieza(pieza, grid)

                    # Limpiar líneas después de fijar
                    grid, lineas = limpiar_lineas(grid)
                    score += lineas * 100   # cada línea vale 100 puntos
                    pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
                    
                    # Si colisiona apenas aparece → Game Over
                    if colision(pieza, grid):
                        game_over = True
                contador_caida = 0

        # ------------------------------------------------------
        # DIBUJAR ELEMENTOS EN PANTALLA
        dibujar_grid(pantalla, grid)

        # Dibujar pieza activa (la que está cayendo)
        if not game_over:
            for i, fila in enumerate(pieza.forma):
                for j, valor in enumerate(fila):
                    if valor:
                        pygame.draw.rect(
                            pantalla,
                            pieza.color,
                            ((pieza.x + j) * TAM_BLOQUE,
                             (pieza.y + i) * TAM_BLOQUE,
                             TAM_BLOQUE, TAM_BLOQUE)
                        )

        # ------------------------------------------------------
        # EVENTOS DE TECLADO Y SISTEMA

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            # Movimiento lateral del jugador
            if evento.type == pygame.KEYDOWN:
                if not game_over:
                    # Movimiento a la izquierda
                    if evento.key == pygame.K_LEFT:     # Mover con ←  
                        pieza.x -= 1
                        if colision(pieza, grid):
                            pieza.x += 1
                    # Movimiento a la derecha
                    elif evento.key == pygame.K_RIGHT:  # Mover con →
                        pieza.x += 1
                        if colision(pieza, grid):
                            pieza.x -= 1
                    # Rotación de la pieza
                    elif evento.key == pygame.K_UP:     # Rotar con ↑
                        pieza.rotar(grid)
                    # Acelerar caída una posición
                    elif evento.key == pygame.K_DOWN:   # Bajar con ↓
                        pieza.y += 1
                        if colision(pieza, grid):
                            pieza.y -= 1
                    # Caída instantánea
                    elif evento.key == pygame.K_SPACE:  # Caída instantánea con [ESPACIO]
                        while not colision(pieza, grid):
                            pieza.y += 1
                        pieza.y -= 1
                        fijar_pieza(pieza, grid)
                        grid, lineas = limpiar_lineas(grid)
                        score += lineas * 100
                        pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
                    elif evento.key == pygame.K_p:  # Pausa con P 
                        pausado = not pausado
                else:
                    # Reiniciar todo el juego
                    grid = crear_grid()
                    pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
                    game_over = False
                    score = 0
                    pausado = False

        # Puntaje y Game Over
        mostrar_puntaje(pantalla, score)
        if game_over:
            mostrar_game_over(pantalla)

        # ------------------------------------------------------
        # ACTUALIZAR PANTALLA Y RITMO DEL JUEGO ----------------
        # ------------------------------------------------------

        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    main()