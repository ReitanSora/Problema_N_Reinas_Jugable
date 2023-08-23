# Tema: Problema de las N reinas / Bactracking
# Nombre:
# - Stiven Pilca           CI: 1750450262
# Carrera: Ingeniería en Sistemas de Información
# Paralelo: SI4 - 002
# Fecha de entrega: 15/08/2023

from fpdf import FPDF


class PDF(FPDF):

    def header(self):

        self.image('static/uce.png', x=10, y=10, w=30, h=30)

        self.set_font('Arial', 'B', 18)

        self.cell(w=0, h=30, txt='Soluciones para un tablero N x N', border=0, ln=1,
                  align='C', fill=0)

        self.ln(10)

    def footer(self):

        self.set_y(-15)

        self.set_font('Arial', 'BI', 12)

        self.cell(w=0, h=10, txt='Problema de las N reinas - pag ' + str(self.page_no()) + '/{nb}', border=0, ln=1,
                  align='C', fill=0)
