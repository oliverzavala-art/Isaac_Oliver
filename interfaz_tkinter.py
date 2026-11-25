import json
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from api import obtener_coordenadas
from ciudad import Ciudad
from calculadora_de_distancias import (
    calcular_distancia,
    convertir_horas_a_horas_y_minutos,
    obtener_distancias_y_tiempos,
)


RUTA_CACHE = Path(__file__).resolve().parent / "data" / "coordenadas_cache.json"

#Este código define funciones para cargar y guardar un caché de coordenadas de ciudades en un archivo JSON, así como para obtener coordenadas con caché y calcular distancias entre ciudades usando una interfaz gráfica de usuario (GUI) con Tkinter.
#GUI es un entorno visual que permite interactuar con una computadora o dispositivo electrónico mediante elementos gráficos.
#Tkinter. es una aplicación visual creada en Python usando su biblioteca estándar Tkinter para interactuar mediante ventanas, botones, menús y cuadros de texto en lugar de escribir comandos en una consola
def cargar_cache():
    if not RUTA_CACHE.exists():
        return {}

    with RUTA_CACHE.open("r", encoding="utf-8") as archivo:
        cache = json.load(archivo)

    if not isinstance(cache, dict):
        raise ValueError("El contenido del caché debe ser un objeto JSON.")

    return cache

#Este código define una función para guardar un diccionario de caché en un archivo JSON, creando automáticamente la carpeta necesaria si no existe.
def guardar_cache(cache):
    RUTA_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with RUTA_CACHE.open("w", encoding="utf-8") as archivo:
        json.dump(cache, archivo, ensure_ascii=False, indent=4)

#En esta parte del codigo, se define una función para obtener las coordenadas de una ciudad utilizando un caché local. Si las coordenadas 
#ya están en el caché, se devuelven directamente; de lo contrario, se consultan a través de la API y se guardan en el caché para futuras consultas.
def clave_ciudad(ciudad):
    return ciudad.strip().casefold()

#En este codigo la funcion es obtener las coordenadas de una ciudad utilizando un caché local. 
#Si las coordenadas ya están en el caché, se devuelven directamente; de lo contrario, 
#se consultan a través de la API y se guardan en el caché para futuras consultas.
def obtener_coordenadas_con_cache(ciudad, cache):
    clave = clave_ciudad(ciudad)
    if clave in cache:
        coordenadas = cache[clave]
        if (
            isinstance(coordenadas, (list, tuple))
            and len(coordenadas) == 2
        ):
            return float(coordenadas[0]), float(coordenadas[1])

    coordenadas = obtener_coordenadas(ciudad)
    if coordenadas is not None:
        cache[clave] = list(coordenadas)
        guardar_cache(cache)

    return coordenadas

# esta fubcion se encarga de calcular la distancia entre dos ciudades ingresadas por el usuario en la interfaz gráfica. 
# 1Valida las entradas, obtiene las coordenadas de las ciudades (usando caché si es posible), calcula la distancia y el tiempo estimado de viaje según el medio seleccionado (avión, carro o ambos), y finalmente muestra los resultados en la interfaz.
def calcular():
    origen = entrada_origen.get().strip()
    destino = entrada_destino.get().strip()

    if not origen or not destino:
        messagebox.showwarning("Aviso", "Escribe ambas ciudades.")
        return

    if not any(caracter.isalpha() for caracter in origen) or not any(
        caracter.isalpha() for caracter in destino
    ):
        messagebox.showwarning(
            "Aviso",
            "Escribe solo el nombre de la ciudad y el país, sin usar números.",
        )
        return

    boton_calcular.config(state=tk.DISABLED)
    lbl_resultado.config(text="Calculando...")
#Aqui def trabajo es una funcion anidada, que la funcion proincipal es calcular, y se ejecuta en un hilo separado para no bloquear 
# la interfaz gráfica mientras se realizan las operaciones de obtención de coordenadas y cálculo de distancias.
# Es por eso que se utiliza threading.Thread para ejecutar la función trabajo en segundo plano, y luego se revisa el resultado periódicamente con ventana.after.
#Threading threads permite ejecutar múltiples operaciones al mismo tiempo en un programa, lo que es útil para mantener la interfaz de usuario receptiva mientras se realizan tareas que pueden tardar en completarse.

    def trabajo():
        try:
            coord_origen = obtener_coordenadas_con_cache(origen, cache)
            coord_destino = obtener_coordenadas_con_cache(destino, cache)

            if coord_origen is None or coord_destino is None:
                resultado = ("no_encontrada", None)
            else:
                ciudad_origen = Ciudad(origen, *coord_origen)
                ciudad_destino = Ciudad(destino, *coord_destino)
                distancia_km = calcular_distancia(
                    ciudad_origen.coordenadas,
                    ciudad_destino.coordenadas,
                )
                resultado = (
                    "ok",
                    {
                        "ciudad_origen": ciudad_origen,
                        "ciudad_destino": ciudad_destino,
                        "distancia_km": distancia_km,
                        "distancias_y_tiempos": obtener_distancias_y_tiempos(
                            distancia_km
                        ),
                    },
                )
        except (OSError, ValueError, TypeError) as error:
            resultado = ("error", str(error))

        cola_resultados.put(resultado)

    threading.Thread(target=trabajo, daemon=True).start()
    ventana.after(100, revisar_resultado)

