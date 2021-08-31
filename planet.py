'''
PLANETA - GRAFICAS POR COMPUTADOR
Andrea Amaya 19357
'''
import struct
from vectors import *
from obj import Obj
import random
import math

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
    elif b < 256 and g < 256 and r < 256:
        # Retorno el color
        return bytes([int(b), int(g), int(r)])
    else:
        # Retorno verde
        return bytes([192, 169, 13])

# Colores
BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)
BLUE = color(0.9, 0, 0.2)
MAGENTA = color(0.9, 0.2, 0.1)
BACKGROUND = color(0.7, 0.9, 1)
AQUA = color(191, 196, 111)

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
        
        self.zbuffer = [
            [-99999 for x in range(self.width)]
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
        self.write('planet.bmp')
        
    # Pintar un pixel -> recibe la posicion y color
    def glVertex(self, x, y, color = None):
        try:
            self.framebuffer[x][y] = color or self.current_color
        except:
            return
        
    # Pintar
    def load(self, filename, translate, scale):
        model = Obj(filename)
        self.light = norm(V3(0, 0, 4))
        mitadX = round(self.width/2)
        mitadY = round(self.height/2)

        for face in model.faces:
            vcount = len(face)
            if vcount == 3 or vcount == 4:
                # Posiciones
                f1 = face[0][0]
                f2 = face[1][0]
                f3 = face[2][0]

                # Cara
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]
                v3 = model.vertices[f3 - 1]

                # Puntos
                x1, y1, z1 = self.calcPoint(v1, scale, translate)
                x2, y2, z2 = self.calcPoint(v2, scale, translate)
                x3, y3, z3 = self.calcPoint(v3, scale, translate)

                # Triangulo
                self.triangle(
                    self.calcViewPort(x1, y1, z1, mitadX, mitadY),
                    self.calcViewPort(x2, y2, z2, mitadX, mitadY), 
                    self.calcViewPort(x3, y3, z3, mitadX, mitadY)
                )
            
            # Cuadrado
            if vcount == 4:
                 # Posicion faltante
                f4 = face[3][0]

                # Cara faltante
                v4 = model.vertices[f4 - 1]

                # Punto faltante
                x4, y4, z4 = self.calcPoint(v4, scale, translate)

                # Triangulo faltante
                self.triangle(
                    self.calcViewPort(x1, y1, z1, mitadX, mitadY),
                    self.calcViewPort(x3, y3, z3, mitadX, mitadY), 
                    self.calcViewPort(x4, y4, z4, mitadX, mitadY)
                )               
        
    
    # Convierto en punto normal la coordenada para que quede dentro de la ventana
    def calcViewPort(self, x, y, z, mitadX, mitadY): 
        resX = round(mitadX + (x * mitadX))
        resY = round(mitadY + (y * mitadY))

        if (self.width <= resX):
            resX = self.width - 1
        elif (resX < 0):
            resX = 0
        if (self.height <= resY):
            resY = self.height - 1
        elif (resY < 0):
            resY = 0

        return V3(resX, resY, z)

    # Obtengo el punto
    def calcPoint(self, point, scale, translate):
        x = (point[0] * scale[0]) + translate[0]
        y = (point[1] * scale[1]) + translate[1]
        z = (point[2] * scale[2]) + translate[2]
    
        return [x, y, z]

    # Triangulo
    def triangle(self, A, B, C):
        xmin, xmax, ymin, ymax = bbox(A, B, C)
        contador = 0


        # Circulos
        def circle(x, y, r, out):
            if (out):
                return ((300-x)**2 + (300-y)**2) > r
            else:
                return ((300-x)**2 + (300-y)**2) < r

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                    P = V3(x, y, 0)
                    w, v, u = barycentric(A, B, C, P)

                    if (w < 0 or v < 0 or u < 0):
                        continue

                    normal = norm(cross(sub(B, A), sub(C, A)))
                    intensity = dot(normal, self.light)
                    grey = round(150 * intensity)
                    z = A.z * w + B.z * v + C.z * u
                
                    if (grey < 0):
                        continue
                    elif (grey > 255):
                        # Centro
                        paint = color(162, 153, 20)
                        grey = 205
                    else:
                        if (circle(x, y, 40000, True)):
                            # Orilla
                            rand = random.randint(0, 5);
                            # Adentro de la orilla
                            paint = color(int(grey*1.6), int(grey*1.1), 0)
                            self.glVertex(y+rand, x+rand, paint)
                            self.glVertex(y-rand, x-rand, paint)
                        else:           
                            # Adentro de la orilla orilla 
                            paint = color(int(grey*1.4), int(grey*1.02), 0)

                    if (random.randint(3, 9) == 4):
                        # Fondo verde
                        paint = color(int(grey*0.9), int(grey*0.9), grey*0.4)



    
                    if abs(z) > self.zbuffer[x][y]:
                        self.glVertex(y, x, paint)
                        self.zbuffer[x][y] = z
                        
                        if (random.randint(3, 9) == 4 and circle(x, y, 25000, False)):
                            rand = random.randint(0, 50);
                            # Fondo verde oscuro
                            paint = color(129, 126, 51)
                            self.glVertex(y+rand, x+rand, paint)
                            self.glVertex(y, int(x-rand/2), paint)
                            self.glVertex(y-rand, x-rand, paint)

                        if (random.randint(3, 9) == 4 and circle(x, y, 20000, False)):
                            rand = random.randint(0, 50);
                            # Fondo verde claro
                            paint = color(int(grey*0.4), int(grey), grey*0.1)
                            self.glVertex(y+rand, x+rand, paint)
                            self.glVertex(y, int(x-rand/2), paint)
                            paint = color(208, 205, 90)
                            self.glVertex(y-rand, x-rand, paint)
                        
                        if (circle(x, y, 47000, True)):
                            # Pinto brillo de afuera
                            paint = color(224, 173, 0)
                            self.glVertex(y-1, x+1, paint)
                            self.glVertex(y+1, x-1, paint)
                            self.glVertex(y+1, x+1, paint)
                            self.glVertex(y-1, x-1, paint)

                        # Fondo cafe
                        if (circle(x, y, 5000, False)):
                            if (random.randint(3, 9) <= 5):
                                paint = color(grey*0.6, grey*0.7, grey*0.5)
                                self.glVertex(y-80, x+50, paint)
                            
    # Pintar una linea
    def glLine(self, x0, y0, x1, y1, translate):
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
        for x in range(int(x0), int(x1+1)):
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))

            try:
                div = dy/dx
            except:
                div = 0
            offset += div * 2 * dx

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx

        for point in points:
            for i in range(3):
                x = point[1] + translate + i
                y = point[0] + i
                self.romboPoint(x, y)

    def romboPoint(self, i, j):
        try:
            # Si no es el fondo ni la orrilla
            if self.framebuffer[i][j] != BLACK:
                b, g, r = self.framebuffer[i][j]
                if not (b == 224 and g == 173 and r == 0):
                    if b < 150:
                        # Orilla
                        actualShade = color(204, 132, 1)
                    # elif b < 200:
                    #     # Centro
                    #     actualShade = color(255, 207, 122)
                    else:
                        # Centro
                        actualShade = color(255, 255, 255)
                    self.glVertex(i, j, actualShade)
        except:
            return
    # Rombos
    def rombo(self, y, size):
        height = size
        width = height*2

        contador = 0
        for j in range(y, self.height):
            actualIteration = contador*width
            a = actualIteration + width/2
            b = height # Altura 1
            c = actualIteration+width
            d = -height # Altura 2

            self.glLine(a, d, c, 0, j)
            self.glLine(c, 0, a, b, j)
            self.glLine(a, b, actualIteration, 0, j)
            self.glLine(actualIteration, 0, a, d, j)

            contador += 1




# Inicializo el framebuffer
def glCreateWindow(width, height):
    return Renderer(width, height)

#r = glInit()
r = glCreateWindow(600, 600)

# Cargo la esfera
r.load('./models/sphere.obj', [0, -0.03, 0], [1.5, 1.5, 500])

# Rombos
r.rombo(80, 12)
r.rombo(80, 12)
r.rombo(110, 15)
r.rombo(150, 20)
r.rombo(200, 22)
r.rombo(250, 27)
r.rombo(300, 30)
r.rombo(350, 27)
r.rombo(400, 22)
r.rombo(440, 20)
r.rombo(470, 15)
r.rombo(500, 12)

# Termino
r.glFinish()