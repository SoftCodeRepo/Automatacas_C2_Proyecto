import pygame
import re
from config import *
from input_box import InputBox
from utils import generar_expresion_regular

class RetoContinuar:
    def __init__(self):
        self.activo = False
        self.patron, self.descripcion, self.ejemplos_positivos, self.ejemplos_negativos = generar_expresion_regular()
        self.input_box = InputBox(ANCHO // 2 - 100, ALTO // 2 + 60, 200, 40)
        self.resultado = None
        self.tiempo_resultado = 0
        self.tiempo_max_resultado = 180  # 3 segundos a 60 FPS
    
    def reiniciar(self):
        self.activo = True
        self.patron, self.descripcion, self.ejemplos_positivos, self.ejemplos_negativos = generar_expresion_regular()
        self.input_box = InputBox(ANCHO // 2 - 100, ALTO // 2 + 60, 200, 40)
        self.resultado = None
        self.tiempo_resultado = 0
    
    def verificar_respuesta(self, respuesta):
        try:
            patron_re = re.compile(self.patron)
            if patron_re.match(respuesta):
                self.resultado = True
                self.tiempo_resultado = 0
                return True
            else:
                self.resultado = False
                self.tiempo_resultado = 0
                return False
        except re.error:
            self.resultado = False
            self.tiempo_resultado = 0
            return False
    
    def manejar_eventos(self, evento):
        if self.activo:
            respuesta = self.input_box.handle_event(evento)
            if respuesta is not None:
                return self.verificar_respuesta(respuesta)
        return None
    
    def actualizar(self):
        if self.activo:
            self.input_box.update()
            if self.resultado is not None:
                self.tiempo_resultado += 1
                if self.tiempo_resultado >= self.tiempo_max_resultado:
                    if self.resultado:
                        self.activo = False
                        return True
                    else:
                        # Reiniciar el campo de entrada si la respuesta fue incorrecta
                        self.input_box.text = ""
                        self.input_box.txt_surface = self.input_box.font.render("", True, NEGRO)
                        self.resultado = None
        return None
    
    def dibujar(self, ventana):
        if self.activo:
            # Fondo semitransparente
            superficie = pygame.Surface((ANCHO, ALTO))
            superficie.fill(NEGRO)
            superficie.set_alpha(128)  # 0 es transparente, 255 es opaco
            ventana.blit(superficie, (0, 0))
            
            # Título del desafío
            fuente_titulo = pygame.font.SysFont(None, 48)
            texto_titulo = fuente_titulo.render("¡DESAFÍO PARA CONTINUAR!", True, BLANCO)
            ventana.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 70))
            
            # Descripción del patrón
            fuente = pygame.font.SysFont(None, 32)
            texto_descripcion = fuente.render(f"Escribe un texto que cumpla: {self.descripcion}", True, BLANCO)
            ventana.blit(texto_descripcion, (ANCHO // 2 - texto_descripcion.get_width() // 2, ALTO // 2 - 90))
            
            # Ejemplos
            fuente_ejemplos = pygame.font.SysFont(None, 24)
            texto_ejemplos_titulo = fuente_ejemplos.render("Ejemplos que funcionan:", True, VERDE)
            ventana.blit(texto_ejemplos_titulo, (ANCHO // 2 - texto_ejemplos_titulo.get_width() // 2, ALTO // 2 - 50))
            
            for i, ejemplo in enumerate(self.ejemplos_positivos):
                texto_ejemplo = fuente_ejemplos.render(f'"{ejemplo}"', True, VERDE)
                ventana.blit(texto_ejemplo, (ANCHO // 2 - texto_ejemplo.get_width() // 2, ALTO // 2 - 25 + i * 25))
            
            texto_ejemplos_no_titulo = fuente_ejemplos.render("Ejemplos que NO funcionan:", True, ROJO)
            ventana.blit(texto_ejemplos_no_titulo, (ANCHO // 2 - texto_ejemplos_no_titulo.get_width() // 2, ALTO // 2 + 10))
            
            for i, ejemplo in enumerate(self.ejemplos_negativos):
                texto_ejemplo = fuente_ejemplos.render(f'"{ejemplo}"', True, ROJO)
                ventana.blit(texto_ejemplo, (ANCHO // 2 - texto_ejemplo.get_width() // 2, ALTO // 2 + 35 + i * 25))
            
            # Campo de entrada
            self.input_box.draw(ventana)
            
            # Mostrar resultado si hay
            if self.resultado is not None:
                if self.resultado:
                    color_resultado = VERDE
                    texto_resultado = "¡CORRECTO! Continúa jugando..."
                else:
                    color_resultado = ROJO
                    texto_resultado = "¡INCORRECTO! Inténtalo de nuevo."
                
                texto_render = fuente.render(texto_resultado, True, color_resultado)
                ventana.blit(texto_render, (ANCHO // 2 - texto_render.get_width() // 2, ALTO // 2 + 120))