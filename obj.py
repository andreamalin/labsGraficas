class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()

    self.vertices = []
    self.tvertices = []
    self.faces = []
    self.tnormales = []
    self.read()

  def read(self):
    for line in self.lines:
      if line:
        prefix, value = line.split(' ', 1)

        if prefix == 'v':
          self.vertices.append(
            list(map(float, value.split(' ')))
          )
        elif prefix == 'vt':
          textures = list(map(float, value.split(' ')))
          if (len(textures) == 2):
            textures.append(0)
          
          self.tvertices.append(textures)
        elif prefix == 'vn':
          self.tnormales.append(
            list(map(float, value.split(' ')))
          )
        elif prefix == 'f':
          try:
            self.faces.append(
              [list(map(int, face.split('/'))) for face in value.split(' ')]
            )
          except:
            self.faces.append(
              [list(map(int, face.split('/'))) for face in value.split(' ')[0:3]]
            )