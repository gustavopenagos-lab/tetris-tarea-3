from tetris import *

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tetris")
    reloj = pygame.time.Clock()

    grid = crear_grid()
    pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
    game_over = False
    contador_caida = 0
    velocidad_caida = 30  # cuanto menor, más rápido cae

    while True:
        pantalla.fill(NEGRO)

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

        # Dibujar tablero
        dibujar_grid(pantalla, grid)

        # Dibujar pieza activa
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

        # Texto de Game Over
        if game_over:
            fuente = pygame.font.SysFont("Arial", 40)
            texto = fuente.render("GAME OVER", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 100, ALTO // 2 - 20))

        # --- Eventos del teclado y del sistema ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            # Movimiento lateral
            elif evento.type == pygame.KEYDOWN and not game_over:
                if evento.key == pygame.K_LEFT:
                    pieza.x -= 1
                    if colision(pieza, grid):  # Evita salirse o chocar
                        pieza.x += 1
                elif evento.key == pygame.K_RIGHT:
                    pieza.x += 1
                    if colision(pieza, grid):
                        pieza.x -= 1


        pygame.display.flip()
        reloj.tick(30)

if __name__ == "__main__":
    main()
