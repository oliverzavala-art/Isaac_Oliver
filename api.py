import requests

# URL de la API que estás utilizando
URL_API = "https://jsonplaceholder.typicode.com/todos/1"

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
