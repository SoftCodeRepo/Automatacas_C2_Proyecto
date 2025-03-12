import pygame
import sys
from config import *
from game import Juego

# Inicializar pygame
pygame.init()

def main():
    juego = Juego()
    
    # Bucle principal
    while True:
        juego.manejar_eventos()
        juego.actualizar()
        juego.dibujar()
        
        pygame.display.update()
        juego.reloj.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()