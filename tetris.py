import pygame
import random

# ==========================================================
# CONSTANTES Y CONFIGURACIÓN INICIAL =======================
# ==========================================================

ANCHO = 300
ALTO = 600
TAM_BLOQUE = 30
COLUMNAS = ANCHO // TAM_BLOQUE
FILAS = ALTO // TAM_BLOQUE

# Colores
NEGRO = (0, 0, 0)
GRIS = (34,34,34)
BLANCO = (255, 255, 255)
COLORES = [
    (0, 255, 255),  # cyan
    (255, 165, 0),  # naranja
    (0, 255, 0),    # verde
    (255, 0, 0),    # rojo
    (0, 0, 255),    # azul
    (255, 255, 0),  # amarillo
    (128, 0, 128)   # morado
]

# ==========================================================
# FORMAS DE LOS TETROMINOS =================================
# ==========================================================

# Formas
TETROMINOS = [
    [[1, 1, 1, 1]],                # I 
    [[1, 1], [1, 1]],              # O 
    [[0, 1, 0], [1, 1, 1]],        # T 
    [[1, 0, 0], [1, 1, 1]],        # L 
    [[0, 0, 1], [1, 1, 1]],        # J
    [[1, 1, 0], [0, 1, 1]],        # S 
    [[0, 1, 1], [1, 1, 0]]         # Z 
]

# ==========================================================
# CLASES ===================================================
# ==========================================================

class Pieza:
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.color = random.choice(COLORES)

    # ROTACION DE LAS PIEZAS -------------------------------
    def rotar(self, grid):
        # Rotación en sentido horario
        rotada = list(zip(*self.forma[::-1]))
        rotada = [list(fila) for fila in rotada]

        forma_original = self.forma
        self.forma = rotada

        # Si colisiona tras rotar, se cancela
        if colision(self, grid):
            self.forma = forma_original

# ==========================================================
# FUNCIONES DE LÓGICA DE JUEGO =============================
# ==========================================================

# --- Crear el grid (tablero vacío) ---

# --- Funciones ---
def crear_grid():
    return [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

# --- Detectar colisión (borde o bloque existente) ---
def colision(pieza, grid):
    for i, fila in enumerate(pieza.forma):
        for j, valor in enumerate(fila):
            if valor:
                x = pieza.x + j
                y = pieza.y + i
                if x < 0 or x >= COLUMNAS or y >= FILAS:
                    return True     # Fuera del tablero
                if y >= 0 and grid[y][x] != 0:
                    return True     # Choca con bloque fijo
    return False

# ==========================================================
# TOCAR FONDO
# ==========================================================

# --- Fijar pieza al tablero cuando toca fondo o choca ---
def fijar_pieza(pieza, grid):
    for i, fila in enumerate(pieza.forma):
        for j, valor in enumerate(fila):
            if valor:
                grid[pieza.y + i][pieza.x + j] = pieza.color

# --- Limpiar linea completa ---
def limpiar_lineas(grid):
    nuevas = [fila for fila in grid if any(c == 0 for c in fila)]
    lineas_eliminadas = FILAS - len(nuevas)
    while len(nuevas) < FILAS:
        nuevas.insert(0, [0 for _ in range(COLUMNAS)])
    return nuevas, lineas_eliminadas

# --- Mostrar puntaje ---
def mostrar_puntaje(pantalla, score):
    fuente = pygame.font.SysFont("Arial", 25)
    texto = fuente.render(f"Puntaje: {score}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

# --- Dibujar tablero y bloques fijos ---
def dibujar_grid(pantalla, grid):
    for y in range(FILAS):
        for x in range(COLUMNAS):
            if grid[y][x] != 0:
                pygame.draw.rect(
                    pantalla,
                    grid[y][x],
                    (x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE)
                )

            # Dibuja líneas blancas como guía    
            pygame.draw.rect(
                pantalla,
                GRIS,
                (x * TAM_BLOQUE, y * TAM_BLOQUE, TAM_BLOQUE, TAM_BLOQUE),
                1
            )
