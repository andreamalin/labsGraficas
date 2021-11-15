import struct
from math import pi, acos, atan2
from vectors import *

import numpy

def color (b, g, r):
    try:
        # Recibe b->blue g->green r-> red 
        if 0 <= b <= 1 and 0 <= g <= 1 and 0 <= r <= 1:    
            # Enteros entre 0 al 255
            return bytes([int(b*255), int(g*255), int(r*255)])
        else:
            # Retorno negro
            return bytes([int(b), int(g), int(r)])
    except:
        return bytes([0, 0, 0])

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.colors = []
    
    def getColor(self, direction):
      direction = norm(direction)

      x = int((atan2(direction.z, direction.x) / (2 * pi) + 0.5) * self.width)
      y = int(acos(-direction.y) / pi * self.height)
      index = (y * self.width + x) * 3 % len(self.pixels)

      realColor = color(0, 0, 0)
      try:
          realColor = color(self.colors[index], self.colors[index + 1], self.colors[index + 2])
      except:
          realColor = color(0, 0, 0)

      return realColor

    def read(self):
        image = open(self.path, 'rb')

        # Puntero -> saltamos el header
        image.seek(10)
        header = struct.unpack("=l", image.read(4))[0]

        # Ancho y largo
        image.seek(18)
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        self.pixels = []
        image.seek(header)

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                # Obtengo los colores b, r, g
                b = ord(image.read(1))
                r = ord(image.read(1))
                g = ord(image.read(1))
                self.pixels[y].append(color(b, r, g))
        
        
        for row in self.pixels:
            for cell in row:
                self.colors.append(cell)

        image.close()
        return self.pixels