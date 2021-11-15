from lib import *
from vectors import *

epsilon = 1e-6

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normal
        self.material = material
    
    def ray_intersect(self, origin, direction):
        # Obtengo el denominador (la verdad no entendi para que D:)
        denom = dot(self.normal, direction)
        if abs(denom) > epsilon:
            # Al igual que la esfera, obtengo
            # el producto punto para ver si el rayo intersecta
            t = dot(self.normal, sub(self.position, origin)) / denom

            if t > 0:
                # Obtengo donde intersecto el rato
                return Intersect(
                    distance = t,
                    point = sum(origin, mul(direction, t)),
                    normal = self.normal
                )
    
def getPlane(coordenate, size, normal, material, position):
    # Se realiza el plano dependiendo de la coordenada
    # Se obtiene el centro del plano para colocarlo donde se debe
    # La normal es dependiendo de la coordenada
    # El material lo da el usuario

    if (coordenate == "x"):
        return Plane(sum(position, V3(0, size.x/2, 0)), normal, material)
    elif (coordenate == "-x"):
        return Plane(sum(position, V3(0, -size.x/2, 0)), normal, material)
    elif (coordenate == "y"):
        return Plane(sum(position, V3(0, size.y/2, 0)), normal, material)
    elif (coordenate == "-y"):
        return Plane(sum(position, V3(0, -size.y/2, 0)), normal, material)
    elif (coordenate == "z"):
        return Plane(sum(position, V3(0, 0, size.z/2)), normal, material)
    elif (coordenate == "-z"):
        return Plane(sum(position, V3(0, 0, -size.z/2)), normal, material)
    return None


def calcFaces(coordenate, size, material, position):
    # Se obtiene el plano respectivo
    # El tamano del cubo lo da el usuario
    # Se utiliza el mismo tamano para todas las caras para realizar un cubo
    # El centro ayuda a posicionar los planos

    if (coordenate == "x"):
        return getPlane("x", size, V3(1, 0, 0), material, position)
    elif (coordenate == "-x"):
        return getPlane("-x", size, V3(1, 0, 0), material, position)
    elif (coordenate == "y"):
        return getPlane("y", size, V3(0, 1, 0), material, position)
    elif (coordenate == "-y"):
        return getPlane("-y", size, V3(0, -1, 0), material, position)
    elif (coordenate == "z"):
        return getPlane("z", size, V3(0, 0, 1), material, position)
    elif (coordenate == "-z"):
        return getPlane("-z", size, V3(0, 0, -1), material, position)


