# ==========================================
# Proyecto Final: Medidas de dimensión y extensión
# Autor: Isaac Oliver
# Archivo: main.py
# ==========================================

from api import obtener_datos


def mostrar_encabezado():
    """Imprime el encabezado del proyecto en la terminal."""
    print("=" * 50)
    print("   PROYECTO FINAL: MEDIDAS DE DIMENSIÓN Y EXTENSIÓN")
    print("   Autor: Isaac Oliver")
    print("=" * 50)


def procesar_reporte(datos):
    """Procesa y muestra los datos obtenidos."""
    if datos:
        print("\n¡Conexión exitosa a la API! Procesando datos en memoria...\n")
        print("-" * 40)
        print("  REPORTE DE DATOS OBTENIDOS")
        print("-" * 40)
        print(f"  Datos RAW en memoria: {datos}")
        print(f"  ID de consulta     : {datos.get('id', 'N/A')}")
        print(f"  Registro / Título  : {datos.get('title', 'N/A')}")
        print(f"  Estado de proceso  : {datos.get('completed', False)}")
        print("-" * 40)
    else:
        print("\nError: No se pudieron obtener datos desde api.py.")


def main():
    """Función principal que coordina la ejecución del programa."""
    mostrar_encabezado()
    print("\nIniciando consulta a través de api.py...")
    datos_obtenidos = obtener_datos()
    procesar_reporte(datos_obtenidos)
    print("\nEjecución finalizada con éxito.")


if __name__ == "__main__":
    main()
