import pygame 
from textBox import TextBox
from dropDown import DropDown
from switchButton import SwitchButton
from boton import Boton
from display import Display
from checkbox import Checkbox 
from magnitudSet import MagnitudSet


class DisplayPanel():
  """
  Display parte superior 
  """
  def __init__(self, posx, posy, sizex, sizey, menu_items=[], back_color=(4, 44, 109), text_color=(0,0,0), font_s=20, font="corbel", s_left=10, s_top=10, s_bottom = 40, s_between = 5, items_sizey=30):

    self.posx = posx
    self.posy = posy
    self.sizex = sizex
    self.sizey = sizey
    self.menu_items = menu_items
    self.menu_length = len(self.menu_items)
    self.back_color = back_color
    self.text_color = text_color
    self.font_size = font_s
    self.font = pygame.font.SysFont(font, font_s, True)
    self.s_left = s_left
    self.s_top = s_top
    self.s_bottom = s_bottom
    self.s_between = s_between
    self.items_sizex = round(self.sizex * 0.164899)
    self.items_sizey = items_sizey
    self.items_pos_y = self.posy + self.sizey - (self.s_bottom + self.items_sizey)//2
    self.carriage_linefeed, self.hex_uni = self.generate_switchBottons()
    self.clear_boton = self.generate_botton()
    self.display = self.generate_display()
    self.checkbox = self.generate_checkbox()
    self.magnitudSet = self.generate_magnitudSet()
    self.lecture_mode = "Line Feed"
    self.clear_flag = 0

  def generate_botton(self):
    """
    Genera el boton de limpia pantalla
    """
    posx = self.posx + self.s_left  
    return Boton(posx, self.items_pos_y, self.items_sizex, self.items_sizey , "CLEAR",font_size=self.font_size)

  def generate_checkbox(self):

    posx = self.posx +self.s_left + self.items_sizex + self.s_between 
    return Checkbox( posx, self.items_pos_y, self.items_sizex, self.items_sizey, text = "Auto-scroll", color=(120,50,40), font_size=self.font_size)

  def generate_switchBottons(self):
    """
    Genera el boton de carriage return o line feed para el panel
    """
    posx = self.posx + 2*self.items_sizex + self.s_left + 2*self.s_between   
    posy = self.items_pos_y
    sizex = self.items_sizex
    sizey = self.items_sizey
    text1 = "\\r"
    text2 = "\\n"
    color = (216, 209, 114)
    color_h=(104, 99, 43)
    text_color=(0,0,0)
    color_click=(104, 99, 43)
    font_size=self.font_size
    act_left = 0
    act_right = 1
    line_carriege = SwitchButton(posx, posy, sizex, sizey, text1, text2, color=color, color_h=color_h, text_color=text_color, color_click=color_click, font_size=font_size, act_left=act_left, act_right=act_right)
    posx = self.posx + round(4.2*self.items_sizex) + self.s_left + 4*self.s_between   
    posy = self.items_pos_y
    sizex = self.items_sizex
    sizey = self.items_sizey
    text1 = "HEX"
    text2 = "UNI"
    color = (216, 209, 114)
    color_h=(104, 99, 43)
    text_color=(0,0,0)
    color_click=(104, 99, 43)
    font_size=self.font_size
    act_left = 0
    act_right = 1
    hex_uni = SwitchButton(posx, posy, sizex, sizey, text1, text2, color=color, color_h=color_h, text_color=text_color, color_click=color_click, font_size=font_size, act_left=act_left, act_right=act_right)
    return (line_carriege, hex_uni)

  def generate_magnitudSet(self):
    """
    Genera el panel para controlar magnitud de font
    """
    posx = self.posx + 3*self.items_sizex + self.s_left + 3*self.s_between   
    return MagnitudSet(posx, self.items_pos_y, round(self.items_sizex*1.2), self.items_sizey, "Size", font_size = self.font_size )  

  def generate_display(self):

    posx = self.posx + self.s_left 
    posy = self.posy + self.s_top
    return Display(posx, posy, self.sizex -2*self.s_left, self.sizey - self.s_bottom - self.s_top)

  def set_file_settings(self, file_name, num_lines, uni_active, hex_active):
    self.display.write_uni_file = uni_active
    self.display.write_hex_file = hex_active
    self.display.length_to_write = num_lines
    self.display.create_files(file_name)

  def save_info_to_files(self):
    self.display.save_info_to_files()

  def check_inside(self, pos):
    """
    Revisa si la posicion esta dentro del click
    """
    x,y = pos
    return x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey

  def event_MOUSEMOTION(self, pos):

    self.display.event_MOUSEMOTION(pos)
    #if self.check_inside(pos):
    self.carriage_linefeed.check_hover(pos)
    self.hex_uni.check_hover(pos)
    self.clear_boton.was_hover(pos)
    self.magnitudSet.event_MOUSEMOTION(pos)

  def event_MOUSEBUTTONDOWN_LEFT(self, pos):

    if self.check_inside(pos):
      selection = self.carriage_linefeed.check_click(pos)
      if selection == "RIGTH":
        self.lecture_mode = "\n"
      elif selection == "LEFT":
        self.lecture_mode = "\r"
      if selection != "NONE":
          self.display.set_end_line_setting(self.lecture_mode)
      selection = self.hex_uni.check_click(pos)
      if selection == "RIGTH":
        self.display.set_display_mode(True)
      elif selection == "LEFT":
        self.display.set_display_mode(False)

      if self.clear_boton.was_click(pos):
        self.display.delete_contents()

      if self.checkbox.was_click(pos):
        self.display.set_auto_scroll(self.checkbox.active)

      self.display.event_MOUSEBUTTONDOWN_LEFT(pos)

      font=self.magnitudSet.event_MOUSEBUTTONDOWN_LEFT(pos)

      if font != -1:
        self.display.change_font_size(font)
      
  def write_to_display_IN_uni(self, string):
    string_carriege = ["IN",string]
    self.display.write_to_display_uni(string_carriege)

  def write_to_display_OUT_uni(self, string):
    string_carriege = ["OUT",string]
    self.display.write_to_display_uni(string_carriege)

  def write_to_display_IN_hex(self, string):
    string_carriege = ["IN", string]
    self.display.write_to_display_hex(string_carriege)

  def write_to_display_OUT_hex(self, string):
    string_carriege = ["OUT", string]
    self.display.write_to_display_hex(string_carriege)

  def event_MOUSEBUTTONDOWN_ROLLER(self, button, pos): 
    self.display.event_MOUSEBUTTONDOWN_ROLLER(button, pos)

  def event_MOUSEBUTTONUP_LEFT(self):
    self.display.event_MOUSEBUTTONUP_LEFT()
    self.clear_boton.released()
    self.magnitudSet.event_MOUSEBUTTONUP_LEFT()

  def paint(self, screen):

    pygame.draw.rect(screen, self.back_color, (self.posx, self.posy, self.sizex, self.sizey))
    self.carriage_linefeed.paint(screen)
    self.hex_uni.paint(screen)
    self.clear_boton.paint(screen)
    self.display.paint(screen)
    self.checkbox.paint(screen)
    self.magnitudSet.paint(screen)
    #self.paint_menu_items(screen)
    #for textBox in self.group_textBox:
    #  textBox.paint(screen)

    #for i in range(self.num_dropDowns-1,-1,-1):
    # self.group_dropDown[i].paint(screen)
