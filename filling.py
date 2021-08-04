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
BLUE = color(0.9, 0.2, 0.1)
MAGENTA = color(0.9, 0.2, 0.1)
BACKGROUND = color(0.7, 0.9, 1)

# RENDERER
class Renderer(object):
    # Constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Seteamos el color y pintamos
        self.current_color = WHITE
        self.glClear()
        
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
        self.framebuffer[x][y] = color or self.current_color
        
    # Pintar una linea
    def glLine(self, x0, y0, x1, y1):
        global BLUE
        dy = y1 - y0
        dx = x1 - x0

        desc = (dy*dx) < 0

        dy = abs(dy)
        dx = abs(dx)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

            dy = abs(y1 - y0)
            dx = abs(x1 - x0)

        if desc and (y0 < y1):
            y0, y1 = y1, y0
        elif (not desc) and (y1 < y0):
            y0, y1 = y1, y0

        if (x1 < x0):
            x1, x0 = x0, x1

        offset = 0
        threshold = dx
        y = y0

        # y = mx + b
        points = []
        for x in range(x0, x1+1):
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))

            offset += (dy/dx) * 2 * dx
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx

        for point in points:
            self.glVertex(*point, BLACK)

    def floodfill(self, x, y, oldColor, newColor):
        puntos = [(x, y)]

        while len(puntos) > 0:
            x, y = puntos.pop()

            try:
                # Si llego a 0 termino el ciclo
                if x == 0:
                    return
                
                # Si y es menor de 0 o mayor a la altura, lo regreso a 0
                if y < 0 or y > self.height -  1:
                    y = 0

                # Reviso si el punto actual es distinto del fondo
                if self.framebuffer[x][y] != oldColor:
                    continue
            except:
                return

            # Punto el punto
            self.framebuffer[x][y] = newColor

            puntos.append((x + 1, y))  # derecha del punto actual
            puntos.append((x - 1, y))  # izquierda del punto actual
            puntos.append((x, y + 1))  # abajo del punto actual
            puntos.append((x, y - 1))  # arriba del punto actual

# Inicializo el framebuffer
def glCreateWindow(width, height):
    return Renderer(width, height)

# Inicializo el render
def glInit():
    return Renderer(1024, 768)

#r = glInit()
r = glCreateWindow(800, 800)
# r.glClear()
r.glClearColor(0.7, 0.9, 1)

# Pinto las lineas
p1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
p2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
p3 = [(377, 249), (411, 197), (436, 249)]
p4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)]
p5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

for i in range(len(p1)):
    x1 ,y1 = p1[i]
    x2, y2 = p1[(i + 1) % len(p1)]
    r.glLine(x1, y1, x2, y2)

for i in range(len(p2)):
    x1 ,y1 = p2[i]
    x2, y2 = p2[(i + 1) % len(p2)]
    r.glLine(x1, y1, x2, y2)

for i in range(len(p3)):
    x1 ,y1 = p3[i]
    x2, y2 = p3[(i + 1) % len(p3)]
    r.glLine(x1, y1, x2, y2)
    
for i in range(len(p4)):
    x1 ,y1 = p4[i]
    x2, y2 = p4[(i + 1) % len(p4)]
    r.glLine(x1, y1, x2, y2)

for i in range(len(p5)):
    x1 ,y1 = p5[i]
    x2, y2 = p5[(i + 1) % len(p5)]
    r.glLine(x1, y1, x2, y2)


# Sirve
for i in range(100):
    for j in range(100):
        r.floodfill(i-r.width, 800-r.height, BACKGROUND, BLACK)

# Asumo que tengo un punto dentro del centro
r.floodfill(710, 130, BACKGROUND, BLACK)

# Termino
r.glFinish()