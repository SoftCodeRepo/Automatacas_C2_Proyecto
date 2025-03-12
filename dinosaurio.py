import pygame
from config import *
from utils import cargar_imagen

class Dinosaurio:
    def __init__(self):
        # Intentar cargar imágenes para animación
        self.imagenes = [
            cargar_imagen("./images/perro1.jpg", (40, 80)),
            cargar_imagen("./images/perro2.jpg", (40, 80)),
            cargar_imagen("./images/perro3.jpg", (40, 80))
        ]
        self.indice_imagen = 0
        self.contador_animacion = 0
        
        # Imagen actual
        self.imagen = self.imagenes[0]
        self.rect = self.imagen.get_rect()
        self.rect.x = 50
        self.rect.y = ALTO - self.rect.height - 10
        self.velocidad_y = 0
        self.en_suelo = True
    
    def actualizar(self):
        # Aplicar gravedad
        self.velocidad_y += GRAVEDAD
        self.rect.y += self.velocidad_y
        
        # Verificar si está en el suelo
        if self.rect.y >= ALTO - self.rect.height - 10:
            self.rect.y = ALTO - self.rect.height - 10
            self.velocidad_y = 0
            self.en_suelo = True
        
        # Animación (solo si está en el suelo)
        if self.en_suelo:
            self.contador_animacion += 1
            if self.contador_animacion >= 10:  # Cambiar cada 10 frames
                self.contador_animacion = 0
                self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes)
                self.imagen = self.imagenes[self.indice_imagen]
        else:
            self.imagen =  cargar_imagen("./images/perroSalto.jpg", (40, 80))
    
    def saltar(self):
        if self.en_suelo:
            self.velocidad_y = SALTO
            self.en_suelo = False
    
    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)