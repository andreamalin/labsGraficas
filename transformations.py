from vectors import *
from math import sin, cos

A = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]
B = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]

# Multplicacion de matrices
def mulMatrix(A, B):
    newMatrix = []

    # Filas de A
    for i in range(len(A)):
        lista = []
        
        # Obtengo la filas de B
        for j in range(len(B[0])):
            actualRes = 0
            # Obtengo la columna de B
            columnB = [row[j] for row in B]
        
            rowA = A[i]
            for k in range(len(rowA)):
                actualRes += A[i][k] * columnB[k]

            # Luego de multiplicar todos los elementos de A con B,
            # meter ese resultado a la matriz resultante
            lista.append(actualRes)
        newMatrix.append(lista)

    return newMatrix


# Translation
def translateMatrix(point):
    translate = V3(*point)
    
    translationMatrix = [
        [1, 0, 0, translate.x],
        [0, 1, 0, translate.y],
        [0, 0, 1, translate.z],
        [0, 0, 0, 1],
    ]

    return translationMatrix

# Rotation
def rotationMatrix(point):
    rotate = V3(*point)

    a = rotate.x
    rotateX = [
        [1, 0, 0, 0],
        [0, cos(a), -sin(a), 0],
        [0, sin(a), cos(a), 0],
        [0, 0, 0, 1],
    ]

    b = rotate.y
    rotateY = [
        [cos(b), 0, sin(b), 0],
        [0, 1, 0, 0],
        [-sin(b), 0, cos(b), 0],
        [0, 0, 0, 1],
    ]

    c = rotate.z
    rotateZ = [
        [cos(c), -sin(c), 0, 0],
        [sin(c), cos(c), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]

    return mulMatrix(rotateX, mulMatrix(rotateY, rotateZ))


# Scale
def scaleMatrix(point):
    scale = V3(*point)

    scaleMatrix = [
        [scale.x, 0, 0, 0],
        [0, scale.y, 0, 0],
        [0, 0, scale.z, 0],
        [0, 0, 0, 1],
    ]

    return scaleMatrix


