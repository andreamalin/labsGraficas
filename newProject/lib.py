import struct

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


def char(c):
    # char -> entero 1byte
    return struct.pack('=c', c.encode('ascii')) 

def word(w):
	# short -> entero 2bytes
    return struct.pack('=h', w) 

def dword(w):
	# long -> entero 4byte
    return struct.pack('=l', w) 


# bmp
def writebmp(filename, width, height, pixels):
    f = open(filename, 'bw')

    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + width * height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    f.write(dword(40))
    f.write(dword(width))
    f.write(dword(height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(width * height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    for x in range(height):
        for y in range(width):
            f.write(pixels[x][y])
    f.close()


class Material(object):
    def __init__(self, diffuse, albedo, spec, refractive_index=0):
        self.diffuse = diffuse # Nos dice de que color es la esfera
        self.albedo = albedo
        self.spec = spec
        self.refractive_index = refractive_index

class Intersect(object):
    def __init__(self, distance, point, normal):
        self.distance = distance
        self.point = point
        self.normal = normal

class Light(object):
    def __init__(self, position, intensity, color):
        self.position = position
        self.intensity = intensity
        self.color = color