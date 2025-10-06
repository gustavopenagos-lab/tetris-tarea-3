import pygame
import random
from tetris import Pieza, TETROMINOS, crear_grid, colision, fijar_pieza, limpiar_lineas, actualizar_puntuacion

pygame.init()

# -------------------------------------------------------------
# CONFIGURACIÓN BÁSICA
# -------------------------------------------------------------
TAM_BLOQUE = 30
COLUMNAS = 10
FILAS = 20
ANCHO_TABLERO = COLUMNAS * TAM_BLOQUE
ALTO_TABLERO = FILAS * TAM_BLOQUE
ANCHO_LATERAL = 150
ANCHO_TOTAL = ANCHO_TABLERO + ANCHO_LATERAL
ALTO_TOTAL = ALTO_TABLERO

NEGRO = (0, 0, 0)
GRIS = (40, 40, 40)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)

pantalla = pygame.display.set_mode((ANCHO_TOTAL, ALTO_TOTAL))
pygame.display.set_caption("Tetris con Dificultad")

fuente = pygame.font.Font(None, 36)
fuente_titulo = pygame.font.Font(None, 60)

# -------------------------------------------------------------
# MENÚ PRINCIPAL
# -------------------------------------------------------------
def menu_principal():
    opciones = ["Fácil", "Medio", "Difícil"]
    while True:
        pantalla.fill(NEGRO)
        titulo = fuente_titulo.render("TETRIS", True, AMARILLO)
        pantalla.blit(titulo, (ANCHO_TOTAL // 2 - 80, 100))
        for i, texto in enumerate(opciones):
            color = BLANCO
            opcion = fuente.render(f"{i+1}. {texto}", True, color)
            pantalla.blit(opcion, (ANCHO_TOTAL // 2 - 70, 250 + i * 60))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return 800
                elif evento.key == pygame.K_2:
                    return 500
                elif evento.key == pygame.K_3:
                    return 300

# -------------------------------------------------------------
# DIBUJAR TABLERO Y ELEMENTOS
# -------------------------------------------------------------
def dibujar_grid(pantalla, grid):
    for y in range(FILAS):
        for x in range(COLUMNAS):
            valor = grid[y][x]
            rect = pygame.Rect(x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
            if valor:
                pygame.draw.rect(pantalla, valor, rect)
            pygame.draw.rect(pantalla, GRIS, rect, 1)

def mostrar_puntaje_y_siguiente(pantalla, score, siguiente_pieza):
    pygame.draw.rect(pantalla, (20, 20, 20), (ANCHO_TABLERO, 0, ANCHO_LATERAL, ALTO_TABLERO))
    pygame.draw.line(pantalla, BLANCO, (ANCHO_TABLERO, 0), (ANCHO_TABLERO, ALTO_TABLERO), 3)
    x_inicio = ANCHO_TABLERO + 15
    y_inicio = 50
    texto = fuente.render(f"Puntaje: {score}", True, BLANCO)
    pantalla.blit(texto, (x_inicio, y_inicio))
    texto2 = fuente.render("Siguiente:", True, BLANCO)
    pantalla.blit(texto2, (x_inicio, y_inicio + 60))
    for i, fila in enumerate(siguiente_pieza.forma):
        for j, valor in enumerate(fila):
            if valor:
                rect = pygame.Rect(
                    x_inicio + j * TAM_BLOQUE,
                    y_inicio + 120 + i * TAM_BLOQUE,
                    TAM_BLOQUE, TAM_BLOQUE
                )
                pygame.draw.rect(pantalla, siguiente_pieza.color, rect)
                pygame.draw.rect(pantalla, GRIS, rect, 1)

# -------------------------------------------------------------
# ESTADOS DEL JUEGO
# -------------------------------------------------------------
def mostrar_pausa(pantalla):
    texto = fuente.render("PAUSA", True, AMARILLO)
    pantalla.blit(texto, (ANCHO_TABLERO // 2 - 40, ALTO_TABLERO // 2))

def mostrar_game_over(pantalla):
    texto = fuente.render("GAME OVER", True, ROJO)
    pantalla.blit(texto, (ANCHO_TABLERO // 2 - 80, ALTO_TABLERO // 2 - 20))
    texto2 = fuente.render("Presiona cualquier tecla", True, BLANCO)
    pantalla.blit(texto2, (ANCHO_TABLERO // 2 - 140, ALTO_TABLERO // 2 + 20))

# -------------------------------------------------------------
# BUCLE PRINCIPAL DEL JUEGO
# -------------------------------------------------------------
def ejecutar_juego(velocidad_caida):
    grid = crear_grid()
    pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
    siguiente_pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
    score = 0
    pausa = False
    game_over = False
    clock = pygame.time.Clock()
    ultimo_descenso = pygame.time.get_ticks()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if game_over:
                    return
                if evento.key == pygame.K_p:
                    pausa = not pausa
                if not pausa and not game_over:
                    if evento.key == pygame.K_LEFT:
                        pieza.x -= 1
                        if colision(pieza, grid):
                            pieza.x += 1
                    elif evento.key == pygame.K_RIGHT:
                        pieza.x += 1
                        if colision(pieza, grid):
                            pieza.x -= 1
                    elif evento.key == pygame.K_DOWN:
                        pieza.y += 1
                        if colision(pieza, grid):
                            pieza.y -= 1
                    elif evento.key == pygame.K_SPACE:
                        while not colision(pieza, grid):
                            pieza.y += 1
                        pieza.y -= 1
                    elif evento.key == pygame.K_UP:
                        pieza.rotar(grid)

        if not pausa and not game_over:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - ultimo_descenso > velocidad_caida:
                pieza.y += 1
                if colision(pieza, grid):
                    pieza.y -= 1
                    fijar_pieza(pieza, grid)
                    grid, lineas = limpiar_lineas(grid)
                    if lineas > 0:
                        score = actualizar_puntuacion(lineas, score)
                    pieza = siguiente_pieza
                    siguiente_pieza = Pieza(COLUMNAS // 2 - 2, 0, random.choice(TETROMINOS))
                    if colision(pieza, grid):
                        game_over = True
                ultimo_descenso = tiempo_actual

        pantalla.fill(NEGRO)
        dibujar_grid(pantalla, grid)
        if not game_over:
            for i, fila in enumerate(pieza.forma):
                for j, valor in enumerate(fila):
                    if valor:
                        pygame.draw.rect(pantalla, pieza.color, ((pieza.x + j) * TAM_BLOQUE, (pieza.y + i) * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE))

        mostrar_puntaje_y_siguiente(pantalla, score, siguiente_pieza)
        if pausa:
            mostrar_pausa(pantalla)
        if game_over:
            mostrar_game_over(pantalla)

        pygame.display.flip()
        clock.tick(30)

# -------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------
while True:
    velocidad = menu_principal()
    if velocidad is None:
        break
    ejecutar_juego(velocidad)

pygame.quit()
