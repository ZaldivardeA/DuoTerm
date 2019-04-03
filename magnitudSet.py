

import pygame 
import os
from boton import Boton


class MagnitudSet():



  def __init__(self,posx,posy,sizex,sizey,text="",color=(178, 174, 242),color_h=(100,100,100),text_color=(0,0,0), font_size=20 ,sizebotx=30, sizeboty=15,between=5):
    self.posx = posx
    self.posy = posy
    self.sizey = sizey
    self.sizex = sizex
    self.text = text
    self.back_color = color
    self.color_hover = color_h
    self.text_color = text_color
    self.font = pygame.font.SysFont('corbel', font_size, bold=True)
    self.font_size = font_size
    self.sizebotx= sizebotx 
    self.sizeboty = sizeboty
    self.between = between
    self.boton_up = self.generate_bottonUp()
    self.boton_down = self.generate_bottonDown()
    self.boton_set = self.generate_bottonSet()
    self.arrow_img = pygame.image.load(os.path.join("Imgs/arrow.png")).convert_alpha()
    self.arrow_img_down = pygame.transform.scale(self.arrow_img,(self.sizebotx,self.sizeboty))
    self.arrow_img_up = pygame.transform.rotate(self.arrow_img_down,180)
    self.font_size = 20
    self.is_hover = False




  def generate_bottonUp(self):
    """
    Genera el boton up 
    """
    posx = self.posx + self.sizex - 2*self.sizebotx    
    posy = self.posy  
    return Boton(posx, posy, self.sizebotx , self.sizeboty, color=(229, 57, 57),color_h=(186, 44, 44),text_color=(0,0,0),  press_color = (150, 34, 34), font_size=5)


  def generate_bottonDown(self):
    """
    Genera el boton down
    """
    posx = self.posx + self.sizex - 2*self.sizebotx   
    posy = self.posy + self.sizeboty  
    return Boton(posx, posy, self.sizebotx, self.sizeboty, color=(124, 117, 221), color_h=(95, 90, 173), text_color=(0,0,0), press_color = (36, 26, 117), font_size=5)


  def generate_bottonSet(self):
    """
    Genera el boton set size
    """
    posx = self.posx + self.sizex - self.sizebotx
    posy = self.posy
    return Boton(posx, posy, self.sizebotx,self.sizey , "Set", color=(210, 232, 125), color_h=(166, 183, 99), press_color = (131, 145, 77),text_color=(0,0,0), font_size=10)


  def check_inside(self, pos):
    """
    Revisa si la posicion esta dentro del click
    """
    x,y = pos
    return x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey


  def event_MOUSEMOTION(self, pos):

    #if self.check_inside(pos):
    self.boton_up.was_hover(pos)
    self.boton_down.was_hover(pos)
    self.boton_set.was_hover(pos)

  def event_MOUSEBUTTONDOWN_LEFT(self, pos):
    if self.check_inside(pos):
      if self.boton_set.was_click(pos):
        return self.font_size
      
      elif self.boton_up.was_click(pos):
        if self.font_size < 35 :
          self.font_size += 1
        

      elif self.boton_down.was_click(pos):
        if self.font_size > 15 : 
          self.font_size -= 1

    return -1 

  def event_MOUSEBUTTONUP_LEFT(self):
    self.boton_set.released()
    self.boton_down.released()
    self.boton_up.released()



  def paint(self, screen):

    pygame.draw.rect(screen, self.back_color, (self.posx, self.posy, self.sizex, self.sizey))
    self.boton_up.paint(screen)
    self.boton_down.paint(screen)
    self.boton_set.paint(screen)

    screen.blit(self.arrow_img_up,(self.posx + self.sizex - 2*self.sizebotx , self.posy))

    screen.blit(self.arrow_img_down,(self.posx + self.sizex - 2*self.sizebotx  , self.posy + self.sizeboty))

    fx, fy = self.font.size(self.text)
    surface = self.font.render(self.text, True, self.text_color)
    screen.blit(surface, (self.posx + self.between , self.posy + (self.sizey - fy)//2))

    fx, fy = self.font.size(str(self.font_size))
    surface = self.font.render(str(self.font_size),True,self.text_color)
    screen.blit(surface, (self.posx + self.sizex - 2*self.sizebotx - self.between - fx , self.posy + (self.sizey- fy)//2))
