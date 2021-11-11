from vectors import *
from lib import *

class Cube(object):
    def __init__(self, xMin, xMax, yMin, yMax, zMin, zMax, material):
        self.xMin = 0 # Punto inicial x
        self.xMax = 0 # Punto final x
        self.yMin = 0 # Punto inicial y
        self.yMax = 0 # Punto final y
        self.zMin = 0 # Punto inicial z
        self.zMax = 0 # Punto final z
        self.material = material
        

    def ray_intersect(self, origin, direction):
        L = sub(self.center, origin)
        tca = dot(L, direction)
        l = length(L)

        d2 = l**2 - tca** 2
        # Si el rayo impacta afuera de la esfecta
        if d2 > self.radius**2:
            return None

        thc = (self.radius**2 -d2)**(1/2)

        # Donde pega el rayo
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            # Intercepto menor en t0
            t0 = t1
        if t0 < 0:
            # La esfera esta detras de la camara
            return None


        # Donde pega en x, y
        hit = sum(origin, mul(direction, t0))
        # 
        normal = norm(sub(hit, self.center))

        return Intersect(distance=t0, normal=normal, point=hit)