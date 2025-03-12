import pygame
import os
import json
import random
from config import *

def cargar_imagen(nombre, escala=None):
    ruta = nombre if os.path.exists(nombre) else None
    
    if ruta:
        try:
            imagen = pygame.image.load(ruta).convert_alpha()
            if escala:
                imagen = pygame.transform.scale(imagen, escala)
            return imagen
        except pygame.error:
            print(f"No se pudo cargar la imagen: {nombre}")
    
    if "dino" in nombre.lower():
        superficie = pygame.Surface((40, 80), pygame.SRCALPHA)
        pygame.draw.rect(superficie, NEGRO, (0, 0, 40, 80))
        return superficie
    elif "cactus" in nombre.lower():
        superficie = pygame.Surface((30, 70), pygame.SRCALPHA)
        pygame.draw.rect(superficie, NEGRO, (0, 0, 30, 70))
        return superficie
    else:
        superficie = pygame.Surface((60, 30), pygame.SRCALPHA)
        pygame.draw.rect(superficie, (200, 200, 200), (0, 0, 60, 30))
        return superficie

def guardar_puntuacion_maxima(puntuacion):
    datos = {"puntuacion_maxima": puntuacion}
    try:
        with open(ARCHIVO_PUNTUACION, 'w') as archivo:
            json.dump(datos, archivo)
    except Exception as e:
        print(f"Error al guardar la puntuación: {e}")

def cargar_puntuacion_maxima():
    try:
        if os.path.exists(ARCHIVO_PUNTUACION):
            with open(ARCHIVO_PUNTUACION, 'r') as archivo:
                datos = json.load(archivo)
                return datos.get("puntuacion_maxima", 0)
    except Exception as e:
        print(f"Error al cargar la puntuación: {e}")
    return 0

def generar_expresion_regular():
    patrones = [
        (r"^a.*", "Texto que comienza con 'a'"),
        (r".*a$", "Texto que termina con 'a'"),
        (r"^[0-9]+$", "Solo números"),
        (r"^[A-Za-z]+$", "Solo letras"),
        (r"^[A-Z].*", "Texto que comienza con mayúscula"),
        (r".*\d.*", "Texto que contiene al menos un número"),
        (r"^[aeiouAEIOU].*", "Texto que comienza con vocal"),
        (r"^[a-z]{3}$", "Exactamente 3 letras minúsculas"),
        (r"^\d{2}-\d{2}$", "Formato: dos números, guion, dos números (ej: 12-34)"),
        (r"^(rojo|verde|azul)$", "Solo una de estas palabras: rojo, verde o azul")
    ]
    
    patron, descripcion = random.choice(patrones)
    
    ejemplos_positivos = []
    ejemplos_negativos = []
    
    if patron == r"^a.*":
        ejemplos_positivos = ["abc", "avion", "agua"]
        ejemplos_negativos = ["casa", "bote", "123"]
    elif patron == r".*a$":
        ejemplos_positivos = ["casa", "mesa", "tela"]
        ejemplos_negativos = ["cas", "meso", "tele"]
    elif patron == r"^[0-9]+$":
        ejemplos_positivos = ["123", "456", "789"]
        ejemplos_negativos = ["a123", "45b6", "7.89"]
    elif patron == r"^[A-Za-z]+$":
        ejemplos_positivos = ["abc", "XYZ", "AbCd"]
        ejemplos_negativos = ["abc1", "2xyz", "a-b"]
    elif patron == r"^[A-Z].*":
        ejemplos_positivos = ["Abc", "Xyz", "Hola"]
        ejemplos_negativos = ["abc", "xyz", "123"]
    elif patron == r".*\d.*":
        ejemplos_positivos = ["a1b", "123", "abc5"]
        ejemplos_negativos = ["abc", "xyz", ""]
    elif patron == r"^[aeiouAEIOU].*":
        ejemplos_positivos = ["agua", "eco", "isla"]
        ejemplos_negativos = ["casa", "pera", "123"]
    elif patron == r"^[a-z]{3}$":
        ejemplos_positivos = ["abc", "xyz", "hola"[:3]]
        ejemplos_negativos = ["abcd", "12", "A"]
    elif patron == r"^\d{2}-\d{2}$":
        ejemplos_positivos = ["12-34", "56-78", "90-12"]
        ejemplos_negativos = ["1-2", "123-45", "ab-cd"]
    elif patron == r"^(rojo|verde|azul)$":
        ejemplos_positivos = ["rojo", "verde", "azul"]
        ejemplos_negativos = ["amarillo", "rojoverde", "r"]
    
    return patron, descripcion, random.sample(ejemplos_positivos, min(2, len(ejemplos_positivos))), random.sample(ejemplos_negativos, min(2, len(ejemplos_negativos)))