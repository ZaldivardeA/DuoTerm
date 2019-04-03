import pygame
import time
import keyboard_dic
from boton import Boton

class TextBoxSend:
    """
    Clase que implementa un cuadro de texto para que el usuario pueda ingresar informacion
    """

    def __init__(self, posx, posy, sizex, sizey, title, color=(255,255,255), text_color=(0,0,0), font_size=20):
        self.posx = posx
        self.posy = posy
        self.sizey = sizey
        self.sizex = sizex
        self.color = color
        self.title = title
        self.spacing = 2
        r,g,b = self.color
        if r >= 128:
            r = 0
        else:
            r = 255
        if g >= 128:
            g = 0
        else:
            g = 255
        if b >= 128:
            b = 0
        else:
            b = 255
        self.blink_color = (r,g,b)
        self.paint_blink = False
        self.text = ""
        self.text_to_paint = ""
        self.text_color = text_color
        self.font = pygame.font.SysFont('times new roman', font_size, bold=False)
        self.title_font = pygame.font.SysFont("times new roman", font_size, True)
        self.font_size = font_size
        self.text_sx, fy = self.title_font.size(self.title)
        self.text_sx += self.spacing
        self.focus = False
        self.blinking = time.time()
        self.shift_pressed = False
        self.caps_active = False
        self.cursor_pos = 0
        self.send_normal, self.send_cr, self.send_ln = self.generate_send_buttons()
        self.string_offset = 0
        self.text_fits = True
        self.repeat_del = 0
        self.del_press = False

    def generate_send_buttons(self):
        posx = self.posx + self.sizex + self.spacing + self.text_sx
        posy = self.posy
        sizex = round(self.sizex*0.257731)
        sizey = self.sizey
        title = "Send"
        normal = Boton(posx, posy, sizex, sizey, title, font_size=self.font_size)
        posx += sizex + self.spacing
        title = "\\r"
        cr = Boton(posx, posy, sizex, sizey, title, font_size=self.font_size)
        posx += sizex + self.spacing
        title = "\\n"
        ln = Boton(posx, posy, sizex, sizey, title, font_size=self.font_size)
        return (normal, cr, ln)

    def check_click(self,pos):
        x,y = pos
        bx = x >= self.posx + self.text_sx and x <= self.posx + self.text_sx + self.sizex
        by = y >= self.posy and y <= self.posy + self.sizey
        self.focus = bx and by

    def reset_blink(self):
        self.blinking = time.time()
        self.paint_blink = True

    def check_caps(self):
        bit_mask = pygame.key.get_mods()
        caps_state = (bit_mask>>13)&1
        shift_state = (bit_mask>>1)&1 | bit_mask&1
        self.caps_active = caps_state != shift_state

    def get_text(self):
        return self.text

    def event_KEYUP(self):
        self.del_press = False

    def process_backspace(self):
        if self.del_press:
            if  time.time() - self.repeat_del > 0.1:
                self.process_back_space()
                self.repeat_del = time.time()
    
    def event_MOUSEBUTTONDOWN(self, pos):
        self.check_click(pos)
        if self.send_normal.was_click(pos):
            return self.text
        elif self.send_cr.was_click(pos):
            return self.text + "\r"
        elif self.send_ln.was_click(pos):
            return self.text + "\n"
        else:
            return None

    def event_MOUSEBUTTONUP(self):
        self.send_normal.released()
        self.send_cr.released()
        self.send_ln.released()

    def event_MOUSEMOTION(self, pos):
        self.send_normal.was_hover(pos)
        self.send_cr.was_hover(pos)
        self.send_ln.was_hover(pos)

    def check_if_text_fits(self):
        fx, fy = self.font.size(self.text)
        self.text_fits = fx < self.sizex
        if self.text_fits:
            self.string_offset = 0

    def shift_text_display(self):
        fxc, fxy = self.font.size(self.text[:self.cursor_pos])
        if fxc > self.sizex:
            self.string_offset = fxc - self.sizex + 2
        else:
            self.string_offset = 1

    def calc_string_offset(self):
        line_posx = self.calculate_cursor_pos()
        posx = self.posx + self.text_sx
        if line_posx < posx + 5:
            #line_posx = self.cursor_pos_nooffset()
            #self.string_offset = line_posx - self.posx
            self.shift_text_display()
        elif line_posx > posx + self.sizex - 2:
            line_posx = self.cursor_pos_nooffset()
            self.string_offset = line_posx - posx - self.sizex + 2

    def set_offset_to_last(self):
        if not self.text_fits:
            fx, fy = self.font.size(self.text)
            self.string_offset = fx - self.sizex + 2

    def process_left_arrow(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

        self.calc_string_offset()

    def process_right_arrow(self):
        if self.cursor_pos < len(self.text):
            self.cursor_pos += 1

        self.calc_string_offset()

    def check_last_char_in(self):
        fx, fy = self.font.size(self.text)
        return fx - self.string_offset < self.sizex

    def process_back_space(self):
        if self.cursor_pos == len(self.text):
            self.reset_blink()
            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
            self.repeat_del = time.time() + 0.3
            self.del_press = True
            self.check_if_text_fits()
            self.set_offset_to_last()
        elif self.cursor_pos > 0:
            self.reset_blink()
            self.repeat_del = time.time() + 0.3
            self.del_press = True
            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
            self.check_if_text_fits()
            self.calc_string_offset()
            if self.check_last_char_in():
                self.set_offset_to_last()

    def add_char(self, char):
        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
        self.cursor_pos += 1
        self.check_if_text_fits()
        self.calc_string_offset()

    def delete_contents(self):
        self.text = ""
        self.string_offset = 0
        self.cursor_pos = 0
        self.text_fits = True

    def write_in_box(self, key):
        """
        Función que escribe del teclado a la caja de texto
        """
        if self.focus:
            self.reset_blink()
            self.check_caps()
            if key in keyboard_dic.dic_keyboard:
                if self.caps_active:
                    char = keyboard_dic.dic_keyboard_shift[key]
                else:
                    char = keyboard_dic.dic_keyboard[key]

                fx,fy = self.font.size(self.text + char)
                del(fy)
                if char == '\b':
                    self.process_back_space()
                #elif fx < self.sizex:
                else:
                    self.add_char(char)
            elif key == 127:
                self.delete_contents()
            else:
                if key == 276: #flecha izquierda
                    self.process_left_arrow()
                elif key == 275: #flecha derecha
                    self.process_right_arrow()
    

    def set_focus_false(self):
        self.focus = False

    def cursor_pos_nooffset(self):
        fx, fy = self.font.size(self.text)
        posx = self.posx + self.text_sx
        if self.text_fits:
            if self.cursor_pos != 0:
                fxc, fyc = self.font.size(self.text[:self.cursor_pos])
                line_posx = posx + (self.sizex - fx)//2 + fxc
            else:
                line_posx = posx + (self.sizex - fx)//2
        else:
            if self.cursor_pos != 0:
                fxc, fyc = self.font.size(self.text[:self.cursor_pos])
                line_posx = posx + fxc
            else:
                line_posx = posx
        return line_posx

    def calculate_cursor_pos(self):
        fx, fy = self.font.size(self.text)
        posx = self.posx + self.text_sx
        if self.text_fits:
            if self.cursor_pos != 0:
                fxc, fyc = self.font.size(self.text[:self.cursor_pos])
                line_posx = posx + (self.sizex - fx)//2 + fxc
            else:
                line_posx = posx + (self.sizex - fx)//2
        else:
            if self.cursor_pos != 0:
                fxc, fyc = self.font.size(self.text[:self.cursor_pos])
                line_posx = posx - self.string_offset + fxc
            else:
                line_posx = posx - self.string_offset
        return line_posx

    def calculate_text_pos(self):
        fx, fy = self.font.size(self.text)
        if self.text_fits:
            text_posx = (self.sizex - fx)//2 - self.string_offset
            text_posy = (self.sizey - fy)//2
        else:
            text_posx = 0 - self.string_offset
            text_posy = (self.sizey - fy)//2
        
        return (text_posx, text_posy)

    def paint(self,screen):
        box = pygame.Surface((self.sizex, self.sizey)).convert()
        box.fill(self.color)
        fx, fy = self.font.size(self.text)
        text_sur = self.font.render(self.text, True, self.text_color)
        text_posx, text_posy = self.calculate_text_pos()
        box.blit(text_sur, (text_posx, text_posy))
        screen.blit(box, (self.posx + self.text_sx, self.posy))

        if self.focus:
            if time.time() - self.blinking > 0.5:
                self.blinking = time.time()
                self.paint_blink = not self.paint_blink
        else:
            self.paint_blink = False
        if self.paint_blink:
            line_posx = self.calculate_cursor_pos()
            pygame.draw.line(screen, self.blink_color, (line_posx, self.posy+(self.sizey-fy)//2), (line_posx, self.posy+(self.sizey-fy)//2 + fy), 2)
        
        fx, fy = self.font.size(self.title)
        surface = self.title_font.render(self.title, True, self.text_color)
        posy = self.posy + (self.sizey - fy)//2
        screen.blit(surface, (self.posx, posy))
        self.send_normal.paint(screen)
        self.send_cr.paint(screen)
        self.send_ln.paint(screen)