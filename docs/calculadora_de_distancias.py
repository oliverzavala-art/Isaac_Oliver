# === Calculadora de Distancias ===
# Autores: Oliver Zavala y Isaac
import sys
import time
from math import atan2, cos, radians, sin, sqrt
from pathlib import Path
import math
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api import obtener_coordenadas
from math import atan2, cos, radians, sin, sqrt
RADIO_TIERRA_KM = 6371.0088


def calcular_distancia(coordenadas_origen, coordenadas_destino):
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
    """Solicita una ciudad y rechaza una respuesta vacía."""
    while True:
        ciudad = input(mensaje).strip()
        if ciudad:
            return ciudad
        print("Por favor, ingresa una ciudad válida.")


def pedir_unidad():
    """Solicita la unidad en la que se mostrará la distancia."""
    while True:
        unidad = input("Unidad (km/millas): ").strip().lower()
        if unidad in ("km", "millas"):
            return unidad
        print("Por favor, ingresa «km» o «millas».")

def mostrar_menu():
    """Muestra el menú y calcula distancias entre las ciudades elegidas."""
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