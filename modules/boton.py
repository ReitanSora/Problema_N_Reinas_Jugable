# Tema: Problema de las N reinas / Bactracking
# Nombre:
# - Stiven Pilca           CI: 1750450262
# Carrera: Ingeniería en Sistemas de Información
# Paralelo: SI4 - 002
# Fecha de entrega: 15/08/2023

import pygame.font
from static import style

class Boton:
    def __init__(self, a_game, texto):
        self.ventana = a_game.pantalla
        self.ventana_rect = self.ventana.get_rect()
        self.width, self.height = 200, 50
        self.color_fondo = style.COLOR_MAGENTA_CLARO
        self.texto_color = style.COLOR_BLANCO

        self.font = pygame.font.SysFont('Verdana', 30, 'bold')

        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.ventana_rect.center

        self.preparacion_texto(texto)
    
    def preparacion_texto(self, texto):
        self.texto_image = self.font.render(texto, True, self.texto_color, self.color_fondo)
        self.texto_image_rect = self.texto_image.get_rect()
        self.texto_image_rect.center = self.rect.center

    
    def render_boton(self):
        self.ventana.fill(self.color_fondo, self.rect)
        self.ventana.blit(self.texto_image, self.texto_image_rect)
        