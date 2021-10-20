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
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

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
    return round(xs[0]), round(xs[-1]), round(ys[0]), round(ys[-1])

# Barycentric
def barycentric(A, B, C, P):
  cx, cy, cz = cross(
      V3(C.x - A.x, B.x - A.x, A.x - P.x),
      V3(C.y - A.y, B.y - A.y, A.y - P.y)
  )

  if cz == 0:
      return -1, -1, -1

  u = cx/cz
  v = cy/cz
  w = 1 - (u + v)

  return w, v, u


# Vector
def reflect(I, N):
    # R = I - 2 (N.I)N
    a = 2 * dot(I, N)
    return norm(sub(I, mul(N, a)))

def refract(I, N, refractive_index):
  cosi = -max(-1, min(1, dot(I, N))) # Angulo en el que entra la luz entre -1 y 1

  etai = 1 # Viene del aire
  etat = refractive_index # El que recibo

  if cosi < 0:
    cosi = -cosi # Lo volvemos positivo
    etai, etat = etat, etai # Volteo los coeficientes
    N = mul(N, -1)

  eta = etai/etat
  k = 1 - eta**2 * (1 - cosi**2) # Segundo angulo

  # No hay refraccion, solo reflexion
  if (k < 0):
    return None

  # Refraccion
  return norm(sum(mul(I, eta), mul(N, (eta * cosi) + k ** 0.5)))