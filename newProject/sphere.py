from vectors import *
from lib import *

class Sphere(object):
    def __init__(self, center, radius, material):
        self.radius = radius
        self.center = center
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