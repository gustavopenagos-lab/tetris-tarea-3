import pygame
import random

# ==========================================================
# CONSTANTES Y CONFIGURACIÓN INICIAL
# ==========================================================

# Ajustamos para que coincidan con el tablero del main (10x20)
TAM_BLOQUE = 30
COLUMNAS = 10
FILAS = 20

# Colores
NEGRO = (0, 0, 0)
GRIS = (34, 34, 34)
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
# FORMAS DE LOS TETROMINOS
# ==========================================================

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
# CLASE PIEZA
# ==========================================================

class Pieza:
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.color = random.choice(COLORES)

    def rotar(self, grid):
        rotada = [list(fila) for fila in zip(*self.forma[::-1])]
        forma_original = self.forma
        self.forma = rotada
        if colision(self, grid):
            self.forma = forma_original

# ==========================================================
# FUNCIONES DE LÓGICA DE JUEGO
# ==========================================================

def crear_grid():
    return [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

def colision(pieza, grid):
    """Detecta colisiones con bordes o piezas fijas"""
    for i, fila in enumerate(pieza.forma):
        for j, valor in enumerate(fila):
            if valor:
                x = pieza.x + j
                y = pieza.y + i
                # Evitar que se pase del área de juego (solo 10 columnas visibles)
                if x < 0 or x >= COLUMNAS or y >= FILAS:
                    return True
                if y >= 0 and grid[y][x] != 0:
                    return True
    return False

def fijar_pieza(pieza, grid):
    for i, fila in enumerate(pieza.forma):
        for j, valor in enumerate(fila):
            if valor and 0 <= pieza.y + i < FILAS and 0 <= pieza.x + j < COLUMNAS:
                grid[pieza.y + i][pieza.x + j] = pieza.color

def limpiar_lineas(grid):
    nuevas = []
    lineas_eliminadas = 0
    for fila in grid:
        if 0 not in fila:  # fila completa
            lineas_eliminadas += 1
        else:
            nuevas.append(fila)
    while len(nuevas) < FILAS:
        nuevas.insert(0, [0 for _ in range(COLUMNAS)])
    return nuevas, lineas_eliminadas

# ==========================================================
# PUNTUACIÓN
# ==========================================================

def actualizar_puntuacion(lineas_eliminadas, puntuacion_actual):
    puntos = {1: 100, 2: 300, 3: 500, 4: 800}
    return puntuacion_actual + puntos.get(lineas_eliminadas, 0)
