import pygame
import os
#cambio
#cambio 2
class Boton():
    """
    Define una clase que representa un botón y sus funcionalidades
    """
    def __init__(self,posx,posy,sizex,sizey,text="",color=(255,255,255),color_h=(100,100,100),text_color=(0,0,0), font_size=20, press_color=(135, 125, 125)):
      self.posx = posx
      self.posy = posy
      self.sizey = sizey
      self.sizex = sizex
      self.color = color
      self.color_hover = color_h
      self.is_hover = False
      self.text = text
      self.text_color = text_color
      self.font = pygame.font.SysFont('corbel', font_size, bold=True)
      self.click_flag = False
      self.press_color = press_color

    def was_click(self,pos):
      """
      Checa si el boton fue presionado
      """
      x , y = pos 
      if x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey:
        self.click_flag = True
        return True 
      return False

    def released(self):
      self.click_flag = False
    
    def was_hover(self,pos):
      """
      Funcion que cambia el color del boton cuando el cursor pasa sobre este
      """
      x , y = pos
      self.is_hover = (x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey)

    def paint(self,screen):

      if self.click_flag:
          change_color = self.press_color
      else: 
        if self.is_hover:
          change_color = self.color_hover
        else:
          change_color = self.color

      pygame.draw.rect(screen, change_color, (self.posx, self.posy, self.sizex, self.sizey))
      fx, fy = self.font.size(self.text)
      surface = self.font.render(self.text, True, self.text_color)
      screen.blit(surface, (self.posx + (self.sizex - fx)//2, self.posy + (self.sizey - fy)//2))

class ImgBoton(Boton):

  def __init__(self,posx,posy,sizex,sizey, img_path="Imgs/gear.png", img_hover="Imgs/gear_blue.png",text="",color=(255,255,255),color_h=(100,100,100),text_color=(0,0,0), font_size=20, press_color=(135, 125, 125)):
    super().__init__(posx, posy, sizex, sizey, "", color, color_h, text_color, font_size, press_color)
    self.img = pygame.image.load(os.path.join(img_path)).convert_alpha()
    self.img = pygame.transform.scale(self.img, self.set_img_size())
    self.img_hover = pygame.image.load(os.path.join(img_hover)).convert_alpha()
    self.img_hover = pygame.transform.scale(self.img_hover, self.set_img_size())
    self.img_posx = round(self.sizex*0.1)
    self.img_posy = round(self.sizey*0.1)

  def set_img_size(self):
    sizex = round(self.sizex*0.8)
    sizey = round(self.sizey*0.8)
    return (sizex, sizey)

  def paint(self, screen):
    pygame.draw.rect(screen, self.color, (self.posx, self.posy, self.sizex, self.sizey))
    if self.click_flag:
      screen.blit(self.img, (self.posx + self.img_posx, self.posy + self.img_posy))
    else:
      if self.is_hover:
        screen.blit(self.img_hover, (self.posx + self.img_posx, self.posy + self.img_posy))
      else:
        screen.blit(self.img, (self.posx + self.img_posx, self.posy + self.img_posy))