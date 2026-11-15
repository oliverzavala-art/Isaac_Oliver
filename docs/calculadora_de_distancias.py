# === Calculadora de Distancias ===
# Autores : Oliver Zavala y Isaac
# === Menú de opciones ===
'''
1. Calcular distancia
2. Salir
Elige una opción: 1

Ciudad de origen: San Marcos, Guatemala
Ciudad de destino: Salt Lake City, Estados Unidos
Unidad (km/millas): km

--- Resumen ---
Origen:  San Marcos, Guatemala
Destino: Salt Lake City, Estados Unidos
Unidad:  kilómetros
Consultando datos...'''

from api import obtener_coordenadas

def mostrar_menu():
    """Mostrar el menú de opciones de la calculadora de distancias."""
    print("\n=== Calculadora de Distancias ===")
    print("1. Calcular distancia")
    print("2. Salir")

    def pedir_ciudad(mensaje):
        return input(mensaje)
