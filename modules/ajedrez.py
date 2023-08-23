# Tema: Problema de las N reinas / Bactracking
# Nombre:
# - Stiven Pilca           CI: 1750450262
# Carrera: Ingeniería en Sistemas de Información
# Paralelo: SI4 - 002
# Fecha de entrega: 15/08/2023

import pygame
from tkinter import messagebox
from fpdf import FPDF
import sys
from functions.motor import EstadoJuego
from functions.motor import Movimientos
from functions.busqueda import BusquedaBinariaR
from functions.n_reinas import ProblemaNReinas
from functions.pdf import PDF
from modules.boton import Boton
from static import style


class Ajedrez:

    def __init__(self):
        pygame.init()
        self.ancho = self.alto = 720
        self.pantalla = pygame.display.set_mode((1280, 720))
        self.pantalla_width = self.pantalla.get_rect().width
        self.pantalla_height = self.pantalla.get_rect().height
        pygame.display.set_caption("Problema de las N reinas")
        self.casilla = int()
        self.max_fps = 15
        self.imagenes = {}

        self.clock = pygame.time.Clock()
        self.pantalla.fill(pygame.Color(style.BG))

        self.juego_activado = False
        self.resuelto = False
        self.play_boton = Boton(self, 'Jugar')

        self.jugar()

    def cargar_imagenes(self):
        piezas = ['reina', ]
        for pieza in piezas:
            self.imagenes[pieza] = pygame.transform.scale(pygame.image.load(
                "static/"+pieza+".png"), (self.casilla, self.casilla))

    def jugar(self):
        self.cargar_imagenes()
        self.ejecutando = True
        self.casilla_seleccionada = ()
        self.clicks_jugador = []

        self.user_text = ''
        self.base_font = pygame.font.SysFont('Verdana', 20, 'bold')
        self.title_font = pygame.font.SysFont('Corbel', 30, 'bold')
        self.subtitle_font = pygame.font.SysFont('Corbel', 25)
        self.text_box = pygame.Rect(490, 200, 300, 40)

        self.active = False
        self.color = pygame.Color(style.COLOR_MAGENTA_NORMAL)

        segundos = 0
        minutos = 0
        horas = 0

        crono_font = pygame.font.SysFont('comicsansms', 60)
        self.text_crono = crono_font.render('{}:{}:{}'.format(
            horas, minutos, segundos), True, style.COLOR_BLANCO)

        while self.ejecutando:
            self.pantalla.fill(style.BG)
            if self.juego_activado is True:
                
                pygame.time.get_ticks()
                segundos += 1.69
                self.pantalla.blit(self.text_crono, (810, 100))
                if segundos >= 100:
                    segundos = 0
                    minutos += 1
                if minutos == 60:
                    minutos = 0
                    horas += 1

                if self.dimension <= 4:
                    if horas == 1:
                        self.ejecutando = False
                elif self.dimension <= 8:
                    if horas == 3:
                        self.ejecutando = False
                elif self.dimension > 8:
                    if horas == 5:
                        self.ejecutando = False
            else:
                segundos = 0
                minutos = 0
                horas = 0

            self.text_crono = crono_font.render('Tiempo:\n\n{}: {}: {:.1f}'.format(
                horas, minutos, segundos), True, style.COLOR_BLANCO)

            for event in pygame.event.get():
                if event.type == pygame.QUIT and self.juego_activado:
                    self.ejecutando = False
                elif event.type == pygame.QUIT and not self.juego_activado: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.text_box.collidepoint(event.pos):
                        self.active = True
                        self.user_text = ''
                    else:
                        self.active = False

                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            self.user_text += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN and self.juego_activado:
                    location = pygame.mouse.get_pos()  # (x,y)

                    column = location[0]//self.casilla
                    row = location[1]//self.casilla

                    if self.casilla_seleccionada == (row, column):
                        self.casilla_seleccionada = ()
                        self.clicks_jugador = []
                    else:
                        try:
                            self.estado_juego.tablero[row][column] = 'reina'
                            self.cargar_imagenes()
                            self.casilla_seleccionada = (row, column)
                            self.clicks_jugador.append(
                                self.casilla_seleccionada)
                        except IndexError:
                            messagebox.showerror(
                                title='Error de selección', message='Presione en una casilla del tablero')

                    if len(self.clicks_jugador) == 2:
                        movimiento = Movimientos(
                            self.clicks_jugador[0], self.clicks_jugador[1], self.estado_juego.tablero)
                        self.estado_juego.mover(movimiento)
                        self.casilla_seleccionada = ()
                        self.clicks_jugador = []

                elif event.type == pygame.MOUSEBUTTONUP:
                    location = pygame.mouse.get_pos()  # (x,y)
                    self.comprobar_boton(location)

            if self.juego_activado:
                self.dibujar_estado_juego(self.pantalla, self.estado_juego, self.clicks_jugador,self.casilla_seleccionada)
                instrucciones_font = pygame.font.SysFont('comicsansms', 22)
                instrucciones = instrucciones_font.render('Instrucciones:',True, style.COLOR_BLANCO)
                instrucciones1 = instrucciones_font.render('• Doble click para colocar una pieza.',True, style.COLOR_BLANCO)
                instrucciones2 = instrucciones_font.render('• Un click para seleccionar una pieza y moverla.',True, style.COLOR_BLANCO)
                instrucciones3 = instrucciones_font.render('• Cierre el juego para comprobar su solución.',True, style.COLOR_BLANCO)
                self.pantalla.blit(instrucciones, (730, 460))
                self.pantalla.blit(instrucciones1, (750, 500))
                self.pantalla.blit(instrucciones2, (750, 540))
                self.pantalla.blit(instrucciones3, (750, 580))

            if not self.juego_activado:
                self.widgets()

            pygame.display.flip()
            self.clock.tick(60)

        if not self.ejecutando:
            posicion_sol, continuar = self.recolectar_solucion()
            if not self.resuelto:
                if continuar:
                    self.creacion_pdf()
                else:
                    respuesta = messagebox.askyesno(
                        message='Vaya! Se ha agotado el tiempo!\nDeseas ver algunas de las soluciones posibles?', title='Game Over')
                    if respuesta:
                        self.creacion_pdf()
            elif self.resuelto and posicion_sol == -1:
                if continuar:
                    self.creacion_pdf()
                else:
                    respuesta = messagebox.askyesno(
                        message='Tu solución no es correcta 💔\nDeseas ver algunas de las soluciones posibles?', title='Game Over')
                    if respuesta:
                        self.creacion_pdf()
            elif self.resuelto and posicion_sol != -1:
                if continuar:
                    self.creacion_pdf()
                else:
                    respuesta = messagebox.askyesno(
                        message='Felicidades!\nHaz encontrado una de las soluciones posibles✨✨\nDeseas ver todas las demás?', title='Game Over')
                    if respuesta:
                        self.creacion_pdf()

    def widgets(self):
        # renderizado del entry
        self.pantalla.fill(style.BG)
        if self.active:
            self.color = pygame.Color(style.COLOR_MAGENTA_CLARO)
        else:
            self.color = pygame.Color(style.COLOR_MAGENTA_NORMAL)

        pygame.draw.rect(self.pantalla, self.color, self.text_box, 4)
        self.text_surface = self.base_font.render(
            self.user_text, True, style.COLOR_BLANCO)
        self.pantalla.blit(
            self.text_surface, (self.text_box.x + 10, self.text_box.y + 10))
        self.text_box.w = max(300, self.text_surface.get_width()+10)

        self.text_surface2 = self.title_font.render(
            'Problema de las N Reinas - Backtracking', True, style.COLOR_BLANCO)
        self.text_surface3 = self.subtitle_font.render(
            'Ingrese la dimensión del tablero', True, style.COLOR_BLANCO)
        self.text_surface4 = self.subtitle_font.render(
            'Recuperación - Algoritmos', True, style.COLOR_BLANCO)
        self.text_surface5 = self.subtitle_font.render(
            'Stiven Pilca - SI4-001', True, style.COLOR_BLANCO)
        self.text_surface6 = self.subtitle_font.render(
            'Universidad Central del Ecuador - 2023-2023', True, style.COLOR_BLANCO)
        self.text_surface7 = self.subtitle_font.render(
            'Se recomienda leer el manual', True, style.COLOR_BLANCO)
        self.pantalla.blit(self.text_surface2,
                           (self.pantalla.get_rect().center[0]-225, 75))
        self.pantalla.blit(self.text_surface3,
                           (self.pantalla.get_rect().center[0]-160, 170))
        self.pantalla.blit(self.text_surface4, (20, 550))
        self.pantalla.blit(self.text_surface5, (20, 600))
        self.pantalla.blit(self.text_surface6, (20, 650))
        self.pantalla.blit(self.text_surface7, (900, 650))

        # renderizado del boton
        self.play_boton.render_boton()


    def highlight(self, pantalla, movimiento, casilla_seleccionada):
        if casilla_seleccionada != ():
            r, c = casilla_seleccionada
            s = pygame.Surface((self.casilla, self.casilla))
            s.set_alpha(100)
            s.fill(pygame.Color('blue'))
            pantalla.blit(s, (c*self.casilla, r*self.casilla))

            s.fill(pygame.Color('yellow'))
            if movimiento[0][0] == r and movimiento[0][1] == c and len(movimiento)>1:
                self.pantalla.blit(s, (self.casilla*movimiento[1][1], self.casilla*movimiento[1][0]))

    def dibujar_estado_juego(self, pantalla, estado_tablero, movimiento, casilla_selec):
        self.dibujar_tablero(pantalla)
        self.highlight(pantalla, movimiento, casilla_selec)
        self.dibujar_piezas(pantalla, estado_tablero.tablero)

    def dibujar_tablero(self, pantalla):
        colores = [pygame.Color(style.COLOR_BLANCO),
                   pygame.Color(style.COLOR_COMPLEMENTO)]
        for row in range(self.dimension):
            for column in range(self.dimension):
                color = colores[((row+column) % 2)]
                pygame.draw.rect(pantalla, color, pygame.Rect(
                    column*self.casilla, row*self.casilla, self.casilla, self.casilla))

    def dibujar_piezas(self, pantalla, estado_tablero):
        for row in range(self.dimension):
            for column in range(self.dimension):
                piezas = estado_tablero[row][column]
                if piezas != '--':
                    pantalla.blit(self.imagenes[piezas], pygame.Rect(
                        column*self.casilla, row*self.casilla, self.casilla, self.casilla))

    def comprobar_boton(self, mouse_position):
        self.boton_press = self.play_boton.rect.collidepoint(mouse_position)
        if self.boton_press and not self.juego_activado:
            try: 
                self.dimension = int(self.user_text)
                self.casilla = self.alto//self.dimension
                self.estado_juego = EstadoJuego(self.dimension)
                self.pantalla.fill(style.BG)

                self.juego_activado = True
            except ValueError:
                self.user_text = 'Ingrese un número entero'

    def recolectar_solucion(self):
        lista = self.estado_juego.tablero

        soluciones_previas = []
        for i in range(len(lista)):
            for j in range(len(lista)):
                if lista[i][j] == 'reina':
                    soluciones_previas.append(j)

        if len(soluciones_previas) == 0:
            self.resuelto = False
        else:
            self.resuelto = True

        solucion = str(soluciones_previas)
        if self.dimension > 8:
            respuesta = messagebox.askyesno(
                    message='A continuación, el programa calculará todas las soluciones posibles para comprobar la suya y generará un pdf con dichas soluciones\n\nEs posible que el programa tarde o que no responda si colocó una dimensión mayor a 8\n\nDesea continuar?',
                      title='Comprobar solución')
            if respuesta:
                posicion_sol = self.comprobar_solucion(solucion)
                return posicion_sol, True
            else:
                exit(0)
        else:
            posicion_sol = self.comprobar_solucion(solucion)
            return posicion_sol, False

    def comprobar_solucion(self, solucion_usuario):
        busqueda = BusquedaBinariaR()
        app = ProblemaNReinas()
        app.n_reinas(self.dimension)
        self.lista_soluciones = app.soluciones
        posicion_sol = busqueda.busqueda_recursiva(
            self.lista_soluciones, 0, len(self.lista_soluciones) - 1, solucion_usuario)
        self.lista_soluciones = app.array_format(self.lista_soluciones, self.dimension)

        return posicion_sol

    def creacion_pdf(self):
        pdf = PDF(orientation='P', unit='mm', format='A4')
        pdf.alias_nb_pages()
        pdf.add_page()

        pdf.set_font('Arial', '', 14)

        pdf.multi_cell(w=0, h=10, txt='Filas', border=1, align='C', fill=0)
        pdf.cell(w=15, h=10, txt=' ', border=1, align='C', fill=0)

        for i in range(self.dimension-1):
            pdf.cell(w=(175/self.dimension), h=10, txt='Fila {}'.format(i+1), border=1, align='C', fill=0)
        pdf.multi_cell(w=(175/self.dimension), h=10, txt='Fila {}'.format(self.dimension), border=1, align='C', fill=0)
        
        for i in range(len(self.lista_soluciones)):
            pdf.cell(w=15, h=10, txt='Col', border=1, align='C', fill=0)
            for j in range(self.dimension-1):
                pdf.cell(w=(175/self.dimension), h=10, txt=str(self.lista_soluciones[i][j]), border=1, align='C', fill=0)
            pdf.multi_cell(w=(175/self.dimension), h=10, txt=str(self.lista_soluciones[i][j+1]), border=1, align='C', fill=0)
        
        pdf.output('Problema N reinas - Soluciones posibles.pdf')
