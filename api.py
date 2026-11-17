import requests

# URL de la API que estás utilizando
URL_API = "https://jsonplaceholder.typicode.com/todos/1"
URL_GEOCODIFICACION = "https://nominatim.openstreetmap.org/search"
ENCABEZADOS_GEOCODIFICACION = {
    "User-Agent": "calculadora-distancias-isaac-oliver/1.0"
}

def obtener_datos():
    """Realiza la petición HTTPS a la API y devuelve los datos en memoria como diccionario."""
    try:
        respuesta = requests.get(URL_API)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"Error en la API. Código: {respuesta.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error de conexión: {e}")
        return None

def obtener_coordenadas(ciudad):
    """Busca una ciudad y devuelve sus coordenadas como (latitud, longitud)."""
    try:
        respuesta = requests.get(
            URL_GEOCODIFICACION,
            params={"q": ciudad, "format": "jsonv2", "limit": 1},
            headers=ENCABEZADOS_GEOCODIFICACION,
            timeout=10,
        )
        respuesta.raise_for_status()
        resultados = respuesta.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"No se pudieron consultar las coordenadas de {ciudad}: {e}")
        return None

    if not resultados:
        print(f"No se encontró la ciudad «{ciudad}».")
        return None

    try:
        return float(resultados[0]["lat"]), float(resultados[0]["lon"])
    except (KeyError, TypeError, ValueError) as e:
        print(f"La API devolvió coordenadas no válidas para {ciudad}: {e}")
        return None
