'''
LAB 01 - GRAFICAS POR COMPUTADOR
Andrea Amaya 19357
'''

import struct 

def char(c):
    # char -> entero 1byte
    return struct.pack('=c', c.encode('ascii')) 

def word(w):
	# short -> entero 2bytes
    return struct.pack('=h', w) 

def dword(w):
	# long -> entero 4byte
    return struct.pack('=l', w) 

def color (b, g, r):
    # Recibe b->blue g->green r-> red 
    if 0 <= b <= 1 and 0 <= g <= 1 and 0 <= r <= 1:    
        # Enteros entre 0 al 255
        return bytes([int(b*255), int(g*255), int(r*255)])
    else:
        # Retorno negro
        return bytes([0, 0, 0])

# Colores
BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)
MAGENTA = color(0.9, 0.2, 0.1)

# RENDERER
class Renderer(object):
    # Constructor
    def __init__(self, width, height, widthVP = None, heightVP = None, xVP = None, yVP = None):
        self.width = width
        self.height = height
        # Si no se especifica un viewport, se pinta en toda la imagen
        self.widthVP = widthVP or width
        self.heightVP = heightVP or height
        self.xVP = xVP or 0
        self.yVP = yVP or 0
        # Seteamos el color y pintamos
        self.current_color = WHITE
        self.glClear()
    
    # Especificando la posicion y tamano del viewPort
    def glViewPort(self, x, y, width, height):
        self.xVP = x
        self.yVP = y
        self.widthVP = width
        self.heightVP = height
        
    # Limpia la imagen a color negro -> llena el framebuffer
    def glClear(self, color = None): 
        self.framebuffer = [
            [color or BLACK for x in range(self.width)]
            for y in range(self.height)
        ]
    
    # Limpia la imagen con un color especificado -> recibe entre 0 a 1
    def glClearColor(self, r, g, b):
        self.glClear(color(r, g, b))
        
    # Escribe el archivo
    def write (self, filname):
        f = open(filname, 'bw') # Definimos el archivo en bytes
        # file header
        f.write(char('B'))
        f.write(char('M'))
        # El archivo pesa 14 bytes del header + 40 de info + 3 bytes de color g, r, b
        f.write(dword(14 + 40 + 3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14 + 40)) # Donde termina el header
        
        # Info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        # Se recorre todo el framebuffer
        for y in range(self.height):
            for x in range (self.width):
                f.write(self.framebuffer[y][x])
        
        f.close()
        
    # Crea el archivo
    def glFinish(self):
        self.write('a.bmp')
        
    # Pintar un pixel -> recibe la posicion y color
    def glVertex(self, x, y, color = None):
        centroX = int(self.widthVP/2)
        centroY = int(self.heightVP/2)
        # multplicamos x, y por el centro para tomar el pixel correcto
        posX = int(x*centroX)
        posY = int(y*centroY)
        
        # Pintamos solo dentro del viewport
        if(posX <= self.widthVP and posY <= self.heightVP):
            # self.xVP+x; self.yVP+y -> permiten comenzar a pintar solo dentro del viewPort
            # centroX, centroY -> permiten comenzar a pintar a partir del centor del viewPort
            posActualX = self.xVP+posX+centroX
            posActualY = self.yVP+posY+centroY

            # Debido a que es un array, restamos 1 a la posicion
            if (posActualX > 0):
                posActualX -= 1
            if (posActualY > 0):
                posActualY -= 1

            self.framebuffer[posActualX][posActualY] = color or self.current_color
        
    # Pintar una linea
    def glLine(self, x0, y0, x1, y1):
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

            dy = abs(y1 - y0)
            dx = abs(x1 - x0)

        offset = 0
        threshold = 0.5 * 2 * dx
        y = y0

        points = []

        incio = x0
        final = x1
       
        while incio < final:
            if steep:
                points.append((y, incio))
            else:
                points.append((incio, y))

            offset += (dy/dx) * 2 * dx

            if offset >= threshold:
                y += 0.01 if y0 < y1 else -1
                threshold += 1 * 2 * dx
            
            incio += 0.01

        for point in points:
            self.glVertex(*point, color(0.9, 0.2, 0.1))

# Inicializo el framebuffer
def glCreateWindow(width, height):
    return Renderer(width, height)

# Inicializo el render
def glInit():
    return Renderer(1024, 768)

#r = glInit()
r = glCreateWindow(500, 500)
# r.glClear()
r.glClearColor(0.7, 0.9, 1)
# Declaro mi viewport
r.glViewPort(400, 400, 100, 100)
# Pinto una linea
r.glLine(-1, -1, 1, 1)

'''
# Pinto un cuadrado dentro del viewport
posActualX = 0
posActualY = 0
for x in range(10):
    posActualY = 0
    for y in range(10):
        r.glVertex(posActualX, posActualY, MAGENTA)
        posActualY += 0.01
    
    posActualX += 0.01
    
# Pinto un pixel en cada esquina del viewport
r.glVertex(-1, -1, MAGENTA)
r.glVertex(1, 1, MAGENTA)
r.glVertex(-1, 1, MAGENTA)
r.glVertex(1, -1, MAGENTA)
'''
# Creo la imagen
r.glFinish()