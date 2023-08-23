# Tema: Problema de las N reinas / Bactracking
# Nombre:
# - Stiven Pilca           CI: 1750450262
# Carrera: Ingeniería en Sistemas de Información
# Paralelo: SI4 - 002
# Fecha de entrega: 15/08/2023

class ProblemaNReinas:
    valor = str()
    soluciones = list()

    def es_valido(self, fila: int, columna: int, reinas: list):
        for row in range(fila):
            if columna == reinas[row]:
                return False
            elif abs(columna - reinas[row]) == abs(fila - row):
                return False
        return True

    def place_queens(self, fila: int, reinas: list, n: int):
        if fila == n:
            self.valor = self.valor + str(reinas)+','
            self.soluciones.append(str(reinas))
            return 1
        else:
            soluciones_totales = 0
            for column in range(n):
                if self.es_valido(fila, column, reinas):
                    reinas[fila] = column
                    soluciones_totales += self.place_queens(fila+1, reinas, n)
            return soluciones_totales

    def n_reinas(self, n):
        reinas = [' ']*n
        row = 0
        return self.place_queens(row, reinas, n)
    
    def array_format(self, array: list, dimension: int) -> list:
        longitud_elemento = array[0]
        longitud_elemento = len(longitud_elemento)
        numero_elementos = longitud_elemento//3
        nuevo_arreglo = []
        inicio = 1
        fin = 2
        for elemento in array:
            for i in range(numero_elementos):
                nuevo_arreglo.append(elemento[inicio:fin])
                inicio += 3
                fin += 3
            inicio = 1
            fin = 2

        matriz = []
        contador = 0
        for i in range(len(array)):
            matriz.append([])
            for j in range(dimension):
                if i > 0:
                    matriz[i].append(int(nuevo_arreglo[contador])+1)
                else:
                    matriz[i].append(int(nuevo_arreglo[j])+1)

                contador += 1
        return matriz
        