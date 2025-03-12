import pygame
import random
from config import *
from utils import cargar_imagen

class Cactus:
    def __init__(self, x):
        self.imagenes = [
            cargar_imagen("./images/cactus1.png", (30, 70)),
            cargar_imagen("./images/cactus2.png", (40, 90)),
            cargar_imagen("./images/cactus3.png", (35, 80))
        ]
        self.imagen = random.choice(self.imagenes)
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = ALTO - self.rect.height - 10
    
    def actualizar(self, velocidad):
        self.rect.x -= velocidad
    
    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)