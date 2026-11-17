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
    """
    Procesa el diccionario cargado en memoria y muestra 
    las categorías del proyecto de forma estructurada.
    """
    if datos:
        print("\n¡Conexión exitosa a la API! Procesando datos en memoria...\n")
        print("-" * 45)
        print("   REPORTE DE DATOS OBTENIDOS")
        print("-" * 45)
        
        # Mostramos los datos directamente desde el diccionario de Python
        print(f"   Datos RAW en memoria : {datos}")
        print(f"   Proyecto             : {datos.get('proyecto', 'N/A')}")
        print(f"   Autor                : {datos.get('autor', 'N/A')}")
        print(f"   Ciudad               : {datos.get('ciudad', 'N/A')}")
        print(f"   Población            : {datos.get('cantidad_poblacion', 'N/A')}")
        print(f"   Extensión (km²)      : {datos.get('extension_km2', 'N/A')}")
        print(f"   Lugares habitados    : {datos.get('lugares_habitados', 'N/A')}")
        print(f"   Estado HTTP          : {datos.get('conexion_api_status', 'N/A')}")
        print("-" * 45)
    else:
        print("\nError: No se pudieron obtener datos desde api.py.")

def main():
    """Función principal que coordina la ejecución del programa."""
    mostrar_encabezado()
    print("\nIniciando consulta a través de api.py...")
    
    # Llamamos a la API y guardamos los datos directamente en memoria
    datos_obtenidos = obtener_datos()
    
    # Procesamos los datos en la terminal
    procesar_reporte(datos_obtenidos)
    print("\nEjecución finalizada con éxito.")

if __name__ == "__main__":
    main()