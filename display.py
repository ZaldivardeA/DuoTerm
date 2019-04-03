import pygame
import specialChars

class SideBand:
  def __init__(self, posx, posy, sizex, sizey, native_posy, native_sizey, color=(200,200,200)):
    self.posx = posx
    self.posy = posy
    self.sizex = sizex
    self.sizey = sizey
    self.color = color
    self.active = False
    self.native_sizey = native_sizey
    self.native_posy = native_posy
    self.click_offset = 0

  def set_sizey(self, items_in_view, total_items):
    if total_items <= items_in_view:
      self.sizey = self.native_sizey
    else:
      self.sizey = int(self.native_sizey * items_in_view / total_items)

  def set_posy(self, total_items, offset):
    if not self.active and total_items > 0:
      self.posy = int(self.native_sizey * offset/total_items) + self.native_posy
    else:
      self.posy = self.native_posy

  def check_inside(self, pos):
    x,y = pos
    return x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey

  def get_offset(self, total_items):
    return int((self.posy - self.native_posy)/self.native_sizey * total_items)

  def event_MOUSEBUTTONDOWN_LEFT(self, pos):
    if self.check_inside(pos):
      x,y = pos
      del x
      self.click_offset = y - self.posy
      self.active = True

  def event_MOUSEMOTION(self, pos):
    if self.active:
      x,y = pos
      y = y - self.click_offset
      del x
      if y >= self.native_posy - 1 and y <= self.native_posy + self.native_sizey - self.sizey + 1:
        self.posy = y 
      return True
    return False

  def event_MOUSEBUTTONUP_LEFT(self):
    self.active = False
    self.click_offset = 0

  def paint(self, screen):
    pygame.draw.rect(screen, self.color, (self.posx, self.posy, self.sizex, self.sizey))

class Display:
  def __init__(self, posx, posy, sizex, sizey, title="Untitle", out_color=(50,50,255), in_color=(255,50,50), font_size=20, back_color=(30,30,30), spacing=0, padding=5, end_line_setting="\n", side_band_sizex=10):

    self.posx = posx
    self.posy = posy
    self.sizex = sizex
    self.sizey = sizey
    self.title = title
    self.out_color = out_color
    self.in_color = in_color
    self.font = pygame.font.SysFont("mono",font_size,False)
    fx,fy = self.font.size(" ")
    self.spacing = spacing
    self.padding = padding
    self.side_band = SideBand(self.posx + self.sizex - side_band_sizex, self.posy, side_band_sizex, self.sizey, self.posy, self.sizey)
    self.num_lines_text = (self.sizey - 2*self.padding)//(self.spacing + fy)
    self.num_char_line = (self.sizex - 2*self.padding - self.side_band.sizex)//(fx)
    self.offset = 0
    self.offset_hex = 0
    self.content_unicode = []
    self.content_hex = []
    self.length_uni = 0
    self.length_hex = 0
    self.display_uni = True
    self.back_color = back_color
    self.auto_scroll_enable = True
    self.end_line_setting = end_line_setting
    if self.end_line_setting == "\n":
      self.end_line_opposite = "\r"
    else:
      self.end_line_opposite = "\n"

  def change_font_size(self, new_font_size):
    self.delete_contents()
    self.font = pygame.font.SysFont("mono", new_font_size, False)
    fx,fy = self.font.size(" ")
    self.num_lines_text = (self.sizey - 2*self.padding)//(self.spacing + fy)
    self.num_char_line = (self.sizex - 2*self.padding - self.side_band.sizex)//(fx)

  def check_inside(self,pos):
    x,y = pos
    return x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey

  def set_display_mode(self, unicode_display):
    self.display_uni = unicode_display
    if self.display_uni:
      self.side_band.set_sizey(self.num_lines_text, self.length_uni)
      self.side_band.set_posy(self.length_uni, self.offset)
    else:
      self.side_band.set_sizey(self.num_lines_text, self.length_hex)
      self.side_band.set_posy(self.length_hex, self.offset_hex)

  def set_end_line_setting(self, char):
    if char == "\n":
      self.end_line_setting = "\n"
      self.end_line_opposite = "\r"
    else:
      self.end_line_setting = "\r"
      self.end_line_opposite = "\n"

  def auto_scroll(self):
    if self.auto_scroll_enable:
      if self.length_uni > self.num_lines_text:
        self.offset = self.length_uni - self.num_lines_text
        if self.display_uni:
          self.side_band.set_posy(self.length_uni, self.offset)
      if self.length_hex > self.num_lines_text:
        self.offset_hex = self.length_hex - self.num_lines_text
        if not self.display_uni:
          self.side_band.set_posy(self.length_hex, self.offset_hex)

  def set_auto_scroll(self, scroll):
    self.auto_scroll_enable = scroll

