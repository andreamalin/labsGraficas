import pygame
import random

def color (b, g, r):
    # Recibe b->blue g->green r-> red 
    if 0 <= b <= 1 and 0 <= g <= 1 and 0 <= r <= 1:    
        # Enteros entre 0 al 255
        return bytes([int(b*255), int(g*255), int(r*255)])
    elif b > 255 or g > 255 or r > 255:
        # Retorno negro
        return bytes([255, 255, 255])
    else:
        # Retorno el color
        return bytes([int(b), int(g), int(r)])

WHITE = color(255, 255, 255)
BLACK = color(0, 0, 0)

class Life(object):
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect() # Obteniendo el tamano de la pantalla
        self.screen = screen
        self.actualCells = []

    def pixel(self, x, y, color=[255,255,255]):
        self.screen.set_at((x, y), (color)) # Parametros, color

    def copy(self):
        # Para poder obtener el color antes de poner el pixel
        self.prev_screen = self.screen.copy() # Se copia

    def beacon(self, x, y):
        # Beacon
        self.pixel(x, y)
        self.pixel(x+1, y)
        self.pixel(x, y+1)
        self.pixel(x+1, y+1)
        self.pixel(x+2, y+2)
        self.pixel(x+3, y+2)
        self.pixel(x+2, y+3)
        self.pixel(x+3, y+3)

    def glider(self, x, y):
        # Glider
        self.pixel(x+2, y)
        self.pixel(x, y+1)
        self.pixel(x+2, y+1)
        self.pixel(x+1, y+2)
        self.pixel(x+2, y+2)


    def sun(self, x, y):
        # Sun
        self.pixel(x+2, y)
        self.pixel(x+3, y)
        self.pixel(x+4, y)
        self.pixel(x+8, y)
        self.pixel(x+9, y)
        self.pixel(x+10, y)

        self.pixel(x, y+2)
        self.pixel(x+5, y+2)
        self.pixel(x+7, y+2)
        self.pixel(x+12, y+2)

        self.pixel(x, y+3)
        self.pixel(x+5, y+3)
        self.pixel(x+7, y+3)
        self.pixel(x+12, y+3)

        self.pixel(x, y+4)
        self.pixel(x+5, y+4)
        self.pixel(x+7, y+4)
        self.pixel(x+12, y+4)
        
        self.pixel(x+2, y+5)
        self.pixel(x+3, y+5)
        self.pixel(x+4, y+5)
        self.pixel(x+8, y+5)
        self.pixel(x+9, y+5)
        self.pixel(x+10, y+5)

        self.pixel(x+2, y+7)
        self.pixel(x+3, y+7)
        self.pixel(x+4, y+7)
        self.pixel(x+8, y+7)
        self.pixel(x+9, y+7)
        self.pixel(x+10, y+7)

        self.pixel(x, y+8)
        self.pixel(x+5, y+8)
        self.pixel(x+7, y+8)
        self.pixel(x+12, y+8)

        self.pixel(x, y+9)
        self.pixel(x+5, y+9)
        self.pixel(x+7, y+9)
        self.pixel(x+12, y+9)

        self.pixel(x, y+10)
        self.pixel(x+5, y+10)
        self.pixel(x+7, y+10)
        self.pixel(x+12, y+10)

        self.pixel(x+2, y+11)
        self.pixel(x+3, y+11)
        self.pixel(x+4, y+11)
        self.pixel(x+8, y+11)
        self.pixel(x+9, y+11)
        self.pixel(x+10, y+11)


    def cross(self, x, y):
        self.pixel(x+1, y)
        self.pixel(x+1, y+1)

        self.pixel(x, y+2)
        self.pixel(x+2, y+2)

        self.pixel(x+1, y+3)
        self.pixel(x+1, y+4)
        self.pixel(x+1, y+5)
        self.pixel(x+1, y+6)

        self.pixel(x, y+7)
        self.pixel(x+2, y+7)

        self.pixel(x+1, y+8)
        self.pixel(x+1, y+9)


    def glider2(self, x, y):
        self.pixel(x+1, y)
        self.pixel(x+2, y)

        self.pixel(x, y+1)
        self.pixel(x+1, y+1)
        self.pixel(x+2, y+1)
        self.pixel(x+3, y+1)
        
        self.pixel(x, y+2)
        self.pixel(x+1, y+2)
        self.pixel(x+3, y+2)
        self.pixel(x+4, y+2)

        self.pixel(x+2, y+3)
        self.pixel(x+3, y+3)


    def random(self, x, y):
        self.pixel(x+1, y)

        self.pixel(x+1, y+1)
        self.pixel(x+3, y+1)

        self.pixel(x, y+2)
        self.pixel(x+2, y+2)

        self.pixel(x+1, y+3)
        self.pixel(x+3, y+3)
        self.pixel(x+4, y+3)

        self.pixel(x+3, y+4)

    def completePattern(self, x, y):
        # Left side
        self.pixel(x, y)
        self.pixel(x+1, y)
        self.pixel(x+1, y+1)
        self.pixel(x+1, y+2)
        self.pixel(x+3, y+2)
        self.pixel(x+2, y+3)
        self.pixel(x+3, y+3)

        self.pixel(x+2, y+13)
        self.pixel(x+3, y+13)
        self.pixel(x+1, y+14)
        self.pixel(x+3, y+14)
        self.pixel(x+1, y+15)
        self.pixel(x, y+16)
        self.pixel(x+1, y+16)

        self.pixel(x+15, y+3)
        self.pixel(x+14, y+4)
        self.pixel(x+13, y+5)
        self.pixel(x+19, y+5)
        self.pixel(x+20, y+5)

        self.pixel(x+14, y+6)
        self.pixel(x+16, y+6)
        self.pixel(x+19, y+6)
        self.pixel(x+20, y+6)

        self.pixel(x+15, y+7)
        self.pixel(x+15, y+9)
        self.pixel(x+14, y+10)
        self.pixel(x+16, y+10)
        self.pixel(x+19, y+10)
        self.pixel(x+20, y+10)

        self.pixel(x+13, y+11)
        self.pixel(x+19, y+11)
        self.pixel(x+20, y+11)

        self.pixel(x+14, y+12)
        self.pixel(x+15, y+13)

        # Right side
        self.pixel(x+31, y+5)
        self.pixel(x+32, y+5)
        self.pixel(x+31, y+6)
        self.pixel(x+32, y+6)
        self.pixel(x+31, y+10)
        self.pixel(x+32, y+10)
        self.pixel(x+31, y+11)
        self.pixel(x+32, y+11)

        
        self.pixel(x+37, y+4)
        self.pixel(x+36, y+5)
        self.pixel(x+37, y+5)
        self.pixel(x+38, y+5)
        self.pixel(x+36, y+6)
        self.pixel(x+37, y+6)
        self.pixel(x+36, y+7)
        self.pixel(x+36, y+9)
        self.pixel(x+36, y+10)
        self.pixel(x+37, y+10)
        self.pixel(x+36, y+11)
        self.pixel(x+37, y+11)
        self.pixel(x+38, y+11)
        self.pixel(x+37, y+12)

        
        self.pixel(x+50, y)
        self.pixel(x+51, y)
        self.pixel(x+50, y+1)
        self.pixel(x+48, y+2)
        self.pixel(x+50, y+2)
        self.pixel(x+48, y+3)
        self.pixel(x+49, y+3)
        self.pixel(x+48, y+13)
        self.pixel(x+49, y+13)
        self.pixel(x+48, y+14)
        self.pixel(x+50, y+14)
        self.pixel(x+50, y+15)
        self.pixel(x+50, y+16)
        self.pixel(x+51, y+16)

    def render(self):
        ## Complete pattern
        self.completePattern(110, 20)

        # # Beacon
        self.beacon(120, 20)
        # # # # Beacon
        self.beacon(140, 20)
        # # Beacon
        self.beacon(120, 10)
        # # # # Beacon
        self.beacon(140, 10)

        # # Glider 2
        self.glider2(150, 10)
        # # Glider 2
        self.glider2(155, 20)
        # # Glider 2
        self.glider2(160, 30)

        
        # # Cross
        self.cross(175, 45)
        ## Complete pattern
        self.completePattern(150, 50)
        
        # # Random
        self.random(100, 50)
        # # # Glider
        self.glider(100, 40)
        
        # # Sun
        self.sun(30, 40)
        # # Cross
        self.cross(35, 55)
        ## Complete pattern
        self.completePattern(10, 10)

    def checkNeighbours(self, x, y):
        # Por cada punto, quiero hacer modulo con el ancho en x y con el alto en y
        # Obtengo las 4 diagonales
        d1 = {'x': x-1, 'y': y-1, 'color': self.prev_screen.get_at((x-1, y-1))}
        d2 = {'x': x-1, 'y': y+1, 'color': self.prev_screen.get_at((x-1, y+1))}
        d3 = {'x': x+1, 'y': y-1, 'color': self.prev_screen.get_at((x+1, y-1))}
        d4 = {'x': x+1, 'y': y+1, 'color': self.prev_screen.get_at((x+1, y+1))}
        # Obtengo las 4 rectas
        l1 = {'x': x+1, 'y': y, 'color': self.prev_screen.get_at((x+1, y))}
        l2 = {'x': x-1, 'y': y, 'color': self.prev_screen.get_at((x-1, y))}
        l3 = {'x': x, 'y': y-1, 'color': self.prev_screen.get_at((x, y-1))}
        l4 = {'x': x, 'y': y+1, 'color': self.prev_screen.get_at((x, y+1))}
        # Celula actual
        act = {'x': x, 'y': y, 'color': self.prev_screen.get_at((x, y))}
        # Obtengo las celulas
        cells = [d1, d2, d3, d4, l1, l2, l3, l4, act]
        self.checkCells(cells)
        

    def checkCells(self, cells):
        # Se separa el punto actual para no analizarlo como vecino
        actualPoint = cells[8]
        cells = cells[0:8]
        aliveCells = []

        # Se chequea cuantas celulas alrededor de la actual estan vivas
        for cell in cells:
            if cell['color'] == (255, 255, 255, 255):
                aliveCells.append(cell)
        
        # Si solo hay 1 celula viva o mas que 3
        if (len(aliveCells) <= 1 or len(aliveCells) > 3):
            # Se muere la celula actual
            if (actualPoint['color'] != (0, 0, 0, 255) or actualPoint['color'] != (0, 0, 0)):
                actualPoint['color'] = BLACK
                self.actualCells.append(actualPoint)
        elif (len(aliveCells) == 3):
            # Se crea una nueva en el punto actual
            actualPoint['color'] = WHITE
            self.actualCells.append(actualPoint)

    def paintNewCells(self):
        # Se pintan todos los resultados obtenidos
        for cell in self.actualCells:
            self.screen.set_at((cell['x'], cell['y']), cell['color'])
        self.actualCells = []



pygame.init() # Siempre va
screen = pygame.display.set_mode((225, 80)) # Tamano de la pantalla


r = Life(screen=screen)


r.render() # Se llama al render en cada vuelta
contador = 0
while contador < 200:
    pygame.time.delay(1) # Tiempo entre renders

    r.copy() # Obteniendo el framebuffer anterior

    for x in range(2, r.width - 5):
        for y in range(2, r.height - 5):
            r.checkNeighbours(x, y)
    r.paintNewCells()

    pygame.display.flip() # Vamos cambiando de buffer
    contador+=1
