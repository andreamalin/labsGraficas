import pygame
import numpy
from PIL import Image

from transformations import *
from textures import Texture

from obj import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

WIDTH = 800
HEIGHT = 600
ASPECT_RATIO = WIDTH/HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0.1, 0.2, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()

vertex_shader = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor;

uniform mat4 theMatrix;

out vec3 mycolor;

void main() 
{
  gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
  mycolor = ccolor;
}
"""

fragment_shader = """
#version 460
layout(location = 0) out vec4 fragColor;

uniform int clock;
in vec3 mycolor;

void main()
{
  if (mod(clock/10, 2) == 0) {
    fragColor = vec4(0, 0, 255, 1.0f);
  } else {
    fragColor = vec4(0, 0, 255, 1.0f);
  }
}
"""

cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)









# Textura
img = Image.open('clouds.bmp') # .jpg, .bmp, etc. also work
pixels = numpy.array(list(img.getdata()), numpy.int8)

textureID = glGenTextures(1);

# GL_TEXTURE_2Dla textura es un arreglo de pixeles de 2 dimensiones
glBindTexture(GL_TEXTURE_2D, textureID);

# Crear la textura
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, pixels)


vertex_shader2 = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 vTexture;

uniform mat4 theMatrix;

out vec2 texCoord;

void main()
{
     gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
     texCoord = vTexture; 
}
"""

fragment_shader2 = """
#version 460
in vec2 texCoord;
out vec4 color;

uniform sampler2D myTexture;

void main()
{
       color = texture(myTexture, texCoord);
}
"""

cvs2 = compileShader(vertex_shader2, GL_VERTEX_SHADER)
cfs2 = compileShader(fragment_shader2, GL_FRAGMENT_SHADER)

shader2 = compileProgram(cvs2, cfs2)





mesh = Obj('./dolphin.obj')

print(len(mesh.vertices), len(mesh.tnormales), len(mesh.tvertices))
vertex_data = numpy.hstack((
  numpy.array(mesh.vertices, dtype=numpy.float32),
  numpy.array(mesh.tnormales, dtype=numpy.float32),
)).flatten()

index_data = numpy.array([[vertex[0] - 1 for vertex in face] for face in mesh.faces], dtype=numpy.uint32).flatten()

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)


vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(
  0, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)





element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(
  1, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(4 * 3)
)
glEnableVertexAttribArray(1)



 # Atributos de textura de vértice
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(12))

glUseProgram(shader2)









def render(rotateY, rotateX, rotateZ):
  i = glm.mat4(1)

  translate = glm.translate(i, glm.vec3(-1.5, -2, -2))
  rotate = rotationMatrix((rotateX, rotateY, rotateZ))
  scale = glm.scale(i, glm.vec3(2, 2, 2))

  model = translate * rotate * scale
  view = glm.lookAt(glm.vec3(0, 0, 30), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), ASPECT_RATIO, 0.1, 1000.0)

  theMatrix = projection * view * model

  glUniformMatrix4fv(
    glGetUniformLocation(shader2, 'theMatrix'),
    1,
    GL_FALSE,
    glm.value_ptr(theMatrix)
  )

glViewport(0, 0, WIDTH, HEIGHT)


# Variables
running = True
rotateX = 0
rotateY = 0
rotateZ = 0
contador = 0

while running:
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  # Para mostrar el modelo y darle movimiento
  render(rotateX, rotateY, rotateZ)
  contador += 1

  # Enteros
  # glUniform1i(
  #   glGetUniformLocation(shader2, 'clock'),
  #   contador
  # )

  glUniform1i(
    glGetUniformLocation(shader2, 'texture'), 0
  )

  # Para especificar el tipo -> GL_TRIANGLES rellena mientras GL_LINE_LOOP une los puntos con lineas
  glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

  # Vamos cambiando de buffer
  pygame.display.flip()
  clock.tick(15)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    # Movimiento del modelo usando el keypad
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_KP1:
        rotateZ += 0.1
      elif event.key == pygame.K_KP9:
        rotateZ -= 0.1
      elif event.key == pygame.K_KP8:
        rotateY += 0.1
      elif event.key == pygame.K_KP2:
        rotateY -= 0.1
      elif event.key == pygame.K_KP6:
        rotateX += 0.1
      elif event.key == pygame.K_KP4:
        rotateX -= 0.1