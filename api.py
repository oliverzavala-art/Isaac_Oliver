import requests

# URL funcional y estable de prueba
URL_API = "https://jsonplaceholder.typicode.com/posts/1"  # URL de prueba para simular la API externa
def obtener_datos():
    """
    Realiza la petición HTTPS a la API y devuelve los datos 
    del proyecto en memoria como un diccionario. Incluye un sistema
    de respaldo (fallback) por si la API externa falla o no hay internet.
    """
    # Definimos los datos base de tu proyecto para usarlos siempre (o como respaldo)
    datos_proyecto = {
        "proyecto": "Medidas de dimensión y extensión",
        "autor": "Isaac Oliver",
        "ciudad": "Ciudad de Ejemplo",
        "cantidad_poblacion": 150420,
        "extension_km2": 45.8,
        "lugares_habitados": 12,
        "conexion_api_status": 200
    }

    try:
        # Hacemos la petición GET con un User-Agent y un timeout de 5 segundos para evitar bloqueos
        headers = {"User-Agent": "Mozilla/5.0"}
        respuesta = requests.get(URL_API, headers=headers, timeout=5)
        
        if respuesta.status_code == 200:
            print("[✓] Conexión exitosa a la API externa.")
            datos_proyecto["conexion_api_status"] = respuesta.status_code
            return datos_proyecto
        else:
            print(f"[!] La API respondió con el código: {respuesta.status_code}. Usando datos locales.")
            datos_proyecto["conexion_api_status"] = respuesta.status_code
            return datos_proyecto
            
    except requests.exceptions.RequestException as e:
        print(f"[x] Error de conexión con la API externa: {e}")
        print("[->] Activando respaldo: cargando datos locales en memoria.")
        datos_proyecto["conexion_api_status"] = "Offline / Sin conexión"
        return datos_proyecto

# Bloque de ejecución directa de api.py para pruebas en terminal
if __name__ == "__main__":
    print("Probando api.py en terminal...")
    resultado = obtener_datos()
    print("Datos procesados en memoria:", resultado)