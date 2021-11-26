import pygame
import numpy
from PIL import Image

from transformations import *

from obj import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import random

WIDTH = 1200
HEIGHT = 800
ASPECT_RATIO = WIDTH/HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0, 0.4, 0.8, 1)
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
    fragColor = vec4(mycolor.xyz, 1.0f);
  } else if (mod(clock/10, 3) == 0) {
    fragColor = vec4(mycolor.yzx, 1.0f);
  } else {
    fragColor = vec4(mycolor.zxy, 1.0f);
  }
}
"""

cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)









# Textura
img = Image.open('clouds.bmp') # la leo
pixels = numpy.array(list(img.getdata()), numpy.int8) # Obtengo los pixeles

textureID = glGenTextures(1);

# GL_TEXTURE_2Dla textura es un arreglo de pixeles de 2 dimensiones
glBindTexture(GL_TEXTURE_2D, textureID);

# Crear la textura
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
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




fragment_shader3 = """
#version 460
layout(location = 0) out vec4 fragColor;
uniform vec3 color;

void main()
{
  fragColor = vec4(color.xyz, 1.0f);
}
"""

cvs3 = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs3 = compileShader(fragment_shader3, GL_FRAGMENT_SHADER)

shader3 = compileProgram(cvs3, cfs3)










mesh = Obj('./dolphin.obj')

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
  ctypes.c_void_p(12)
)
glEnableVertexAttribArray(1)



# Atributos de textura de vértice
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(24))







def render(rotateY, rotateX, rotateZ, actualShader):
  i = glm.mat4(1)

  translate = glm.translate(i, glm.vec3(-1.5, -2, -2))
  rotate = rotationMatrix((rotateX, rotateY, rotateZ))
  scale = glm.scale(i, glm.vec3(2, 2, 2))

  model = translate * rotate * scale
  view = glm.lookAt(glm.vec3(0, 0, 35), glm.vec3(0, -1, 0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), ASPECT_RATIO, 0.1, 1000.0)

  theMatrix = projection * view * model

  glUniformMatrix4fv(
    glGetUniformLocation(actualShader, 'theMatrix'),
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
actualShader = shader2
shaderCounter = 0

while running:
  glUseProgram(actualShader)
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  # Para mostrar el modelo y darle movimiento
  render(rotateX, rotateY, rotateZ, actualShader)
  contador += 1

  if (actualShader != shader3):
      glUniform1i(
        glGetUniformLocation(actualShader, 'clock'), contador
      )
  else:
      r = random.uniform(0, 1)
      g = random.uniform(0, 1)
      b = random.uniform(0, 1)

      glUniform3f(
        glGetUniformLocation(actualShader, 'color'), r, g, b
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
        rotateZ += 0.5
      elif event.key == pygame.K_KP9:
        rotateZ -= 0.5
      elif event.key == pygame.K_KP8:
        rotateY += 0.5
      elif event.key == pygame.K_KP2:
        rotateY -= 0.5
      elif event.key == pygame.K_KP6:
        rotateX += 0.5
      elif event.key == pygame.K_KP4:
        rotateX -= 0.5
      elif event.key == pygame.K_a:
        if (shaderCounter == 0):
          actualShader = shader
        elif (shaderCounter == 2):
          actualShader = shader2
        else:
          actualShader = shader3

        shaderCounter += 1
        shaderCounter = shaderCounter % 3