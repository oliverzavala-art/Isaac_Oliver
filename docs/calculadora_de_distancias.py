# === Calculadora de Distancias ===
# Autores: Oliver Zavala y Isaac
import json
import os
import sys
import time
from math import atan2, cos, radians, sin, sqrt
from pathlib import Path
import math
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api import obtener_coordenadas
from ciudad import Ciudad
from math import atan2, cos, radians, sin, sqrt
RADIO_TIERRA_KM = 6371.0088


CACHE_DIR = "data"
CACHE_FILE = os.path.join(CACHE_DIR, "coordenadas_cache.json")


def cargar_cache():
    #Este código lee el archivo JSON de caché local si está presente; devuelve un diccionario vacío en caso de error.
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def guardar_cache(cache):
    #este programa crea automáticamente una subcarpeta para almacenar el archivo de caché si no existe
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
#Este codigo Guardar el diccionario de caché en el archivo JSON con formato legible
            json.dump(cache, f, ensure_ascii=False, indent=4)
#Este código maneja errores de entrada/salida al guardar el archivo de caché y muestra un mensaje de error si ocurre un problema.
    except IOError as e:
        print(f"[CACHE ERROR] Could not save file: {e}")



def calcular_distancia(coordenadas_origen, coordenadas_destino):
    #Este código calcula la distancia de gran círculo entre 
    # dos pares de coordenadas (latitud, longitud) utilizando la fórmula de Haversine.
    latitud_origen, longitud_origen = map(math.radians, coordenadas_origen)
    latitud_destino, longitud_destino = map(math.radians, coordenadas_destino)

    diferencia_latitud = latitud_destino - latitud_origen
    diferencia_longitud = longitud_destino - longitud_origen
    a = (
        math.sin(diferencia_latitud / 2) ** 2
        + math.cos(latitud_origen)
        * math.cos(latitud_destino)
        * math.sin(diferencia_longitud / 2) ** 2
    )
    a = min(1.0, max(0.0, a))
    #Este código calcula el ángulo central entre dos puntos en la superficie
    #  de la Tierra utilizando la fórmula de Haversine y devuelve la distancia en kilómetros.
    angulo_central = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return RADIO_TIERRA_KM * angulo_central


def pedir_ciudad(mensaje):
    #Este código solicita al usuario que ingrese el nombre de una ciudad 
    # y asegura que la entrada no esté vacía. Si el usuario no proporciona una ciudad válida, se le pedirá que lo intente nuevamente.
    while True:
        ciudad = input(mensaje).strip()
        if ciudad:
            return ciudad
        print("Por favor, ingresa una ciudad válida.")
#E

def pedir_unidad():
    #Este código solicita al usuario que ingrese la unidad en la que se mostrará la distancia.
    while True:
        unidad = input("Unidad (km/millas): ").strip().lower()
        if unidad in ("km", "millas"):
            return unidad
        print("Por favor, ingresa «km» o «millas».")
 #Constantes de velocidad en km/h para avión y auto
VELOCIDAD_AVION = 800
VELOCIDAD_AUTO = 80

#Este código calcula el tiempo de viaje estimado en horas entre dos ciudades dadas
#  la distancia y la velocidad del medio de transporte.

def calcular_tiempo_viaje(distancia, velocidad):
    ##calcula el tiempo de viaje en horas decimal y lo devuelve como un número decimal.
 return distancia / velocidad

 #Este codigo convierte horas decimales a horas y minutos
 #  y devuelve una cadena con el formato "X horas Y minutos".

 tiempo_avion = calcular_tiempo_viaje(distancia, VELOCIDAD_AVION)
 tiempo_auto = calcular_tiempo_viaje(distancia, VELOCIDAD_AUTO) 

#Este código muestra el tiempo estimado de viaje en horas y minutos para un avión y un auto,
#  utilizando la distancia calculada y las velocidades predefinidas.
def convertir_horas_a_horas_y_minutos(horas):
    horas_enteras = int(horas)
    minutos = int((horas - horas_enteras) * 60)
    return f"{horas_enteras} horas {minutos} minutos"


def mostrar_menu():
    #Este código muestra el menú y calcula distancias entre las ciudades elegidas.
    while True:
        print("\n=== Calculadora de Distancias ===")
        print("1. Calcular distancia")
        print("2. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "2":
            print("Hasta luego.")
            return
        if opcion != "1":
            print("Opción no válida. Elige 1 o 2.")
            continue

        ciudad_origen = pedir_ciudad("Ciudad de origen (incluye país): ")
        ciudad_destino = pedir_ciudad("Ciudad de destino (incluye país): ")
        unidad = pedir_unidad()

        coordenadas_origen = obtener_coordenadas(ciudad_origen)
        if coordenadas_origen is None:
            continue

        time.sleep(1)
        coordenadas_destino = obtener_coordenadas(ciudad_destino)
        if coordenadas_destino is None:
            continue

        origen = Ciudad(ciudad_origen, *coordenadas_origen)
        destino = Ciudad(ciudad_destino, *coordenadas_destino)
        distancia_km = calcular_distancia(
            origen.coordenadas,
            destino.coordenadas,
        )
        if unidad == "millas":
            #Este código convierte la distancia de kilómetros a millas

            distancia = distancia_km / 1.609344
            etiqueta = "millas"
        else:
            distancia = distancia_km
            etiqueta = "km"
#Este código muestra el resultado en kilómetros de la distancia calculada entre las ciudades de origen y destino,
#  junto con la unidad seleccionada por el usuario. 
        print("\n--- Resultado ---")
        print(f"Origen: {origen.nombre}")
        print(
            "Coordenadas de origen (latitud, longitud): "
            f"{origen.latitud:.6f}, {origen.longitud:.6f}"
        )
        print(f"Destino: {destino.nombre}")
        print(
            "Coordenadas de destino (latitud, longitud): "
            f"{destino.latitud:.6f}, {destino.longitud:.6f}"
        )
        print(f"Distancia aproximada en linea recta: {distancia:.2f} {etiqueta}")
#Este código calcula y muestra el tiempo estimado de viaje en horas y minutos para un avión y un auto,
#  utilizando la distancia calculada y las velocidades predefinidas.    
        tiempo_avion = calcular_tiempo_viaje(distancia_km, VELOCIDAD_AVION)
        tiempo_auto = calcular_tiempo_viaje(distancia_km, VELOCIDAD_AUTO)

        print(f"Tiempo estimado en avión: {convertir_horas_a_horas_y_minutos(tiempo_avion)}")
        print(f"Tiempo estimado en auto: {convertir_horas_a_horas_y_minutos(tiempo_auto)}")

if __name__ == "__main__":
    mostrar_menu()  

