import pygame
from textBox import TextBox
from switchButton import SwitchButton
from boton import Boton

def generate_text():
  ans = ["File Name:", "Save each # of lines:", "Unicode file:", "HEX file:"]
  return ans[:]

class TestConfigPanel:

  def __init__(self, posx, posy, sizex, sizey, background_c=(220,220,220), text_color=(0,0,0)):
    self.posx = posx
    self.posy = posy
    self.sizex = sizex
    self.sizey = sizey
    self.text_color = text_color
    self.font_size = round(self.sizex * 0.047619047)
    self.font = pygame.font.SysFont("times new roman", self.font_size, False)
    self.s_left = round(self.sizex*0.01680672)
    self.s_text_inter = round(self.sizex * 0.0140056022)
    self.s_top = round(self.sizey*0.031578947)
    self.s_between = self.s_top
    self.items_sizey = round(self.sizey*0.157894736)
    self.items_sizex = round(self.sizex*0.560224089)
    self.back_color = background_c
    self.textBoxes_text = generate_text()
    self.textBoxes_text_len = len(self.textBoxes_text)
    self.text_sizex = self.get_longest_menu_item_size()
    self.textBoxes = self.generate_textBoxs()
    self.switches = self.generate_switches()
    self.close_button = self.generate_button()
    self.switches_states = [False, False] # si o no escribir los archivos de unicode y hex
    self.active = False

  def get_longest_menu_item_size(self):
    maximum = 0
    for item in self.textBoxes_text:
      fx,fy = self.font.size(item)
      if fx > maximum:
        maximum = fx
    return maximum

  def generate_textBoxs(self):
    group = []
    posx = self.posx + self.s_left + self.s_text_inter + self.text_sizex
    for i in range(0,2):
      posy = self.posy + self.s_top + (self.items_sizey+self.s_between)*i
      group.append(TextBox(posx, posy, self.items_sizex, self.items_sizey, color=(176, 184, 196), font_size=self.font_size))
    return group[:]

  def generate_switches(self):
    group = []
    posx = self.posx + self.s_left + self.s_text_inter + self.text_sizex
    posy = self.posy + self.s_top + (self.items_sizey+self.s_between)*2
    for i in range(0,2):
      posy += (self.items_sizey+self.s_between)*i
      group.append(SwitchButton(posx, posy, self.items_sizex, self.items_sizey, "Yes", "No", act_left = False, act_right = True))
    return group[:]

  def generate_button(self):
    posx = self.posx + self.s_left + self.s_text_inter + self.text_sizex
    posy = self.posy + self.s_top + (self.items_sizey+self.s_between)*4
    text = "CLOSE"
    return Boton(posx, posy, self.items_sizex, self.items_sizey, text)

  def set_activated(self, on_off):
    self.active = on_off

  def get_settings(self):
    if self.switches[0].act_left or self.switches[1].act_left:
      if len(self.textBoxes[0].text) > 0:
        file_name = self.textBoxes[0].text
      else:
        return -4 # invalid file name error
      try:
        number_lines = int(self.textBoxes[1].text)
      except:
        return -5 # number of lines has to be an integer
      uni_active = self.switches[0].act_left
      hex_active = self.switches[1].act_left
      return [file_name, number_lines, uni_active, hex_active]
    return None

  def check_inside(self, pos):
    x, y = pos
    bx = x >= self.posx and x <= self.posx + self.sizex
    by = y >= self.posy and y <= self.posy + self.sizey
    return bx and by

  def event_KEYDOWN(self, key):
    if self.active:
      for textBox in self.textBoxes:
        textBox.write_in_box(key)

  def event_KEYUP(self):
    if self.active:
      for textBox in self.textBoxes:
        textBox.event_KEYUP()

  def frame_process(self):
    if self.active:
      for textBox in self.textBoxes:
        textBox.process_backspace()

  def event_MOUSEBUTTONDOWN_LEFT(self, pos):
    if self.active:
      if self.check_inside(pos):
        if self.close_button.was_click(pos):
          self.active = False
          self.close_button.released()
          self.close_button.is_hover = False
          return "CLOSE"
        for i in range(0,2):
          ans = self.switches[i].check_click(pos)
          if ans != "NONE":
            self.switches_states[i] = ans == "LEFT"
      for textBox in self.textBoxes:
          textBox.check_click(pos)
    return None

  def event_MOUSEMOTION(self, pos):
    if self.active:
      for switch in self.switches:
        switch.check_hover(pos)
      self.close_button.was_hover(pos)
  
  def paint_menu(self, screen):
    fx, fy = self.font.size(" ")
    del fx
    for i in range(0,self.textBoxes_text_len):
      surface = self.font.render(self.textBoxes_text[i], True, self.text_color)
      screen.blit(surface, (self.posx + self.s_left, self.posy + self.s_top + (self.items_sizey + self.s_between)*i + (self.items_sizey-fy)//2))

  def paint(self, screen):
    if self.active:
      pygame.draw.rect(screen, self.back_color, (self.posx, self.posy, self.sizex, self.sizey))
      for textBox in self.textBoxes:
        textBox.paint(screen)
      for switch in self.switches:
        switch.paint(screen)
      self.paint_menu(screen)
      self.close_button.paint(screen)
      