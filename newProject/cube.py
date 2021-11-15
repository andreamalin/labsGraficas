from vectors import *
from lib import *
from plane import *

epsilon = 1e-6
class Cube(object):
    def __init__(self, position, size, material):
        # El centro del cubo y el material
        self.position = position
        self.material = material

        # Obtengo el minbox y maxbox
        self.minbox = sub(position, (sum((mul(size, 1/2)), V3(epsilon, epsilon, epsilon))))
        self.maxbox = sum(position, (sum((mul(size, 1/2)), V3(epsilon, epsilon, epsilon))))

        # Mi cubo esta conformado por 6 caras, una en cada coordenada
        self.box = [
            calcFaces("x", size, material, position),
            calcFaces("-x", size, material, position),
            calcFaces("y", size, material, position),
            calcFaces("-y", size, material, position),
            calcFaces("z", size, material, position),
            calcFaces("-z", size, material, position)
        ]

    def getBoxLimits(hit):
        if hit.point.x < self.minbox.x or self.maxbox.x < hit.point.x and hit.point.y < self.minbox.y or self.maxbox.y < hit.point.y and hit.point.z < self.minbox.z or self.maxbox.z < hit.point.z:
            return True

    # Obtengo si intersecta el rato
    def ray_intersect(self, orig, dir):
        intersect = 0
        d = 999

        for plane in self.box:
            hit = plane.ray_intersect(orig, dir)
            if hit:
                # Reviso que el rayo este dentro de mis limites
                if hit.point.x < self.minbox.x or self.maxbox.x < hit.point.x: continue
                if hit.point.y < self.minbox.y or self.maxbox.y < hit.point.y: continue
                if hit.point.z < self.minbox.z or self.maxbox.z < hit.point.z: continue
                
                # Obtengo el ultimo resultado
                if hit.distance < d:
                    d = hit.distance
                    intersect = Intersect(
                        distance = d,
                        point = hit.point,
                        normal = hit.normal
                    )
        return intersect