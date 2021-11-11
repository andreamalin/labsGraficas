from lib import *
from sphere import *
from math import pi, acos, atan2

class Plane(object):
    def __init__(self, minbound, maxbound, material):
        self.min = minbound
        self.max = maxbound
        self.material = material

    def ray_intersect(self, origin, direction):
        dxo = -(origin.x + self.min.x) / direction.x
        dxf = -(origin.x + self.max.x) / direction.x
        dyo = -(origin.y + self.min.y) / direction.y
        dyf = -(origin.y + self.max.y) / direction.y
        dzo = -(origin.z + self.min.z) / direction.z
        dzf = -(origin.z + self.max.z) / direction.z

        tmin = origin.x + (direction.x * dxo)
        tmax = origin.x + (direction.x * dxf)
        if tmin > tmax:
            tmin, tmax, dxo, dxf = tmax, tmin, dxf, dxo
        d = dxo

        tymin = origin.y + (direction.y * dyo)
        tymax = origin.y + (direction.y * dyf)
        if tymin > tymax: tymin, tymax, dyo, dyf = tymax, tymin, dyf, dyo

        if (tmin > tmax) or (tymin > tmax): return None
        if (tymin > tmin): 
            tmin = tymin
            d = dyo
        if (tymax < tmax): tmax = tymax

        tzmin = origin.z + (direction.z * dzo)
        tzmax = origin.z + (direction.z * dzf)
        if tzmin > tzmax: tzmin, tzmax, dzo, dzf = tzmax, tzmin, dzf, dzo

        # if (tmin > tzmax) or (tzmin > tmax): return None
        if (tzmin > tmin): 
            tmin = tzmin
            d = dzo
        if (tzmax < tmax): tmax = tzmax

        normal = V3(0, 1, 0)

        print(sum(origin, mul(direction, d)))
        return Intersect(
            distance=d,
            point=sum(origin, mul(direction, d)),
            normal=normal
        )
            
import mmap
import numpy

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        img = open(self.path, "rb")
        m = mmap.mmap(img.fileno(), 0, access=mmap.ACCESS_READ)
        ba = bytearray(m)
        header_size = struct.unpack("=l", ba[10:14])[0]
        self.width = struct.unpack("=l", ba[18:22])[0]
        self.height = struct.unpack("=l", ba[18:22])[0]
        all_bytes = ba[header_size::]
        self.pixels = numpy.frombuffer(all_bytes, dtype='uint8')
        img.close()

    def get_color(self, direction):
      width = 2000
      height = 1000
      direction = norm(direction)

      x = int((atan2(direction.z, direction.x) / (2 * pi) + 0.5) * width)
      y = int(acos(-direction.y) / pi * height)
      index = (y * self.width + x) * 3 % len(self.pixels)

      processed = self.pixels[index:index+3].astype(numpy.uint8)
      return color(processed[2], processed[1], processed[0])