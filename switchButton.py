import pygame

class SwitchButton():
  """
  Define una clase que es un boton con dos opciones
  """
  def __init__(self,posx,posy,sizex,sizey,text1="",text2="",center = -1 ,color=(150,150,150),color_h=(100,100,250),text_color=(0,0,0),color_click=(250,10,10), font_size=20, act_left = 1, act_right = 0):
    self.posx = posx
    self.posy = posy
    self.sizey = sizey
    self.sizex = sizex
    if center == -1:
      center = sizex//2
    self.center = center
    self.text1 = text1
    self.text2 = text2
    self.color = color
    self.color_hover = color_h
    self.text_color = text_color
    self.color_click = color_click
    self.font = pygame.font.SysFont('times new roman', font_size, bold=True)
    self.act_left = act_left
    self.act_right = act_right
    self.default = (act_left, act_right)
    self.hoverL = 0
    self.hoverR = 0

  def check_if_inside(self,pos):
    """
    check if cursor is inside the botton
    """
    x , y = pos
    return (x >= self.posx and x <= (self.posx + self.sizex) and y >= self.posy and y <= (self.posy + self.sizey))

  def return_to_default(self):
    """
    Regresa el boton a su estado original
    """
    self.act_left, self.act_right = self.default

  def check_click(self, pos):
    """
    checa que boton fue presionado
    """
    if self.check_if_inside(pos):
      if self.check_if_Left(pos):
        if not self.act_left:
          self.act_left = 1
          self.act_right = 0
          return "LEFT"
        else:
          return "NONE"
      if self.check_if_Right(pos):	
        if not self.act_right:
          self.act_left = 0
          self.act_right = 1
          return "RIGTH"
        else:
          return "NONE"
    return "NONE"
    


  def check_hover(self,pos):
    """
    Funcion que cambia el color del boton cuando el cursor pasa sobre este
    """
    if self.check_if_inside(pos):
      if self.check_if_Left(pos):
        self.hoverL = 1
        self.hoverR = 0
      elif self.check_if_Right(pos):	
        self.hoverR = 1
        self.hoverL = 0
    else:
      self.hoverR = 0
      self.hoverL = 0


  def check_if_Left(self,pos):
    """
    Checa si el cursor esta en el lado izquierdo de los botones
    """
    x , y = pos
    return (x <= (self.posx + self.center))

  def check_if_Right(self,pos):
    """
    Checa si el cursor esta en el lado derecho de los botones
    """
    x , y = pos
    return ( x >= (self.posx + self.center ))
      


  def paint(self,screen):
     
    if self.hoverR == 1 and self.hoverL == 0:
      change_colorR = self.color_hover
      change_colorL = self.color
    elif self.hoverR == 0 and self.hoverL == 1:
      change_colorL = self.color_hover
      change_colorR = self.color
    else:
      change_colorL = self.color
      change_colorR = self.color

    if (self.act_left != 0 or self.act_right != 0):
      if self.act_right == 1:
        change_colorR = self.color_click
      else: 
        change_colorL = self.color_click


    pygame.draw.rect(screen, change_colorL, (self.posx, self.posy, self.sizex - self.center , self.sizey))
    pygame.draw.rect(screen, change_colorR, (self.posx + 1 + self.center, self.posy, self.sizex - self.center, self.sizey))

    fx1, fy1 = self.font.size(self.text1)
    surface = self.font.render(self.text1, True, self.text_color)
    screen.blit(surface, ((self.posx + (self.center)//2) - fx1//2, self.posy + (self.sizey - fy1)//2))

    fx2, fy2 = self.font.size(self.text2)
    surface = self.font.render(self.text2, True, self.text_color)
    screen.blit(surface, (self.posx + self.sizex - self.sizex//4 - fx2//2, self.posy + (self.sizey - fy2)//2))