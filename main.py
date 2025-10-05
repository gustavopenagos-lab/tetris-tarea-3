from tetris import *

def main():

    # ==========================================================
    # INTERFAZ GRÁFICA
    # ==========================================================

    # ==========================================================
    # CONFIGURACIÓN DE LA INTERFAZ GRÁFICA

    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tetris")
    reloj = pygame.time.Clock()

    # ==========================================================
    # VARIABLES DE JUEGO INICIALES
    
    grid = crear_grid()
    pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
    game_over = False
    contador_caida = 0
    velocidad_caida = 30  # cuanto menor, más rápido cae
    score = 0   # Variable de puntaje
    pausado = False     # Variable de pausa

    # ==========================================================
    # BUCLE PRINCIPAL DEL JUEGO

    while True:
        pantalla.fill(NEGRO)

                # ==========================================================
        # PAUSA DEL JUEGO
        # ==========================================================
        if pausado:
            fuente = pygame.font.SysFont("Arial", 40)
            texto = fuente.render("PAUSA", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 60, ALTO // 2 - 20))
            
            # Actualiza pantalla para mostrar "PAUSA"
            pygame.display.flip()
            
            # Mientras está pausado, espera eventos (para poder reanudar con 'P')
            pausando = True
            while pausando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_p:  # reanudar
                            pausado = False
                            pausando = False
                            break
                reloj.tick(10)  # controla la velocidad del bucle en pausa
        
        # ==========================================================
        # PAUSA DELJUEGO
        # ==========================================================

        if pausado:
            fuente = pygame.font.SysFont("Arial", 40)
            texto = fuente.render("PAUSA", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 60, ALTO // 2 - 20))


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

                    # 🔹 Limpiar líneas después de fijar
                    grid, lineas = limpiar_lineas(grid)
                    score += lineas * 100  # cada línea vale 100 puntos

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
            elif evento.type == pygame.KEYDOWN and not game_over:
                # Movimiento a la izquierda
                if evento.key == pygame.K_LEFT: # Mover con ←  
                    pieza.x -= 1
                    if colision(pieza, grid):  
                        pieza.x += 1
                # Movimiento a la derecha
                elif evento.key == pygame.K_RIGHT:  # Mover con →
                    pieza.x += 1
                    if colision(pieza, grid):
                        pieza.x -= 1

            # Rotación de la pieza
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:  # Rotar con ↑
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

                if evento.key == pygame.K_p: # Pausa con P 
                    pausado = not pausado
            
            # Reiniciar todo el juego
            if game_over and evento.type == pygame.KEYDOWN and evento.key != pygame.K_p:
                grid = crear_grid()
                pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
                game_over = False
                score = 0
                pausado = False

        # ------------------------------------------------------
        # MOSTRAR PUNTAJE EN PANTALLA
        dibujar_grid(pantalla, grid)
        mostrar_puntaje(pantalla, score)

        # ------------------------------------------------------
        # ACTUALIZAR PANTALLA Y RITMO DEL JUEGO ----------------
        # ------------------------------------------------------

        if game_over:
            # Fondo semitransparente
            overlay = pygame.Surface((ANCHO, ALTO))
            overlay.set_alpha(150)  # nivel de transparencia (0–255)
            overlay.fill((0, 0, 0))  # negro
            pantalla.blit(overlay, (0, 0))

            # Texto de Game Over encima
            fuente = pygame.font.SysFont("Arial", 40, bold=True)
            texto = fuente.render("GAME OVER", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 100, ALTO // 2 - 20))


        pygame.display.flip()
        reloj.tick(30)

# ==========================================================
# PUNTO DE ENTRADA DEL PROGRAMA ============================
# ==========================================================

if __name__ == "__main__":
    main()
