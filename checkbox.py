



import pygame
import os 

class Checkbox:

  def __init__(self,posx,posy,sizex, sizey,text = "",text_color=(255,255,255), color = (200,200,60),click_color = (0,0,0), font_size=15):
    
    self.posx = int(posx)
    self.posy = int(posy)
    self.sizex = int(sizex)
    self.sizey = int(sizey)
    self.color = color
    self.text = text
    self.text_color = text_color
    self.font = pygame.font.SysFont('corbel', font_size, bold=True)
    self.active = True
    self.color_check = (255,255,255) 
    self.click_color = click_color
    self.box_x = 0
    self.box_y = 0
    self.tick_x = 0
    self.tick_y = 0
    self.spacing_x = 5
    self.tick_img = pygame.image.load(os.path.join("Imgs/checked.png")).convert_alpha()
    self.tick_img = pygame.transform.scale(self.tick_img,self.set_box_size())
    

  def was_click(self,pos):
    """
    Checa si el boton fue presionado
    """
    x , y = pos 
    if x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey:
      self.active = not self.active
      return True

    return False

  def set_box_size(self):
    self.box_x = 15
    self.box_y = 15
    self.tick_x = int((2*self.box_x)/3)
    self.tick_y = int((2*self.box_y)/3)

    return ( self.tick_x , self.tick_y)


  def paint(self, screen):


    pygame.draw.rect(screen, self.color, (self.posx, self.posy, self.sizex, self.sizey))
    pygame.draw.rect(screen, (255,255,255),(self.posx + self.sizex - self.box_x - self.spacing_x, self.posy + (self.sizey - self.box_y)//2, self.box_x, self.box_y))

    if self.active:
      screen.blit(self.tick_img,(self.posx + self.sizex - self.box_x - self.spacing_x +(self.box_x - self.tick_x)//2, self.posy + (self.sizey - self.tick_y)//2 ))    

    fx, fy = self.font.size(self.text)
    surface = self.font.render(self.text, True, self.text_color)
    screen.blit(surface, (self.posx + self.spacing_x, self.posy + (self.sizey - fy)//2))