import pygame
from config import *

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = NEGRO
        self.text = text
        self.font = pygame.font.SysFont(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, self.color)
        return None

    def update(self):
        # Mantener el rectángulo creciendo con el texto
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width
        
        # Parpadeo del cursor
        self.cursor_timer += 1
        if self.cursor_timer > 30:  # Cambiar cada medio segundo aprox
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, screen):
        # Dibujar el fondo del rectángulo
        pygame.draw.rect(screen, BLANCO, self.rect, 0)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
        # Dibujar el texto
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        
        # Dibujar el cursor si está activo
        if self.active and self.cursor_visible:
            cursor_pos = self.rect.x + 5 + self.txt_surface.get_width()
            cursor_rect = pygame.Rect(cursor_pos, self.rect.y + 5, 2, self.font.get_height())
            pygame.draw.rect(screen, self.color, cursor_rect)