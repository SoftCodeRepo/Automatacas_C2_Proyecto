import pygame
import random
from config import *
from utils import cargar_imagen

class Nube:
    def __init__(self, x):
        # Cargar imagen de nube
        self.imagen = cargar_imagen("./images/nube.png", (random.randint(60, 120), random.randint(30, 50)))
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = random.randint(50, 150)
    
    def actualizar(self, velocidad):
        self.rect.x -= velocidad // 2  # Las nubes se mueven más lento
    
    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)