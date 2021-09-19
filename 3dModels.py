'''
3D MODELS - GRAFICAS POR COMPUTADOR
Andrea Amaya 19357
'''
import struct
from math import sin, cos
from vectors import *
from textures import *
from transformations import *
from obj import Obj



pi = 3.14

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
BLUE = color(0.9, 0, 0.2)
MAGENTA = color(0.9, 0.2, 0.1)
BACKGROUND = color(0.7, 0.9, 1)
AQUA = color(161, 91, 0)

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
            [color or AQUA for x in range(self.width)]
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
        self.write('face.bmp')
        
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

    # Pintar
    def load(self, filename, translate, scale, rotation):
        self.loadModelMatrix(translate, scale, rotation)
    
        model = Obj(filename)
        self.light = norm(V3(0, 0, 1))
        mitadX = round(self.width/2)
        mitadY = round(self.height/2)

        self.Matrix = mulMatrix(self.Viewport, mulMatrix(self.Projection, mulMatrix(self.View, self.Model)))

        for face in model.faces:
            vcount = len(face)
            if vcount == 3 or vcount == 4:
                # Posiciones
                f1 = face[0][0]
                f2 = face[1][0]
                f3 = face[2][0]

                # Cara
                v1 = V3(*model.vertices[f1 - 1])
                v2 = V3(*model.vertices[f2 - 1])
                v3 = V3(*model.vertices[f3 - 1])

                self.triangle(self.transform(v1), self.transform(v2), self.transform(v3))
            
            # Cuadrado
            if vcount == 4:
                 # Posicion faltante
                f4 = face[3][0]

                # Cara faltante
                v4 =  V3(*model.vertices[f4 - 1])
                self.triangle(self.transform(v1), self.transform(v3), self.transform(v4))            
    
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
                        continue
                    elif (grey > 255):
                        paint = color(255, 255, 255)
                    else:
                        paint = color(grey, int(grey*0.5), grey*0)
                        # paint = color(grey, int(grey*0.3), grey*0)

                    try:
                        if z > self.zbuffer[x][y]:
                            self.glVertex(y, x, paint)
                            self.zbuffer[x][y] = z
                    except:
                        pass

    # Transform
    def transform(self, vertex):
        vertexA = [[vertex.x], [vertex.y], [vertex.z], [1]]
        transformedVerted = mulMatrix(self.Matrix, vertexA)

        transformed3D = [
            transformedVerted[0][0]/transformedVerted[3][0],
            transformedVerted[1][0]/transformedVerted[3][0],
            transformedVerted[2][0]/transformedVerted[3][0]
        ]

        return V3(*transformed3D)

    # Load model matrix
    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        rotationM = rotationMatrix(rotate)
        translationM = translateMatrix(translate)
        scaleM = scaleMatrix(scale)

        self.Model = mulMatrix(translationM, mulMatrix(rotationM, scaleM))
    # Load view matrix Mi - O
    def loadViewMatrix(self, x, y, z, center):
        Mi = [
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1]]

        O = [[1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0, 1]]

        self.View = mulMatrix(Mi, O)
    
    # View port matrix
    def loadViewPortMatrix(self, x=0, y=0):
        self.Viewport = [
            [self.width/2, 0, 0, x + self.width/2],
            [0, self.height/2, 0, y + self.height/2],
            [0, 0, 128, 128],
            [0, 0, 0, 1]]

    # Camara
    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1/len(sub(eye, center)))
        self.loadViewPortMatrix()

    # Projection matrix -> Valores coeff < 1
    def loadProjectionMatrix(self, coeff):
        self.Projection = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, coeff, 1]]



# Inicializo el framebuffer
def glCreateWindow(width, height):
    return Renderer(width, height)

# Inicializo el render
def glInit():
    return Renderer(1024, 768)

#r = glInit()
r = glCreateWindow(600, 600)
# Camara
r.lookAt(V3(3, 0, 5), V3(0, 0, 0), V3(0, 1, 0))
# Modelo
r.load('./models/model.obj', [0, 0, 0], [1/2, 1/2, 1], [0, 0, 0])
# r.load('./models/sphere.obj', [0, 0, 0], [1, 1, 500])

# Termino
r.glFinish()