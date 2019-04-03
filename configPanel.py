import pygame
from textBox import TextBox
from dropDown import DropDown
from switchButton import SwitchButton
from textBoxSend import TextBoxSend
from consoleDisplay import ConsoleDisplay
from boton import Boton
from boton import ImgBoton
from testConfigPanel import TestConfigPanel

class ConfigPanel:
  """
  Implementa el panel de configuracion de la aplicacion con cuadros de texto, menus dropDown, botones y switches
  """
  def __init__(self, posx, posy, sizex, sizey, menu_items=[], font_s=20, back_color=(150,150,150), text_color=(0,0,0), font="times new roman", s_left=10, s_top=10, s_text_inter=6):
    """
    Constructor de la clase
    """
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
    self.menu_items_sizex = self.get_longest_menu_item_size()
    self.s_left = s_left
    self.s_top = s_top
    self.s_text_inter = s_text_inter
    self.s_between = round(self.sizey * 0.0220588)
    self.items_sizex = self.get_longest_drop_down_item_size()
    self.items_sizey = round(self.sizey * 0.11029)
    self.group_textBox = self.generate_textBoxs()
    self.num_textBox = len(self.group_textBox)
    self.dropDown_options = self.generate_dropDowns_options()
    self.dropDwon_defaults = self.generate_dropDowns_defaults()
    self.group_dropDown = self.generate_dropDowns()
    self.num_dropDowns = len(self.group_dropDown)
    self.open_close = self.generate_switchBotton()
    self.port_state = "CLOSE"
    self.textBoxSend = self.generate_textBoxSend()
    self.console = self.generate_console()
    self.test_config_button = self.generate_config_buttton()
    self.test_config_panel = self.generate_config_panel()

  def get_longest_menu_item_size(self):
    """
    Regresa el tamaño del item en el menu más largo
    """
    maximum = 0
    for item in self.menu_items:
      fx,fy = self.font.size(item)
      if fx > maximum:
        maximum = fx
    return maximum

  def close_port(self):
    self.port_state = "CLOSE"
    self.open_close.return_to_default()

  def generate_config_panel(self):
    sizex = round(self.sizex*0.42)
    sizey = round(self.sizey*0.7)
    posx = self.posx + round(self.sizex*0.51)
    posy = self.posy + round(self.sizey*0.1)
    return TestConfigPanel(posx, posy, sizex, sizey)

  def generate_config_buttton(self):
    posx = self.sizex + self.posx - self.s_left - round(self.sizex*0.0588928)
    posy = self.posy + round(self.sizey * 0.75)
    sizex = round(self.sizex*0.0588928)
    sizey = sizex
    return ImgBoton(posx, posy, sizex, sizey, color=(150,150,150))

  def generate_console(self):
    posy = self.posy + self.s_top + 2*(self.items_sizey + self.s_between)
    posx = self.posx + self.s_left + self.s_text_inter + self.menu_items_sizex + 2*self.s_between + self.items_sizex
    sizex = self.sizex - (posx-self.posx) - self.s_left - round(self.sizex*0.0588928) - self.s_between
    sizey = self.items_sizey*5 + self.s_between*4
    color = (30,30,30)
    return ConsoleDisplay(posx, posy, sizex, sizey, color=color, font_size = round(self.font_size*0.8))

  def generate_dropDowns_options(self):
    """
    Genera la matriz para las opciones de los drop down
    """
    return [["110", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200",],["5", "6", "7", "8"],["NONE", "EVEN", "ODD"],["STOPBITS_ONE", "STOPBITS_TWO"]]

  def generate_dropDowns_defaults(self):
    """
    Genera el arreglo para los valores default de inicio de los drop down 
    """
    return [6,3,0,0]

  def get_longest_drop_down_item_size(self):
    """
    Regresa el tamaño más grande en x de los menus drop down
    """
    config_list = self.generate_dropDowns_options()
    maximum = 0
    for drop_down_list in config_list:
      for item in drop_down_list:
        fx, fy = self.font.size(item)
        if fx > maximum:
          maximum = fx
    return maximum + 40

  def generate_switchBotton(self):
    """
    Genera el boton de open/close para el panel
    """
    posx = self.posx + self.s_left + self.s_text_inter + self.menu_items_sizex
    posy = self.posy + self.s_top + 6*(self.items_sizey+self.s_between)
    return SwitchButton(posx, posy, self.items_sizex, self.items_sizey, "OPEN", "CLOSE",color=(216, 209, 114),color_h=(104, 99, 43),text_color=(0,0,0),color_click=(104, 99, 43),font_size=self.font_size, act_left = 0, act_right = 1)

  def generate_dropDowns(self):
    """
    Genera el arreglo de DropDowns
    """
    group = []
    posx = self.posx + self.s_left + self.s_text_inter + self.menu_items_sizex
    for i in range(0,4):
      group.append(DropDown(posx , self.posy + self.s_top + 2*(self.items_sizey+self.s_between) + (self.items_sizey+self.s_between)*i, self.items_sizex, self.items_sizey, self.dropDown_options[i], default=self.dropDwon_defaults[i],color = (176, 184, 196),font_size=self.font_size))

    return group[:]

  def generate_textBoxs(self):
    """
    Genera el arreglo de TextBoxes
    """
    group = []
    posx = self.posx + self.s_left + self.s_text_inter + self.menu_items_sizex
    for i in range(0,2):
      group.append(TextBox(posx , self.posy + self.s_top + (self.items_sizey+self.s_between)*i, self.items_sizex, self.items_sizey, color=(176, 184, 196), font_size=self.font_size))

    return group[:]

  def generate_textBoxSend(self):
    #posx = self.posx + self.s_left + self.s_text_inter + self.menu_items_sizex + self.items_sizex + 100
    posx = self.posx + self.s_left + self.s_text_inter + self.menu_items_sizex + 2*self.s_between + self.items_sizex
    posy = self.posy + self.s_top
    sizex = self.items_sizex
    sizey = self.items_sizey
    title = "Send:"
    return TextBoxSend(posx, posy, sizex, sizey, title, color=(176, 184, 196), font_size=self.font_size)

  def paint_menu_items(self, screen):
    """
    Pinta el texto del menu
    """
    fx, fy = self.font.size(" ")
    del fx
    for i in range(0,self.menu_length):
      surface = self.font.render(self.menu_items[i], True, self.text_color)
      screen.blit(surface, (self.posx + self.s_left, self.posy + self.s_top + (self.items_sizey + self.s_between)*i + (self.items_sizey-fy)//2))

  def write_in_console(self, string):
    self.console.write(string)

  def write_errors(self, code, info=[]):
    self.console.process_error(code, info)

  def check_inside(self, pos):
    """
    Revisa si la posicion esta dentro del click
    """
    x,y = pos
    return x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey

  def get_config(self):
    """
    Regresa la configuracion seleccionada
    """
    config = []
    try:
      config.append(self.group_textBox[0].get_text())
      config.append("COM"+str(int(self.group_textBox[1].get_text())))
      config.append(int(self.group_dropDown[0].get_selected()))
      config.append(int(self.group_dropDown[1].get_selected()))
      config.append(self.group_dropDown[2].get_selected())
      config.append(self.group_dropDown[3].get_selected())
      return config[:]
    except:
      self.open_close.return_to_default()
      self.port_state = "CLOSE"
      return "ERROR"
    
  def process_test_close(self):
    self.test_config_button.is_hover = False

  def event_KEYDOWN(self, key):
    if not self.test_config_panel.active:
      for textBox in self.group_textBox:
        textBox.write_in_box(key)
      self.textBoxSend.write_in_box(key)
    else:
      self.test_config_panel.event_KEYDOWN(key)

  def event_KEYUP(self):
    for textBox in self.group_textBox:
      textBox.event_KEYUP()
    self.textBoxSend.event_KEYUP()
    self.test_config_panel.event_KEYUP()

  def frame_process(self):
    if not self.test_config_panel.active:
      for textBox in self.group_textBox:
        textBox.process_backspace()
      self.textBoxSend.process_backspace()
    else:
      self.test_config_panel.frame_process()

  def event_MOUSEBUTTONUP_LEFT(self):
    if not self.test_config_panel.active:
      self.textBoxSend.event_MOUSEBUTTONUP()
    else:
      self.test_config_button.released()

  def event_MOUSEBUTTONDOWN_LEFT(self, pos):
    if not self.test_config_panel.active:
      if self.check_inside(pos):
        flag = True
        if self.test_config_button.was_click(pos):
          self.test_config_panel.set_activated(True)
        if self.port_state == "CLOSE":
          for textBox in self.group_textBox:
            textBox.check_click(pos)
          for dropDown in self.group_dropDown:
            if dropDown.check_click(pos):
              flag = False
              break
          self.textBoxSend.event_MOUSEBUTTONDOWN(pos)
        else:
          text_send = self.textBoxSend.event_MOUSEBUTTONDOWN(pos)
          if text_send != None:
            return text_send
        if flag:
          selection = self.open_close.check_click(pos)
          if selection == "RIGTH":
            self.port_state = -1   #CLOSE
          elif selection == "LEFT":
            self.port_state = -2    #OPEN
          if selection != "NONE":
            return self.port_state
        return None
      else:
        for textBox in self.group_textBox:
          textBox.set_focus_false()
        self.textBoxSend.set_focus_false()

        for dropDown in self.group_dropDown:
          dropDown.set_active_false()
        return None
    else:
      result = self.test_config_panel.event_MOUSEBUTTONDOWN_LEFT(pos)
      if result == "CLOSE":
        self.process_test_close()

  def event_MOUSEMOTION(self, pos):
    if not self.test_config_panel.active:
      if self.check_inside(pos):
        if self.port_state == "CLOSE":
          for dropDown in self.group_dropDown:
              if dropDown.check_hover(pos):
                break
        self.open_close.check_hover(pos)
      self.textBoxSend.event_MOUSEMOTION(pos)
      self.test_config_button.was_hover(pos)
    else:
      self.test_config_panel.event_MOUSEMOTION(pos)

  def event_MOUSEBUTTONDOWN_ROLLER(self, button, pos):
    if not self.test_config_panel.active:
      flag = False
      i = 0
      index = -1
      for dropDown in self.group_dropDown:
        if dropDown.change_offset(button):
          flag = True
          index = i

      if self.check_inside(pos):
        if flag:
          self.group_dropDown[index].check_hover(pos)
        self.console.event_MOUSEBUTTONDOWN_ROLLER(button, pos)

  def paint(self, screen):

    pygame.draw.rect(screen, self.back_color, (self.posx, self.posy, self.sizex, self.sizey))
    self.open_close.paint(screen)
    self.paint_menu_items(screen)
    for textBox in self.group_textBox:
      textBox.paint(screen)
    
    self.textBoxSend.paint(screen)
    self.console.paint(screen)
    for i in range(self.num_dropDowns-1,-1,-1):
      self.group_dropDown[i].paint(screen)
    self.test_config_button.paint(screen)
    self.test_config_panel.paint(screen)

