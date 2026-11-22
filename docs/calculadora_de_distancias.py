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
from math import atan2, cos, radians, sin, sqrt
RADIO_TIERRA_KM = 6371.0088


CACHE_DIR = "data"
CACHE_FILE = os.path.join(CACHE_DIR, "coordenadas_cache.json")


def cargar_cache():
    """Reads local JSON cache file if present; returns an empty dict on error."""
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
    """Calcula la distancia de gran círculo entre dos pares (latitud, longitud)."""
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


def pedir_unidad():
    #Este código solicita al usuario que ingrese la unidad en la que se mostrará la distancia.
    while True:
        unidad = input("Unidad (km/millas): ").strip().lower()
        if unidad in ("km", "millas"):
            return unidad
        print("Por favor, ingresa «km» o «millas».")

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

        distancia_km = calcular_distancia(coordenadas_origen, coordenadas_destino)
        if unidad == "millas":
            distancia = distancia_km / 1.609344
            etiqueta = "millas"
        else:
            distancia = distancia_km
            etiqueta = "km"

        print("\n--- Resultado ---")
        print(f"Origen: {ciudad_origen}")
        print(f"Destino: {ciudad_destino}")
        print(f"Distancia aproximada: {distancia:.2f} {etiqueta}")


if __name__ == "__main__":
    mostrar_menu()  

