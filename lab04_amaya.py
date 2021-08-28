'''
LAB 01 - GRAFICAS POR COMPUTADOR
Andrea Amaya 19357
'''
import struct
from vectors import *
from textures import *
from obj import Obj

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
        return bytes([int(b), int(g), int(r)])

# Colores
BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)
BLUE = color(0.9, 0, 0.1)
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
            x = point[1]
            y = point[0]
            self.glVertex(x, y, BLUE)

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


    # Triangulos
    def transform(self, vertex, translate=(0,0,0), scale=(1,1,1)):
        return V3 (
            round((vertex[0] + translate[0]) * scale[0]),
            round((vertex[1] + translate[1]) * scale[1]),
            round((vertex[2] + translate[2]) * scale[2]),
        )
        

    # Pintar
    def load(self, filename, translate, scale):
        model = Obj(filename)
        self.light = norm(V3(0, 2, -1))
        
        for face in model.faces:
            vcount = len(face)

            if vcount == 4:
                # Posiciones
                f1 = face[0][0]
                f2 = face[1][0]
                f3 = face[2][0]
                f4 = face[3][0]

                # Cara
                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]
                v3 = model.vertices[f3 - 1]
                v4 = model.vertices[f4 - 1]

                x1 = int((v1[0] + translate[0]) * scale[0])
                y1 = int((v1[1] + translate[1]) * scale[1])
                z1 = ((v1[2] + translate[2]) * scale[2])
                x2 = int((v2[0] + translate[0]) * scale[0])
                y2 = int((v2[1] + translate[1]) * scale[1])
                z2 = ((v2[2] + translate[2]) * scale[2])
                x3 = int((v3[0] + translate[0]) * scale[0])
                y3 = int((v3[1] + translate[1]) * scale[1])
                z3 = ((v3[2] + translate[2]) * scale[2])
                x4 = int((v4[0] + translate[0]) * scale[0])
                y4 = int((v4[1] + translate[1]) * scale[1])
                z4 = ((v4[2] + translate[2]) * scale[2])

                self.triangle(V3(x1, y1, z1), V3(x2, y2, z2), V3(x3, y3, z3))
                self.triangle(V3(x1, y1, z1), V3(x3, y3, z3), V3(x4, y4, z4))

    # Texturas
    def texture(self, filename):
        model = Obj(filename)
        contador = 0
        for face in model.faces:
            if (contador < 100):
                vcount = len(face)

                # Posiciones
                f1 = face[0][0]
                f2 = face[1][0]
                f3 = face[2][0]
                f4 = face[3][0]

                # Triangulo
                tA = V2(model.tvertices[f1][0]*200, model.tvertices[f1][1]*200)
                tB = V2(model.tvertices[f2][0]*200, model.tvertices[f2][1]*200)
                tC = V2(model.tvertices[f3][0]*200, model.tvertices[f3][1]*200)
                tD = V2(model.tvertices[f4][0]*200, model.tvertices[f4][1]*200)

                r.glLine(int(tA[0]), int(tA[1]), int(tB[0]), int(tB[1]))
                r.glLine(int(tB[0]), int(tB[1]), int(tC[0]), int(tC[1]))
                r.glLine(int(tC[0]), int(tC[1]), int(tA[0]), int(tA[1]))

                r.glLine(int(tA[0]), int(tA[1]), int(tC[0]), int(tC[1]))
                r.glLine(int(tC[0]), int(tC[1]), int(tD[0]), int(tD[1]))
                r.glLine(int(tD[0]), int(tD[1]), int(tA[0]), int(tA[1]))

                contador +=1 


                
    def triangle(self, A, B, C):
        xmin, xmax, ymin, ymax = bbox(A, B, C)

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                    P = V3(x, y, 0)
                    w, v, u = barycentric(A, B, C, P)

                    if (w < 0 or v < 0 or u < 0):
                        continue
    
                    normal = norm(cross(sub(B, A), sub(C, A)))
                    intensity = dot(normal, self.light)
                    grey = round(200 * intensity)
                    z = A.z * w + B.z * v + C.z * u

                    if (grey < 0):
                        paint = color(39, 15, 20)
                    else:
                        paint = color(grey, int(grey*0.5), grey*0)
                    
    
                    if abs(z) > self.zbuffer[y][x]:
                        self.glVertex(y, x, paint)
                        self.zbuffer[y][x] = z


# Inicializo el framebuffer
def glCreateWindow(width, height):
    return Renderer(width, height)

# Inicializo el render
def glInit():
    return Renderer(1024, 768)

#r = glInit()
r = glCreateWindow(600, 600)
# r.glClear()
# r.glClearColor(0.7, 0.9, 1)


# r.load('./models/untitled.obj', [2.7, 0.5, 0], [110, 110, 50000])
r.texture('./models/untitled.obj')

# Pruebo mi textura -> Sirve :D
'''
t = Texture('./models/water.bmp')
r = glCreateWindow(256, 256)

for x in range(256):
    for y in range(256):
        r.glVertex(x, y, t.pixels[x][y])

r.write('copy.bmp')
'''


# Termino
r.glFinish()