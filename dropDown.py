import pygame
import os

class DropDown:
  """
  Clase que implementa un menu de estilo drop down con tamaño variable
  """
  def __init__(self, posx, posy, sizex, sizey, contents, color=(255,255,255), text_color=(0,0,0), hover_color=(100,100,100), line_color=(0,0,0), spacing=6, font_size=20, default=0):
    """
    El contenido tienen que ser strings en un array
    """
    self.posx = posx
    self.posy = posy
    self.sizex = sizex
    self.sizey = sizey
    self.contents = contents[:]
    self.length = len(self.contents)
    self.roller_enable = self.length > 5
    self.color = color
    self.text_color = text_color
    self.hover_color = hover_color
    self.is_hover = False
    self.item_hover = -1
    self.line_color = line_color
    self.spacing = spacing
    self.selected = default
    self.active = False
    self.font = pygame.font.SysFont('times new roman', font_size, bold=True)

    if self.roller_enable:
      self.list_offset = default
    else:
      self.list_offset = 0

    x,self.fy = self.font.size(" ")
    del(x)
    self.expanded_size = self.get_expanded_size()
    self.tick_img = pygame.image.load(os.path.join("Imgs/checked.png")).convert_alpha()
    self.tick_img = pygame.transform.scale(self.tick_img, (10, 10))

  def get_expanded_size(self):
    """
    Regresa el tamaño del cuadro de forma expandida
    """
    if self.roller_enable:
      return 5 * self.sizey
    else:
      return self.length * self.sizey

  def get_selected(self):
    return self.contents[self.selected]

  def change_offset(self, button):
    flag = False
    if self.active and self.roller_enable:
      if button == 5:
        if self.list_offset < self.length - 5:
          self.list_offset += 1
          flag = True
      elif button == 4:
        if self.list_offset > 0:
          self.list_offset -= 1
          flag = True
    return flag

  def check_click_box(self, pos):
    """
    Revisa si el click fue adentro de la caja o no
    """
    x,y = pos
    return x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.expanded_size

  def check_item_click(self, pos):
    """
    Revisa que item dentro del drop down fue al que se le dio click
    """
    x,y = pos
    del(x)
    y -= self.posy
    return int(y/self.sizey) + self.list_offset

  def check_hover(self, pos):
    """
    Revisa si la posicion esta sobre el elemento dependiendo del estado
    """
    x,y = pos
    if self.active:
      if self.check_click_box(pos):
        self.item_hover = self.check_item_click(pos)
        return True
      else:
        self.item_hover = -1
        return False
    else:
      self.is_hover = x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey
  
  def check_click(self, pos):
    """
    Revisa cual es el estado actual del menu (abierto o cerrado) actuar en base a eso
    """
    x,y = pos
    if self.active:
      if self.check_click_box(pos):
        self.selected = self.check_item_click(pos)
      self.is_hover = False
      self.item_hover = 0
      self.active = False
      if self.roller_enable:
        if self.length - self.selected >= 5:
          self.list_offset = self.selected
        else:
          self.list_offset = self.length - 5
      return True
    else:
      self.active = x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey
      return False

  def set_active_false(self):
    self.is_hover = False
    self.item_hover = 0
    self.active = False
    if self.roller_enable:
      if self.length - self.selected >= 5:
        self.list_offset = self.selected
      else:
        self.list_offset = self.length - 5

  def paint(self, screen):
    """
    Pinta el drop down dependiendo en el estado en el que se encuentra
    """
    if self.active:
      if self.roller_enable:
        upper_limit = self.list_offset + 5
      else:
        upper_limit = self.length

      pygame.draw.rect(screen, self.color, (self.posx, self.posy, self.sizex, self.expanded_size))
      
      for i in range(self.list_offset , upper_limit):
        if i == self.item_hover:
          pygame.draw.rect(screen, self.hover_color, (self.posx, self.posy + self.sizey*(i-self.list_offset), self.sizex, self.sizey))
        surface = self.font.render(self.contents[i], True, self.text_color)
        screen.blit(surface, (self.posx + self.spacing, int(self.posy + (self.sizey - self.fy)//2 + self.sizey*(i-self.list_offset))))

      pygame.draw.rect(screen, self.line_color, (self.posx, self.posy, self.sizex, self.expanded_size), 3)
      if self.roller_enable:
        if self.selected >= self.list_offset and self.selected < upper_limit:
          screen.blit(self.tick_img, (self.posx + self.sizex - 15, self.posy + (self.sizey - 10)//2 + self.sizey*(self.selected-self.list_offset)))
      else:
        screen.blit(self.tick_img, (self.posx + self.sizex - 15, self.posy + (self.sizey - 10)//2 + self.sizey*self.selected))

    else:
      if self.is_hover:
        back_color = self.hover_color
      else:
        back_color = self.color

      pygame.draw.rect(screen, back_color, (self.posx, self.posy, self.sizex, self.sizey))
      pygame.draw.rect(screen, self.line_color, (self.posx, self.posy, self.sizex, self.sizey), 3)
      fx, fy = self.font.size(self.contents[self.selected])
      del(fx)
      surface = self.font.render(self.contents[self.selected], True, self.text_color)
      screen.blit(surface, (self.posx + self.spacing, self.posy + (self.sizey - fy)//2))

