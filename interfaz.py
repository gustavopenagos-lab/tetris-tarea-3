
import pygame
from pygame._sdl2.video import Window, Renderer
from tetris import ANCHO, ALTO, BLANCO, GRIS, TAM_BLOQUE, COLUMNAS, FILAS

def crear_pantalla():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tetris")
    return pantalla

def crear_panel():
    panel_window = Window("Panel de Información", size=(300, 600))
    panel_renderer = Renderer(panel_window)
    return panel_window, panel_renderer

def dibujar_grid(pantalla, grid):
    for y in range(FILAS):
        for x in range(COLUMNAS):
            color = grid[y][x]
            if color != 0:
                pygame.draw.rect(
                    pantalla, color,
                    (x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
                )
            pygame.draw.rect(pantalla, GRIS, (x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE), 1)

def mostrar_puntaje_panel(renderer, score):
    surface = pygame.Surface((300, 600))
    surface.fill((30, 30, 30))
    fuente = pygame.font.SysFont("Arial", 30, bold=True)
    texto = fuente.render(f"Puntaje: {score}", True, BLANCO)
    surface.blit(texto, (50, 50))
    return surface

def mostrar_siguiente_pieza_panel(surface, siguiente_pieza):
    fuente = pygame.font.SysFont("Arial", 25)
    texto = fuente.render("Siguiente:", True, BLANCO)
    surface.blit(texto, (90, 150))
    x_offset, y_offset = 100, 200
    for i, fila in enumerate(siguiente_pieza.forma):
        for j, valor in enumerate(fila):
            if valor:
                pygame.draw.rect(surface, siguiente_pieza.color,
                                 (x_offset + j * TAM_BLOQUE,
                                  y_offset + i * TAM_BLOQUE,
                                  TAM_BLOQUE, TAM_BLOQUE))

def mostrar_pausa(pantalla):
    fuente = pygame.font.SysFont("Arial", 40)
    texto = fuente.render("PAUSA", True, BLANCO)
    pantalla.blit(texto, (ANCHO // 2 - 60, ALTO // 2 - 20))
    pygame.display.flip()

def mostrar_game_over(pantalla):
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    pantalla.blit(overlay, (0, 0))
    fuente = pygame.font.SysFont("Arial", 40, bold=True)
    texto = fuente.render("GAME OVER", True, BLANCO)
    pantalla.blit(texto, (ANCHO // 2 - 100, ALTO // 2 - 20))
