import pygame
import sys
import random
from config import *
from utils import cargar_imagen, guardar_puntuacion_maxima, cargar_puntuacion_maxima
from dinosaurio import Dinosaurio
from cactus import Cactus
from nube import Nube
from reto_continuar import RetoContinuar

class Juego:
    def __init__(self):
        # Configuración de la ventana
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Juego del Dinosaurio")
        self.reloj = pygame.time.Clock()
        
        # Elementos del juego
        self.dinosaurio = Dinosaurio()
        self.cactus = []
        self.nubes = []
        self.velocidad = VELOCIDAD_INICIAL
        self.puntuacion = 0
        self.puntuacion_maxima = cargar_puntuacion_maxima()
        self.fuente = pygame.font.SysFont(None, 36)
        self.game_over = False
        self.reto_continuar = RetoContinuar()
        
        # Cargar imagen de fondo y suelo
        self.imagen_suelo = cargar_imagen("suelo.png", (ANCHO, 20))
        if isinstance(self.imagen_suelo, pygame.Surface) and self.imagen_suelo.get_width() < ANCHO:
            # Crear un patrón repetido si la imagen es más pequeña que la pantalla
            nueva_superficie = pygame.Surface((ANCHO, self.imagen_suelo.get_height()))
            for x in range(0, ANCHO, self.imagen_suelo.get_width()):
                nueva_superficie.blit(self.imagen_suelo, (x, 0))
            self.imagen_suelo = nueva_superficie
        
        self.posicion_suelo_x = 0
        
        # Crear cactus iniciales
        self.cactus.append(Cactus(ANCHO + random.randint(100, 300)))
        
        # Crear nubes iniciales
        for i in range(3):
            self.nubes.append(Nube(random.randint(0, ANCHO)))
    
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # Guardar puntuación máxima antes de salir
                if int(self.puntuacion) > self.puntuacion_maxima:
                    guardar_puntuacion_maxima(int(self.puntuacion))
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if not self.game_over and not self.reto_continuar.activo:
                        self.dinosaurio.saltar()
                if evento.key == pygame.K_r and self.game_over and not self.reto_continuar.activo:
                    self.__init__()  # Reiniciar juego
                if evento.key == pygame.K_c and self.game_over and not self.reto_continuar.activo:
                    # Activar el reto para continuar
                    self.reto_continuar.reiniciar()
            
            # Manejar eventos del reto si está activo
            if self.reto_continuar.activo:
                resultado = self.reto_continuar.manejar_eventos(evento)
                if resultado is True:
                    if self.puntuacion >= 100:
                        self.puntuacion -= 100
                    else:
                        self.puntuacion = 0
                    # El jugador ha superado el reto, continuar el juego
                    self.game_over = False
                    # Reiniciar posición del dinosaurio si es necesario
                    self.dinosaurio.rect.y = ALTO - self.dinosaurio.rect.height - 10
                    self.dinosaurio.velocidad_y = 0
                    self.dinosaurio.en_suelo = True
                    # Limpiar cactus cercanos para dar tiempo al jugador
                    self.cactus = [cactus for cactus in self.cactus if cactus.rect.x > 200]
                    if not self.cactus:
                        self.cactus.append(Cactus(ANCHO + random.randint(100, 300)))
    
    def actualizar(self):
        # Actualizar el reto si está activo
        if self.reto_continuar.activo:
            resultado = self.reto_continuar.actualizar()
            if resultado is True:
                self.game_over = False
                # Ya se ha manejado en manejar_eventos()
        
        if not self.game_over and not self.reto_continuar.activo:
            self.dinosaurio.actualizar()
            
            # Actualizar cactus
            for cactus in self.cactus:
                cactus.actualizar(self.velocidad)
            
            # Eliminar cactus fuera de pantalla
            self.cactus = [cactus for cactus in self.cactus if cactus.rect.right > 0]
            
            # Crear nuevos cactus si es necesario
            if len(self.cactus) < 3 and random.random() < 0.02:
                distancia_min = 300 + self.velocidad * 10  # Distancia mínima entre cactus
                if not self.cactus or self.cactus[-1].rect.x < ANCHO - distancia_min:
                    self.cactus.append(Cactus(ANCHO + random.randint(0, 100)))
            
            # Actualizar nubes
            for nube in self.nubes:
                nube.actualizar(self.velocidad)
            
            # Eliminar nubes fuera de pantalla
            self.nubes = [nube for nube in self.nubes if nube.rect.right > 0]
            
            # Crear nuevas nubes si es necesario
            if len(self.nubes) < 5 and random.random() < 0.01:
                self.nubes.append(Nube(ANCHO + random.randint(0, 100)))
            
            # Mover el suelo (efecto parallax)
            self.posicion_suelo_x -= self.velocidad
            if self.posicion_suelo_x <= -ANCHO:
                self.posicion_suelo_x = 0
            
            # Detectar colisiones
            for cactus in self.cactus:
                if self.dinosaurio.rect.colliderect(cactus.rect):
                    self.game_over = True
                    # Actualizar puntuación máxima si es necesario
                    if int(self.puntuacion) > self.puntuacion_maxima:
                        self.puntuacion_maxima = int(self.puntuacion)
                        guardar_puntuacion_maxima(self.puntuacion_maxima)
            
            # Aumentar puntuación y dificultad
            self.puntuacion += 0.1
            if self.puntuacion % 100 < 0.1:
                self.velocidad += 0.5
    
    def dibujar(self):
        self.ventana.fill(BLANCO)
        
        # Dibujar nubes
        for nube in self.nubes:
            nube.dibujar(self.ventana)
        
        # Dibujar suelo con efecto de desplazamiento
        self.ventana.blit(self.imagen_suelo, (self.posicion_suelo_x, ALTO - 20))
        self.ventana.blit(self.imagen_suelo, (self.posicion_suelo_x + ANCHO, ALTO - 20))
        
        # Dibujar dinosaurio
        self.dinosaurio.dibujar(self.ventana)
        
        # Dibujar cactus
        for cactus in self.cactus:
            cactus.dibujar(self.ventana)
        
        # Dibujar puntuaciones
        texto_puntuacion = self.fuente.render(f"Puntuación: {int(self.puntuacion)}", True, NEGRO)
        self.ventana.blit(texto_puntuacion, (10, 10))
        
        texto_max = self.fuente.render(f"Máxima: {self.puntuacion_maxima}", True, NEGRO)
        self.ventana.blit(texto_max, (ANCHO - texto_max.get_width() - 10, 10))
        
        # Dibujar mensaje de game over
        if self.game_over and not self.reto_continuar.activo:
            texto_game_over = self.fuente.render("GAME OVER", True, NEGRO)
            self.ventana.blit(texto_game_over, (ANCHO // 2 - texto_game_over.get_width() // 2, ALTO // 2 - 50))
            
            texto_reiniciar = self.fuente.render("Presiona R para reiniciar", True, NEGRO)
            self.ventana.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, ALTO // 2))
            
            texto_continuar = self.fuente.render("Presiona C para continuar (desafío)", True, NEGRO)
            self.ventana.blit(texto_continuar, (ANCHO // 2 - texto_continuar.get_width() // 2, ALTO // 2 + 40))
        
        # Dibujar la interfaz del reto si está activo
        if self.reto_continuar.activo:
            self.reto_continuar.dibujar(self.ventana)