#
def revisar_resultado():
    try:
        estado, resultado = cola_resultados.get_nowait()
    except queue.Empty:
        ventana.after(100, revisar_resultado)
        return

    boton_calcular.config(state=tk.NORMAL)

    if estado == "no_encontrada":
        lbl_resultado.config(
            text="No se encontró una ciudad o falló la consulta."
        )
    elif estado == "error":
        lbl_resultado.config(text="No se pudo completar el cálculo.")
        messagebox.showerror("Error", str(resultado))
    else:
        def formatear(kilometros):
            if unidad.get() == "millas":
                return f"{kilometros / 1.609344:.2f} millas"
            return f"{kilometros:.2f} km"

        ciudad_origen = resultado["ciudad_origen"]
        ciudad_destino = resultado["ciudad_destino"]
        distancias_y_tiempos = resultado["distancias_y_tiempos"]
        medio_seleccionado = medio.get()
        lineas = [
            (
                f"Origen - {ciudad_origen.nombre} (latitud, longitud): "
                f"{ciudad_origen.latitud:.6f}, {ciudad_origen.longitud:.6f}"
            ),
            (
                f"Destino - {ciudad_destino.nombre} (latitud, longitud): "
                f"{ciudad_destino.latitud:.6f}, {ciudad_destino.longitud:.6f}"
            ),
        ]
        if medio_seleccionado == "recta":
            lineas.append(
                f"Distancia en línea recta: "
                f"{formatear(resultado['distancia_km'])}"
            )
        else:
            if medio_seleccionado in ("avion", ):
                avion = distancias_y_tiempos["avion"]
                lineas.append(
                    "Avión: "
                    f"{formatear(avion['distancia_km'])} | "
                    f"{convertir_horas_a_horas_y_minutos(avion['tiempo_horas'])}"
                )
            if medio_seleccionado in ("carro", "ambos"):
                carro = distancias_y_tiempos["carro"]
                lineas.append(
                    "Carro: "
                    f"{formatear(carro['distancia_km'])} | "
                    f"{convertir_horas_a_horas_y_minutos(carro['tiempo_horas'])}"
                )
        lbl_resultado.config(text="\n".join(lineas))

class Ciudad:
    def __init__(self, nombre: str, latitud: float, longitud: float):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la ciudad no puede estar vacío.")

        self.nombre = nombre.strip()
        self.latitud = float(latitud)
        self.longitud = float(longitud)

        if not (-90.0 <= self.latitud <= 90.0):
            raise ValueError("La latitud debe estar entre -90 y 90.")
        if not (-180.0 <= self.longitud <= 180.0):
            raise ValueError("La longitud debe estar entre -180 y 180.")

    @property
    def coordenadas(self) -> tuple[float, float]:
        return (self.latitud, self.longitud)

    def __str__(self) -> str:
        return f"{self.nombre} ({self.latitud:.6f}, {self.longitud:.6f})"


ventana = tk.Tk()
ventana.title("Calculadora de Distancias")
ventana.geometry("460x490")

try:
    cache = cargar_cache()
except (OSError, json.JSONDecodeError, ValueError) as error:
    cache = {}
    messagebox.showwarning(
        "Caché",
        f"No se pudo cargar el caché; se iniciará uno nuevo.\n{error}",
    )

cola_resultados = queue.Queue()

tk.Label(ventana, text="Ciudad de origen (con país):").pack(pady=(15, 2))
entrada_origen = tk.Entry(ventana, width=38)
entrada_origen.pack()

tk.Label(ventana, text="Ciudad de destino (con país):").pack(pady=(10, 2))
entrada_destino = tk.Entry(ventana, width=38)
entrada_destino.pack()

unidad = tk.StringVar(value="km")
tk.Radiobutton(
    ventana, text="Kilómetros", variable=unidad, value="km"
).pack(pady=(10, 0))
tk.Radiobutton(
    ventana, text="Millas", variable=unidad, value="millas"
).pack()

medio = tk.StringVar(value="ambos")
tk.Label(ventana, text="Tipo de resultado:").pack(pady=(8, 0))
tk.Radiobutton(
    ventana, text="Línea recta", variable=medio, value="recta"
).pack()
tk.Radiobutton(
    ventana, text="Avión", variable=medio, value="avion"
).pack()
tk.Radiobutton(
    ventana, text="Carro", variable=medio, value="carro"
).pack()
tk.Radiobutton(
    ventana, text="Ambos", variable=medio, value="ambos"
).pack()

lbl_resultado = tk.Label(ventana, text="", font=("Arial", 10, "bold"))
lbl_resultado.pack(padx=10, pady=5)

boton_calcular = tk.Button(
    ventana,
    text="Calcular",
    command=calcular,
)
boton_calcular.pack(pady=(10, 0))

boton_salir = tk.Button(
    ventana,
    text="Salir",
    command=ventana.destroy,
)
boton_salir.pack(pady=(10, 15))

ventana.mainloop()
