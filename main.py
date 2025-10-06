from tetris import *
import pygame
import random

def main():

    # ==========================================================
    # CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
    # ==========================================================
    pygame.init()
    
    # 🔹 Aumentamos el ancho para mostrar la pieza siguiente
    ANCHO_TOTAL = ANCHO + 150  
    pantalla = pygame.display.set_mode((ANCHO_TOTAL, ALTO))
    pygame.display.set_caption("Tetris Mejorado")
    reloj = pygame.time.Clock()

    # ==========================================================
    # VARIABLES DE JUEGO INICIALES
    # ==========================================================
    grid = crear_grid()
    pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
    siguiente_pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))

    game_over = False
    contador_caida = 0
    velocidad_caida = 30
    score = 0
    pausado = False

    # ==========================================================
    # BUCLE PRINCIPAL DEL JUEGO
    # ==========================================================
    while True:
        pantalla.fill(NEGRO)

        # ==========================================================
        # CAÍDA AUTOMÁTICA
        # ==========================================================
        if not game_over:
            contador_caida += 1
            if contador_caida >= velocidad_caida:
                pieza.y += 1
                if colision(pieza, grid):
                    pieza.y -= 1
                    fijar_pieza(pieza, grid)
                    grid, lineas = limpiar_lineas(grid)
                    score += lineas * 100
                    
                    # 🔹 Cambiar a la siguiente pieza
                    pieza = siguiente_pieza
                    siguiente_pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))

                    if colision(pieza, grid):
                        game_over = True
                contador_caida = 0

        # ==========================================================
        # DIBUJAR TODO
        # ==========================================================
        dibujar_grid(pantalla, grid)

        # Dibujar pieza actual
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

        # Mostrar puntaje
        mostrar_puntaje(pantalla, score)

        # 🔹 Mostrar la próxima pieza
        mostrar_siguiente_pieza(pantalla, siguiente_pieza)

        # ==========================================================
        # EVENTOS
        # ==========================================================
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.KEYDOWN and not game_over:
                if evento.key == pygame.K_LEFT:
                    pieza.x -= 1
                    if colision(pieza, grid):
                        pieza.x += 1
                elif evento.key == pygame.K_RIGHT:
                    pieza.x += 1
                    if colision(pieza, grid):
                        pieza.x -= 1
                elif evento.key == pygame.K_UP:
                    pieza.rotar(grid)
                elif evento.key == pygame.K_DOWN:
                    pieza.y += 1
                    if colision(pieza, grid):
                        pieza.y -= 1
                elif evento.key == pygame.K_SPACE:
                    while not colision(pieza, grid):
                        pieza.y += 1
                    pieza.y -= 1
                    fijar_pieza(pieza, grid)
                    grid, lineas = limpiar_lineas(grid)
                    score += lineas * 100
                    pieza = siguiente_pieza
                    siguiente_pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
                elif evento.key == pygame.K_p:
                    pausado = not pausado

        # ==========================================================
        # GAME OVER
        # ==========================================================
        if game_over:
            fuente = pygame.font.SysFont("Arial", 40, bold=True)
            texto = fuente.render("GAME OVER", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 100, ALTO // 2 - 20))

        pygame.display.flip()
        reloj.tick(30)


# ==========================================================
# NUEVA FUNCIÓN PARA MOSTRAR LA SIGUIENTE PIEZA
# ==========================================================
def mostrar_siguiente_pieza(pantalla, pieza):
    fuente = pygame.font.SysFont("Arial", 25)
    texto = fuente.render("Siguiente:", True, BLANCO)
    pantalla.blit(texto, (ANCHO + 20, 50))

    for i, fila in enumerate(pieza.forma):
        for j, valor in enumerate(fila):
            if valor:
                pygame.draw.rect(
                    pantalla,
                    pieza.color,
                    (ANCHO + 40 + j * TAM_BLOQUE,
                     100 + i * TAM_BLOQUE,
                     TAM_BLOQUE,
                     TAM_BLOQUE)
                )

# ==========================================================
# EJECUCIÓN PRINCIPAL
# ==========================================================
if __name__ == "__main__":
    main()
