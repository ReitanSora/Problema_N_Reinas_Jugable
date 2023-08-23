# Tema: Problema de las N reinas / Bactracking
# Nombre:
# - Stiven Pilca           CI: 1750450262
# Carrera: Ingeniería en Sistemas de Información
# Paralelo: SI4 - 002
# Fecha de entrega: 15/08/2023

class BusquedaBinariaR:
    
    def busqueda_recursiva(self, lista, bajo, alto, dato):
        if bajo > alto:
            return -1
        centro = (bajo+alto)//2
        if lista[centro] == dato:
            return centro
        elif lista[centro] < dato:
            return self.busqueda_recursiva(lista, centro + 1, alto, dato)
        else:
            return self.busqueda_recursiva(lista, bajo, centro - 1, dato)