# items_in_view, total_items
  def delete_contents(self):
    self.content_unicode = []
    self.content_hex = []
    self.length_uni = 0
    self.length_hex = 0
    self.offset = 0
    self.offset_hex = 0
    self.side_band.set_sizey(self.num_lines_text, self.length_uni)
    self.side_band.set_posy(self.length_uni, self.offset)

  def event_MOUSEBUTTONDOWN_LEFT(self, pos):
    self.side_band.event_MOUSEBUTTONDOWN_LEFT(pos)

  def event_MOUSEBUTTONUP_LEFT(self):
    self.side_band.event_MOUSEBUTTONUP_LEFT()

  def event_MOUSEMOTION(self, pos):
    if self.side_band.event_MOUSEMOTION(pos):
      if self.display_uni:
        self.offset = self.side_band.get_offset(self.length_uni)
      else:
        self.offset_hex = self.side_band.get_offset(self.length_hex)

  def event_MOUSEBUTTONDOWN_ROLLER(self, button, pos):
    if self.check_inside(pos):
      if self.display_uni:
        if button == 5:
          if self.offset < self.length_uni - self.num_lines_text:
            self.offset += 1
        elif button == 4:
          if self.offset > 0:
            self.offset -= 1
        self.side_band.set_posy(self.length_uni, self.offset)
      else:
        if button == 5:
          if self.offset_hex < self.length_hex - self.num_lines_text:
            self.offset_hex += 1
        elif button == 4:
          if self.offset_hex > 0:
            self.offset_hex -= 1
        self.side_band.set_posy(self.length_hex, self.offset_hex)

  def change_special_chars(self, string):
    ans = ""
    for letter in string:
      if letter in specialChars.special_chars:
        ans += specialChars.special_chars[letter]
      else:
        ans += letter
    return ans

  def write_to_display_uni(self, data):

    data[1] = self.change_special_chars(data[1])
    self.write_data_uni(data)
    self.auto_scroll()

  def write_to_display_hex(self, data):

    self.write_data_hex(data)
    self.auto_scroll()

  def divide_string_add_items(self, string, in_out):
    added_length = 0
    aux = []
    while len(string) >= self.num_char_line:
      str_to_append = string[:self.num_char_line]
      aux.append([in_out, "DONE", str_to_append])
      string = string[self.num_char_line:]
      added_length += 1
    return (aux, string, added_length)

  def get_formated_list(self, data_list, char_to_add, in_out):
    len_list = len(data_list)
    count = 1   # variable para no agregarle el caracter a la última string
    added_length = 0
    out = []
    for string in data_list:
      if count < len_list:
        string += char_to_add
      aux, string, added_length_aux = self.divide_string_add_items(string, in_out)
      added_length += added_length_aux
      count += 1
      out.extend(aux)
      out.append([in_out, "DONE", string])
      added_length += 1
    out[-1][1] = "NOTDONE"
    return (out, added_length)

  def write_data_hex(self, data):
    change_lines = False
    if self.length_hex > 0:
      change_lines = self.content_hex[self.length_hex-1][0] != data[0] or self.content_hex[self.length_hex-1][1] == "DONE"
    if self.length_hex == 0 or change_lines:
      if change_lines and len(self.content_hex[self.length_hex-1][2]) == 0:
        self.content_hex.pop(-1)
        self.length_hex -= 1
      if hex(ord(self.end_line_setting)) in data[1]:
        data_list = data[1].split(hex(ord(self.end_line_setting))+" ") # agregar el espacio para que lo elimine de los enter
        char = hex(ord(self.end_line_setting))
      else:
        data_list = [data[1]]
        char = ""
    else:
      temp_string = self.content_hex[self.length_hex-1][2] + data[1]
      self.content_hex.pop(-1)
      self.length_hex -= 1
      if hex(ord(self.end_line_setting)) in data[1]:
        char = hex(ord(self.end_line_setting))
        data_list = temp_string.split(hex(ord(self.end_line_setting))+" ")
      else:
        char = ""
        data_list = [temp_string]
    aux, added_length = self.get_formated_list(data_list, char, data[0])
    self.length_hex += added_length
    self.content_hex.extend(aux)
      
    if not self.display_uni:
      self.side_band.set_sizey(self.num_lines_text, self.length_hex)

  def write_data_uni(self, data):
    change_lines = False
    if self.length_uni > 0:
      change_lines = self.content_unicode[self.length_uni-1][0] != data[0] or self.content_unicode[self.length_uni-1][1] == "DONE"
    if self.length_uni == 0 or change_lines:
      if change_lines and len(self.content_unicode[self.length_uni-1][2]) == 0:
        self.content_unicode.pop(-1)
        self.length_uni -= 1
      if specialChars.special_chars[self.end_line_setting] in data[1]:
        data_list = data[1].split(specialChars.special_chars[self.end_line_setting])
        char = specialChars.special_chars[self.end_line_setting]
      else:
        data_list = [data[1]]
        char = ""
    else:
      temp_string = self.content_unicode[self.length_uni-1][2] + data[1]
      self.content_unicode.pop(-1)
      self.length_uni -= 1
      if specialChars.special_chars[self.end_line_setting] in data[1]:
        char = specialChars.special_chars[self.end_line_setting]
        data_list = temp_string.split(specialChars.special_chars[self.end_line_setting])
      else:
        char = ""
        data_list = [temp_string]
    aux, added_length = self.get_formated_list(data_list, char, data[0])
    self.length_uni += added_length
    self.content_unicode.extend(aux)

    if self.display_uni:
      self.side_band.set_sizey(self.num_lines_text, self.length_uni)

  def paint(self, screen):

    pygame.draw.rect(screen, self.back_color, (self.posx, self.posy, self.sizex, self.sizey))
    self.side_band.paint(screen)

    fx, fy = self.font.size(" ")
    if self.display_uni:
      end_pos = int(self.offset + self.num_lines_text)
    else:
      end_pos = int(self.offset_hex + self.num_lines_text)

    if self.display_uni:
      if end_pos > self.length_uni:
        end_pos = self.length_uni

      for index in range(self.offset, end_pos):
        line = self.content_unicode[index]
        if line[0] == "IN":
          color = self.in_color
        else:
          color = self.out_color
        surface = self.font.render(line[2], True, color)
        screen.blit(surface, (self.posx + self.padding, self.posy+self.padding+(self.spacing+fy)*(index - self.offset)))
    else:
      if end_pos > self.length_hex:
        end_pos = self.length_hex

      for index in range(self.offset_hex, end_pos):
        line = self.content_hex[index]
        if line[0] == "IN":
          color = self.in_color
        else:
          color = self.out_color
        surface = self.font.render(line[2], True, color)
        screen.blit(surface, (self.posx + self.padding, self.posy+self.padding+(self.spacing+fy)*(index - self.offset_hex)))