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

    # ==========================================================
    # BUCLE PRINCIPAL DEL JUEGO

    while True:
        pantalla.fill(NEGRO)

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
        # TEXTO DE GAME OVER
        
        if game_over:
            fuente = pygame.font.SysFont("Arial", 40)
            texto = fuente.render("GAME OVER", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 100, ALTO // 2 - 20))

        # ------------------------------------------------------
        # EVENTOS DE TECLADO Y SISTEMA
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            # Movimiento lateral del jugador
            elif evento.type == pygame.KEYDOWN and not game_over:
                # Movimiento a la izquierda
                if evento.key == pygame.K_LEFT:
                    pieza.x -= 1
                    if colision(pieza, grid):  # Evita salirse o chocar
                        pieza.x += 1
                # Movimiento a la derecha
                elif evento.key == pygame.K_RIGHT:
                    pieza.x += 1
                    if colision(pieza, grid):
                        pieza.x -= 1

        # ------------------------------------------------------
        # ACTUALIZAR PANTALLA Y RITMO DEL JUEGO ----------------
        # ------------------------------------------------------

        pygame.display.flip()
        reloj.tick(30)

# ==========================================================
# PUNTO DE ENTRADA DEL PROGRAMA ============================
# ==========================================================

if __name__ == "__main__":
    main()
