# Tema: Problema de las N reinas / Bactracking
# Nombre:
# - Stiven Pilca           CI: 1750450262
# Carrera: Ingeniería en Sistemas de Información
# Paralelo: SI4 - 002
# Fecha de entrega: 15/08/2023

import numpy as np

class EstadoJuego():
    def __init__(self, dimension):
        self.tablero = np.chararray((dimension,dimension), itemsize=5, unicode= True)
        self.tablero.fill('--')
        self.movimientos = []

    def mover(self, move):
        self.tablero[move.fila_inicial][move.columna_inicial] = '--'
        self.tablero[move.fila_final][move.columna_final] = move.pieza_movida
        self.movimientos.append(move)
        

class Movimientos():

    def __init__ (self, casilla_inicial, casilla_final, tablero):
        self.fila_inicial = casilla_inicial[0]
        self.columna_inicial = casilla_inicial[1]
        self.fila_final = casilla_final[0]
        self.columna_final = casilla_final[1]

        self.pieza_movida = tablero[self.fila_inicial][self.columna_inicial]
        self.pieza_capturada = tablero[self.fila_final][self.columna_final]
