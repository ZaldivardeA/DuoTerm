import pygame

class ConsoleDisplay:

  def __init__(self, posx, posy, sizex, sizey, color=(0,0,0), font_size=18, text_color=(255,0,0), spacing=0, padding=5):

    self.posx = posx
    self.posy = posy
    self.sizex = sizex
    self.sizey = sizey
    self.color = color
    self.font = pygame.font.SysFont("consolas", font_size, False)
    self.fx, self.fy = self.font.size(" ")
    self.padding = padding
    self.spacing = spacing
    self.num_char_line = (self.sizex - 2*self.padding)//(self.fx)
    self.num_lines_text = (self.sizey - 2*self.padding)//(self.spacing + self.fy)
    self.offset = 0
    self.length = 0
    self.text_color = text_color
    self.text = []
    self.box = pygame.Surface((self.sizex, self.sizey)).convert()

  def check_inside(self, pos):
    x,y = pos
    bx = x >= self.posx and x <= self.posx + self.sizex
    by = y >= self.posy and y <= self.posy + self.sizey
    return bx and by

  def auto_scroll(self):
    if self.length > self.num_lines_text:
      self.offset = self.length - self.num_lines_text

  def delete_contents(self):
    self.text = []
    self.length = 0
    self.offset = 0

  def event_MOUSEBUTTONDOWN_ROLLER(self, button, pos):
    if self.check_inside(pos):
      if button == 5:
        if self.offset < self.length - self.num_lines_text:
          self.offset += 1
      elif button == 4:
        if self.offset > 0:
          self.offset -= 1

  def write(self, string):
    while len(string) > self.num_char_line:
      self.text.append(string[:self.num_char_line])
      string = string[self.num_char_line:]
      self.length += 1
    self.text.append(string)
    self.length += 1
    self.auto_scroll()

  def process_error(self, code, info=[]):
    message = "ERROR: "
    if code == -1:  #No es posible abrir el puerto
      message += "Cannot open port: " + info[0]
    elif code == -2:  #Puerto tiene que ser un numero
      message += "Port must be an integer."
    elif code == -3:  #No se pudo mandar el dato
      message += "Could not send data into terminal: " + info[0] + ".(Timeout reached) Make sure the device connected can handle incoming data"
    self.write(message) 

  def paint(self, screen):
    self.box.fill(self.color)
    index = 0
    for string in self.text[self.offset:]:
      if index < self.num_lines_text:
        text_sur = self.font.render(string, True, self.text_color)
        posx = self.padding
        posy = self.padding + (self.spacing + self.fy)*index
        self.box.blit(text_sur, (posx, posy))
        index += 1
      else:
        break
    screen.blit(self.box, (self.posx, self.posy))
