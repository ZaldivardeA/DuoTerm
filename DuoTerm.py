import pygame
from configPanel import ConfigPanel
from displayPanel import DisplayPanel
import serial
import os

pygame.init()

class Window(object):

  def __init__(self, s_left=10, s_top=10, s_between=10, s_right=10, s_bottom = 6):
    pygame.display.set_caption("DuoTerm")
    self.info = pygame.display.Info()
    self.s_left = s_left
    self.s_right = s_right
    self.s_between = s_between
    self.s_top = s_top
    self.s_bottom = s_bottom
    self.sizex , self.sizey, self.font_size = self.get_sizes()
    self.screen = pygame.display.set_mode((self.sizex, self.sizey), pygame.DOUBLEBUF)
    self.background = pygame.Surface((self.sizex,self.sizey)).convert()
    self.term1 = serial.Serial()
    self.term1.close()
    self.term2 = serial.Serial()
    self.term2.close()
    self.clock = pygame.time.Clock()
    self.icon = pygame.image.load(os.path.join("Imgs/terminal.png")).convert_alpha()
    self.icon = pygame.transform.scale(self.icon, (32, 32))
    pygame.display.set_icon(self.icon)

    self.position_y_sett = round(self.sizey * 0.2921)

    self.displayPanel1 = self.generate_DisplayPanel(self.s_left)
    self.displayPanel2 = self.generate_DisplayPanel(self.sizex//2 + self.s_between//2)

    self.configPanel1 = self.generate_ConfigPanel(self.s_left)
    self.configPanel2 = self.generate_ConfigPanel(self.sizex//2 + self.s_between//2)

  def generate_ConfigPanel(self, posx):
    """
    Genera un config panel dependiendo la posicion en x de entrada
    """
    posy = self.sizey - self.position_y_sett
    sizex = self.sizex//2 - self.s_left - self.s_between//2
    sizey = self.position_y_sett - 2*self.s_bottom
    menu_items = ["Port Name:","Port Number:","Baud Rate:","Word Size:","Parity:","Stop Bits:"]

    return ConfigPanel(posx, posy, sizex, sizey, menu_items, self.font_size)

  def generate_DisplayPanel(self, posx):
    """
    Genera un display panel dependiendo de la posicion x de entrada
    """
    posy = self.s_top
    sizex = self.sizex//2 - self.s_left - self.s_between//2
    sizey = self.sizey - self.position_y_sett - self.s_between//2 - self.s_top

    return DisplayPanel(posx, posy, sizex, sizey, font_s=self.font_size)

  def transform_to_hex(self, encoded):
    hex_string = ""
    for byte in encoded:
      hex_string += hex(byte) + " "
    return hex_string

  def open_term1(self, config):
    if config != "ERROR":
      port = config[1]
      baudrate = config[2]

      if config[3] == 5:
        bytesize = serial.FIVEBITS
      elif config[3] == 6:
        bytesize = serial.SIXBITS
      elif config[3] == 7:
        bytesize = serial.SEVENBITS
      elif config[3] == 8:
        bytesize = serial.EIGHTBITS

      if config[4] == "NONE":
        parity = serial.PARITY_NONE
      elif config[4] == "EVEN":
        parity = serial.PARITY_EVEN
      elif config[4] == "ODD":
        parity = serial.PARITY_ODD

      if config[5] == "STOPBITS_ONE":
        stopbits = serial.STOPBITS_ONE
      elif config[5] == "STOPBITS_TWO":
        stopbits = serial.STOPBITS_TWO
      try:
        self.term1 = serial.Serial(port, baudrate, bytesize, parity, stopbits, write_timeout=0.2)
      except:
        self.close_term1()
        self.configPanel1.write_errors(-1, [port])
    else:
        self.configPanel1.write_errors(-2)

  def close_term1(self):
    self.term1.close()
    self.configPanel1.close_port()

  def read_term1(self):
    if self.term1.is_open:
      try:
        if self.term1.in_waiting > 0:
          data = self.term1.read(self.term1.in_waiting)
          data_str = data.decode()
          data_hex = self.transform_to_hex(data)
          self.displayPanel1.write_to_display_OUT_uni(data_str)
          self.displayPanel1.write_to_display_OUT_hex(data_hex)
          if self.term2.is_open:
            try:
              self.term2.write(data)
            except:
              self.configPanel2.write_errors(-3, ["2"])
            self.displayPanel2.write_to_display_IN_uni(data_str)
            self.displayPanel2.write_to_display_IN_hex(data_hex)
      except:
        self.term1.close()

  def open_term2(self, config):
    if config != "ERROR":
      port = config[1]
      baudrate = config[2]

      if config[3] == 5:
        bytesize = serial.FIVEBITS
      elif config[3] == 6:
        bytesize = serial.SIXBITS
      elif config[3] == 7:
        bytesize = serial.SEVENBITS
      elif config[3] == 8:
        bytesize = serial.EIGHTBITS

      if config[4] == "NONE":
        parity = serial.PARITY_NONE
      elif config[4] == "EVEN":
        parity = serial.PARITY_EVEN
      elif config[4] == "ODD":
        parity = serial.PARITY_ODD

      if config[5] == "STOPBITS_ONE":
        stopbits = serial.STOPBITS_ONE
      elif config[5] == "STOPBITS_TWO":
        stopbits = serial.STOPBITS_TWO
      try:
        self.term2 = serial.Serial(port, baudrate, bytesize, parity, stopbits, write_timeout=0.2)
      except:
        self.close_term2()
        self.configPanel2.write_errors(-1, [port])
    else:
      self.configPanel2.write_errors(-2)

  def close_term2(self):
    self.term2.close()
    self.configPanel2.close_port()

  def read_term2(self):
    if self.term2.is_open:
      try:
        if self.term2.in_waiting > 0:
          data = self.term2.read(self.term2.in_waiting)
          data_str = data.decode()
          data_hex = self.transform_to_hex(data)
          self.displayPanel2.write_to_display_OUT_uni(data_str)
          self.displayPanel2.write_to_display_OUT_hex(data_hex)
          if self.term1.is_open:
            try:
              self.term1.write(data)
            except:
              self.configPanel1.write_errors(-3, ["1"])
            self.displayPanel1.write_to_display_IN_uni(data_str)
            self.displayPanel1.write_to_display_IN_hex(data_hex)
      except:
        self.term2.close()

  def send_in_term1(self, string):
    if string != "":
      data = string.encode()
      data_hex = self.transform_to_hex(data)
      self.displayPanel1.write_to_display_IN_uni(string)
      self.displayPanel1.write_to_display_IN_hex(data_hex)
      try:
        self.term1.write(data)
      except:
        self.configPanel1.write_errors(-3, ["1"])

  def send_in_term2(self, string):
    if string != "":
      data = string.encode()
      data_hex = self.transform_to_hex(data)
      self.displayPanel2.write_to_display_IN_uni(string)
      self.displayPanel2.write_to_display_IN_hex(data_hex)
      try:
        self.term2.write(data)
      except:
        self.configPanel2.write_errors(-3, ["2"])

  def process_config_actions(self):
    action1 = self.configPanel1.event_MOUSEBUTTONDOWN_LEFT(pygame.mouse.get_pos())
    action2 = self.configPanel2.event_MOUSEBUTTONDOWN_LEFT(pygame.mouse.get_pos())

    if action1 != None:
      if action1 == -2: # open
        config = self.configPanel1.get_config()
        self.open_term1(config)
      elif action1 == -1: # close
        self.close_term1()
      elif action1 == -3: # reset file settings
        self.displayPanel1.reset_file_settings()
      elif action1[0] == 0: # insertar la configuración de archivos
        self.displayPanel1.set_file_settings(action1[1])
      elif self.term1.is_open:
        self.send_in_term1(action1[1])

    if action2 != None:
      if action2 == -2: #open
        config = self.configPanel2.get_config()
        self.open_term2(config)
      elif action2 == -1: #close
        self.close_term2()
      elif action2 == -3:
        self.displayPanel2.reset_file_settings()
      elif action2[0] == 0:
        self.displayPanel2.set_file_settings(action2[1])
      elif self.term2.is_open:
        self.send_in_term2(action2[1])

  def run(self):
    """
    Funcion con el main loop de la ventana
    """
    run = True
    while run:
      self.clock.tick(80)
      self.read_term1()
      self.read_term2()

      for event in pygame.event.get():  # iterar sobre los eventos ocurridos
        if event.type == pygame.QUIT:
          run = False
        # elif event == poner el tipo de evento, buscar en la documentacion de pygame
        elif event.type == pygame.KEYDOWN:
          self.configPanel1.event_KEYDOWN(event.key)
          self.configPanel2.event_KEYDOWN(event.key)
        elif event.type == pygame.KEYUP:
          self.configPanel1.event_KEYUP()
          self.configPanel2.event_KEYUP()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:
            self.process_config_actions()
            self.displayPanel1.event_MOUSEBUTTONDOWN_LEFT(pygame.mouse.get_pos())
            self.displayPanel2.event_MOUSEBUTTONDOWN_LEFT(pygame.mouse.get_pos())

          elif event.button == 4 or event.button == 5:
            self.configPanel1.event_MOUSEBUTTONDOWN_ROLLER(event.button,pygame.mouse.get_pos())
            self.configPanel2.event_MOUSEBUTTONDOWN_ROLLER(event.button,pygame.mouse.get_pos())
            self.displayPanel1.event_MOUSEBUTTONDOWN_ROLLER(event.button,pygame.mouse.get_pos())
            self.displayPanel2.event_MOUSEBUTTONDOWN_ROLLER(event.button,pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION:
          self.configPanel1.event_MOUSEMOTION(pygame.mouse.get_pos())
          self.configPanel2.event_MOUSEMOTION(pygame.mouse.get_pos())
          self.displayPanel1.event_MOUSEMOTION(pygame.mouse.get_pos())
          self.displayPanel2.event_MOUSEMOTION(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            self.displayPanel1.event_MOUSEBUTTONUP_LEFT()
            self.displayPanel2.event_MOUSEBUTTONUP_LEFT()
            self.configPanel1.event_MOUSEBUTTONUP_LEFT()
            self.configPanel2.event_MOUSEBUTTONUP_LEFT()
            
      self.configPanel1.frame_process()
      self.configPanel2.frame_process()
      self.paint()

  def get_sizes(self):
    """
    obtine las medidas del ancho y largo de la pantalla del usuario
    """
    
    monitor_x = self.info.current_w
    monitor_y = self.info.current_h
    monitor_x = round(monitor_x * .9)
    monitor_y = round(monitor_y * .9)

    font_size = round(monitor_y * 0.02057)

    return (monitor_x, monitor_y, font_size)

  def paint(self):
    """
    Mandar a llamar las funciones paint de los componentes probados
    Mandar como argumento a self.background
    """
    # Aqui mandar a llamar la funcion paint de los componentes probados

    self.configPanel1.paint(self.background)
    self.configPanel2.paint(self.background)
    self.displayPanel1.paint(self.background)
    self.displayPanel2.paint(self.background)

    #####
    self.screen.blit(self.background, (0,0))
    pygame.display.flip()
    self.background.fill((0,0,0))

if __name__ == "__main__":
  Window().run()