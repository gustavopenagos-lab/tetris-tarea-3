# ==========================================================
# interfaz.py — Módulo de Interfaz Gráfica
# ==========================================================

import pygame
from tetris import ANCHO, ALTO, BLANCO, NEGRO, GRIS, TAM_BLOQUE, COLUMNAS, FILAS

# --- Crear pantalla principal ---
def crear_pantalla():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Tetris")
    return pantalla

# --- Dibujar tablero (cuadrícula + bloques) ---
def dibujar_grid(pantalla, grid):
    for y in range(FILAS):
        for x in range(COLUMNAS):
            color = grid[y][x]
            if color != 0:
                pygame.draw.rect(
                    pantalla,
                    color,
                    (x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
                )
            # Líneas guía suaves
            pygame.draw.rect(
                pantalla,
                GRIS,
                (x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE),
                1
            )

# --- Mostrar puntaje ---
def mostrar_puntaje(pantalla, score):
    fuente = pygame.font.SysFont("Arial", 25)
    texto = fuente.render(f"Puntaje: {score}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

# --- Mostrar mensaje de pausa ---
def mostrar_pausa(pantalla):
    fuente = pygame.font.SysFont("Arial", 40)
    texto = fuente.render("PAUSA", True, BLANCO)
    pantalla.blit(texto, (ANCHO // 2 - 60, ALTO // 2 - 20))
    pygame.display.flip()

# --- Mostrar Game Over (encima de todo) ---
def mostrar_game_over(pantalla):
    # Fondo semitransparente
    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.set_alpha(150) # nivel de transparencia (0–255)
    overlay.fill((0, 0, 0))  # negro
    pantalla.blit(overlay, (0, 0))
    # Texto de Game Over encima
    fuente = pygame.font.SysFont("Arial", 40, bold=True)
    texto = fuente.render("GAME OVER", True, BLANCO)
    pantalla.blit(texto, (ANCHO // 2 - 100, ALTO // 2 - 20))
