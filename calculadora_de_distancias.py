# === Calculadora de Distancias ===
# Autores: Oliver Zavala y Isaac
import sys
import time
from math import atan2, cos, radians, sin, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from api import obtener_coordenadas
RADIO_TIERRA_KM = 6371.0088
VELOCIDAD_AVION_KMH = 800
VELOCIDAD_AUTO_KMH = 80
#Esta función calcula la distancia de gran círculo entre dos pares (latitud, longitud) utilizando la fórmula de Haversine. La distancia se devuelve en kilómetros.

def calcular_distancia(coordenadas_origen, coordenadas_destino):
    """Calcula la distancia de gran círculo entre dos pares (latitud, longitud)."""
    latitud_origen, longitud_origen = map(radians, coordenadas_origen)
    latitud_destino, longitud_destino = map(radians, coordenadas_destino)

    diferencia_latitud = latitud_destino - latitud_origen
    diferencia_longitud = longitud_destino - longitud_origen
    a = (
        sin(diferencia_latitud / 2) ** 2
        + cos(latitud_origen)
        * cos(latitud_destino)
        * sin(diferencia_longitud / 2) ** 2
    )
    a = min(1.0, max(0.0, a))
    angulo_central = 2 * atan2(sqrt(a), sqrt(1 - a))
    return RADIO_TIERRA_KM * angulo_central


def calcular_tiempo_viaje(distancia_km, velocidad_kmh):
    """Calcula el tiempo de viaje en horas."""
    if distancia_km < 0 or velocidad_kmh <= 0:
        raise ValueError("La distancia y la velocidad deben ser válidas.")
    return distancia_km / velocidad_kmh


def convertir_horas_a_horas_y_minutos(horas):
    """Convierte horas decimales a texto en horas y minutos."""
    if horas < 0:
        raise ValueError("Las horas no pueden ser negativas.")

    horas_enteras = int(horas)
    minutos = int(round((horas - horas_enteras) * 60))
    if minutos == 60:
        horas_enteras += 1
        minutos = 0
    return f"{horas_enteras} horas {minutos} minutos"


def obtener_distancias_y_tiempos(distancia_km):
    """Calcula las distancias y los tiempos estimados para avión y automóvil."""
    tiempo_avion = calcular_tiempo_viaje(distancia_km, VELOCIDAD_AVION_KMH)
    tiempo_auto = calcular_tiempo_viaje(distancia_km, VELOCIDAD_AUTO_KMH)
    return {
        "avion": {
            "distancia_km": distancia_km,
            "tiempo_horas": tiempo_avion,
        },
        "carro": {
            "distancia_km": distancia_km,
            "tiempo_horas": tiempo_auto,
        },
    }


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
