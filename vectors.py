from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])


# Suma de vectores
def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

# Resta de vectores
def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

# Multiplicacion de vectores
def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

# Producto punto
def dot(v0, v1):
  return v0.x * v1.x + v0.z * v1.z + v0.z * v1.z

# Producto cruz
def cross(v0, v1):
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

# Longitud del vector
def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

# Normal
def norm(v0):
  l = length(v0)

  if l == 0:
    return V3(0, 0, 0)

  return V3(v0.x/l, v0.y/l, v0.z/l)

# Bounding box
def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    ys = [A.y, B.y, C.y]
    xs.sort()
    ys.sort()
    return xs[0], xs[-1], ys[0], ys[-1]

# Barycentric
def barycentric(A, B, C, P):
  cx, cy, cz = cross(
      V3(B.x - A.x, C.x - A.x, A.x - P.x),
      V3(B.y - A.y, C.y - A.y, A.y - P.y)
  )

  if cz == 0:
      return -1, -1, -1

  u = cx/cz
  v = cy/cz
  w = 1 - (u + v)

  return u, v, w