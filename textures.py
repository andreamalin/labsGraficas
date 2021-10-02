import struct

def color (b, g, r):
    # Recibe b->blue g->green r-> red 
    if 0 <= b <= 1 and 0 <= g <= 1 and 0 <= r <= 1:    
        # Enteros entre 0 al 255
        return bytes([int(b*255), int(g*255), int(r*255)])
    else:
        # Retorno negro
        return bytes([int(b), int(g), int(r)])

class Texture(object):
    def __init__(self, path):
        self.path = path
    
    def getColor(self, tx, ty):
        x = int(tx * self.width) - 1
        y = int(ty * self.height) - 1

        return self.pixels[y][x]

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
        image.close()
        return self.pixels