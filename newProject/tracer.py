from lib import *
from transformations import *
from vectors import *
from math import tan
import random
from sphere import *
from cube import *

MAX_RECURSION_DEPTH = 3
pi = 3.14
# Colores
BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)
MAGENTA = color(0.9, 0.2, 0.5)
AQUA = color(161, 91, 0)

class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.aspectRatio = self.width/self.height # Para que las imagenes no tengan que ser cuadradas
        self.background_color = MAGENTA
        self.light = None
        self.glClear()

    # Limpia la imagen a color negro -> llena el framebuffer
    def glClear(self, color = None): 
        self.framebuffer = [
            [color or MAGENTA for x in range(self.width)]
            for y in range(self.height)
        ]
    
    def write(self, filename):
        writebmp(filename, self.width, self.height, self.framebuffer)

    # Pintar un pixel -> recibe la posicion y color
    def glVertex(self, x, y, color = None):
        self.framebuffer[x][y] = color or self.background_color

    # Donde se intersecta con la esfera
    def cast_ray(self, origin, direction, recursion=0):
        material, intersect = self.scene_intersect(origin, direction)

        if ((material is None or intersect is None) or recursion >= MAX_RECURSION_DEPTH):
            return self.background_color


        # Direccion de la luz
        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))

        # Movemos la sombra por 0.1
        offset_normal = mul(intersect.normal, 0.1) # shadow bias
        # Si es menor que 0, resto para mandarlo atras, sino sumo
        shadow_orig = sum(intersect.point, offset_normal) if dot(light_dir, intersect.normal) >= 0 else sub(intersect.point, offset_normal)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)

        # Si no choca en nada, no llego hasta la sombra
        if shadow_material is None or length(sub(shadow_intersect.point, shadow_orig)) > light_distance:
            shadow_intensity = 0
        else:
            # De lo contrario, hay sombra
            shadow_intensity = 0.9

        # Reflex -> Luz que rebota
        if material.albedo[2] > 0:
            # Obtengo la direccion de la reflexion
            reverse_direction = mul(direction, -1)
            reflect_direction = reflect(reverse_direction, intersect.normal)
            
            reflect_origin = sum(intersect.point, offset_normal) if dot(reflect_direction, intersect.normal) >= 0 else sub(intersect.point, offset_normal)
            reflect_color = self.cast_ray(reflect_origin, reflect_direction, recursion + 1)
        else:
            reflect_color  = color(0, 0, 0)

        # Refractive -> Luz que atraviesa
        if material.albedo[3] > 0:
            refract_direction = refract(direction, intersect.normal, material.refractive_index)
            
            if refract_direction is None:
                refract_color  = color(0, 0, 0)
            else:
                refract_origin = sum(intersect.point, offset_normal) if dot(refract_direction, intersect.normal) >= 0 else sub(intersect.point, offset_normal)
                refract_color = self.cast_ray(refract_origin, refract_direction, recursion + 1)
        else:
            refract_color  = color(0, 0, 0)




        # Color -> Regreso 0 cuando el valor es menor que 0
        diffuse_intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

        # Si estoy en la sombra
        if shadow_intensity > 0:
            specular_intensity = 0
        else:
            # Reflexion
            specular_reflection = reflect(light_dir, intersect.normal)
            # Si es mayor que 0, regreso 0  -> Intensidad
            specular_intensity = self.light.intensity * (max(0, dot(specular_reflection, direction)) ** material.spec)


        # Calcular el color difuso
        listOfColor = list(material.diffuse)
        diffuse = [
            listOfColor[0] * diffuse_intensity * material.albedo[0],
            listOfColor[1] * diffuse_intensity * material.albedo[0],
            listOfColor[2] * diffuse_intensity * material.albedo[0]]

        # Calcular el color especular
        listOfColor = list(self.light.color)
        specular = [
            listOfColor[0] * specular_intensity * material.albedo[1],
            listOfColor[1] * specular_intensity * material.albedo[1],
            listOfColor[2] * specular_intensity * material.albedo[1]]


        # Calcular el color de la reflexion
        listOfColor = list(reflect_color)
        reflection = [
            listOfColor[0] * material.albedo[2],
            listOfColor[1] * material.albedo[2],
            listOfColor[2] * material.albedo[2]]

        # Calcular el color de la refraccion
        listOfColor = list(refract_color)
        refraction = [
            listOfColor[0] * material.albedo[2],
            listOfColor[1] * material.albedo[2],
            listOfColor[2] * material.albedo[2]]

        # Calculo del color resultante
        result = color(
            diffuse[0] + specular[0] + reflection[0] + refraction[0],
            diffuse[1] + specular[1] + reflection[1] + refraction[1],
            diffuse[2] + specular[2] + reflection[2] + refraction[2]
        )
        return result

    # Revisar si golpeo el objeto
    def scene_intersect(self, origin, direction):
        zbuffer = float('inf')
        material = None
        intersect = None

        for obj in self.scene:
            r_intersect = obj.ray_intersect(origin, direction)

            if r_intersect and r_intersect.distance < zbuffer:
                zbuffer = r_intersect.distance
                material = obj.material
                intersect = r_intersect

        return material, intersect


    
    def render(self):
        fov = pi/2
        angulo = tan(fov/2)

        for y in range(self.height):
            for x in range(self.width):
                # if random.randint(0, 1) > 0.7:
                    i = (2 * ((x + 0.5) / self.width) - 1) * self.aspectRatio * angulo
                    j = 1 - 2 * ((y + 0.5) / self.height) * angulo
                    direction = norm(V3(i, j, -1))
                    color = self.cast_ray(V3(0, 0, 0), direction)
                    self.glVertex(x, y, color)


r = Raytracer(1000, 1000)
r.light = Light(position=V3(10, 10, 20), intensity=1, color=color(255, 255, 255))

ivory = Material(diffuse=color(100, 100, 80), albedo=[0.6, 0.3, 0.1, 0], spec=50)
rubber = Material(diffuse=color(80, 0, 0), albedo=[0.9, 0.1, 0, 0], spec=10)
mirror = Material(diffuse=color(255, 255, 255), albedo=[0, 10, 0.8, 0], spec=1500)
glass = Material(diffuse=color(255, 255, 255), albedo=[0, 0.5, 0.1, 0.5], spec=150, refractive_index=1.5)

r.scene = [
#   Sphere(V3(0, -1.5, -10), 1.5, ivory),
#   Sphere(V3(-2, 1, -12), 2, glass),
#   Sphere(V3(1, 1, -8), 1, rubber),
#   Sphere(V3(0, 5, -20), 5, mirror),
  # Plane(V3(0, 2, -5), V3(0, 2, -7), V3(0, 0, 0), ivory),
    Cube(position=V3(-2, 5, -15), size=V3(2, 3, 7), material=ivory)
]

r.render()
r.write('pruebaRaytracer.bmp')
    