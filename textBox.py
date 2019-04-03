import pygame
import time
import keyboard_dic

class TextBox:
    """
    Clase que implementa un cuadro de texto para que el usuario pueda ingresar informacion
    """

    def __init__(self, posx, posy, sizex, sizey, color=(255,255,255), text_color=(0,0,0), font_size=20):
        self.posx = posx
        self.posy = posy
        self.sizey = sizey
        self.sizex = sizex
        self.color = color
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
        self.text_color = text_color
        self.font = pygame.font.SysFont('times new roman', font_size, bold=False)
        self.focus = False
        self.blinking = time.time()
        self.shift_pressed = False
        self.caps_active = False
        self.cursor_pos = 0
        self.repeat_del = 0
        self.del_press = False

    def check_click(self,pos):
        x,y = pos
        self.focus = x >= self.posx and x <= self.posx + self.sizex and y >= self.posy and y <= self.posy + self.sizey

    def check_caps(self):
        bit_mask = pygame.key.get_mods()
        caps_state = (bit_mask>>13)&1
        shift_state = (bit_mask>>1)&1 | bit_mask&1
        self.caps_active = caps_state != shift_state

    def get_text(self):
        return self.text

    def reset_blink(self):
        self.blinking = time.time()
        self.paint_blink = True

    def event_KEYUP(self):
        self.del_press = False

    def process_backspace(self):
        if self.del_press:
            if  time.time() - self.repeat_del > 0.1:
                if self.cursor_pos > 0:
                    self.reset_blink()
                    self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    self.repeat_del = time.time()

    def write_in_box(self, key):
        """
        Función que escribe del teclado a la caja de texto
        """
        if self.focus:
            self.check_caps()
            self.reset_blink()
            if key in keyboard_dic.dic_keyboard:
                if self.caps_active:
                    char = keyboard_dic.dic_keyboard_shift[key]
                else:
                    char = keyboard_dic.dic_keyboard[key]

                fx,fy = self.font.size(self.text + char)
                del(fy)
                if char == '\b':
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                        self.del_press = True
                        self.repeat_del = time.time() + 0.3
                elif  fx < self.sizex:
                    self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
            elif key == 127:
                self.text = ""
                self.cursor_pos = 0
            else:
                if key == 276: #flecha izquierda
                    if self.cursor_pos > 0:
                        self.cursor_pos -= 1
                elif key == 275: #flecha derecha
                    if self.cursor_pos < len(self.text):
                        self.cursor_pos += 1

    def set_focus_false(self):
        self.focus = False
        self.del_press = False

    def paint(self,screen):

        pygame.draw.rect(screen, self.color, (self.posx, self.posy, self.sizex, self.sizey))
        fx, fy = self.font.size(self.text)
        surface = self.font.render(self.text, True, self.text_color)
        screen.blit(surface, (self.posx + (self.sizex - fx)//2, self.posy + (self.sizey - fy)//2))
        if self.focus:
            if time.time() - self.blinking > 0.5:
                self.blinking = time.time()
                self.paint_blink = not self.paint_blink
        else:
            self.paint_blink = False
        if self.paint_blink:
            if self.cursor_pos != 0:
                fxc, fyc = self.font.size(self.text[:self.cursor_pos])
                line_posx = self.posx + (self.sizex - fx)//2 + fxc
            else:
                line_posx = self.posx + (self.sizex - fx)//2
            pygame.draw.line(screen, self.blink_color, (line_posx, self.posy+(self.sizey-fy)//2), (line_posx, self.posy+(self.sizey-fy)//2 + fy), 2)