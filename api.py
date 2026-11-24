import requests

URL_API = "https://jsonplaceholder.typicode.com/todos/1"
URL_GEOCODIFICACION = "https://nominatim.openstreetmap.org/search"
ENCABEZADOS_GEOCODIFICACION = {
    "User-Agent": "calculadora-distancias-isaac-oliver/1.0"
}


def obtener_datos():
    """Realiza la petición HTTPS a la API y devuelve los datos en memoria como diccionario."""
    try:
        respuesta = requests.get(URL_API, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as error:
        print(f"Ocurrió un error de conexión: {error}")
        return None
    except ValueError as error:
        print(f"La API devolvió datos no válidos: {error}")
        return None


def obtener_coordenadas(ciudad):
    """Busca una ciudad y devuelve sus coordenadas como (latitud, longitud)."""
    try:
        respuesta = requests.get(
            URL_GEOCODIFICACION,
            params={
                "q": ciudad,
                "format": "jsonv2",
                "limit": 1,
                "featureType": "city",
            },
            headers=ENCABEZADOS_GEOCODIFICACION,
            timeout=10,
        )
        respuesta.raise_for_status()
        resultados = respuesta.json()
    except (requests.exceptions.RequestException, ValueError) as error:
        print(f"No se pudieron consultar las coordenadas de {ciudad}: {error}")
        return None

    if not resultados:
        print(f"No se encontró la ciudad «{ciudad}».")
        return None

    try:
        return float(resultados[0]["lat"]), float(resultados[0]["lon"])
    except (KeyError, TypeError, ValueError) as error:
        print(f"La API devolvió coordenadas no válidas para {ciudad}: {error}")
        return None
