import json
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from api import obtener_coordenadas
from calculadora_de_distancias import (
    calcular_distancia,
    convertir_horas_a_horas_y_minutos,
    obtener_distancias_y_tiempos,
)


RUTA_CACHE = Path(__file__).resolve().parent / "data" / "coordenadas_cache.json"


def cargar_cache():
    if not RUTA_CACHE.exists():
        return {}

    with RUTA_CACHE.open("r", encoding="utf-8") as archivo:
        cache = json.load(archivo)

    if not isinstance(cache, dict):
        raise ValueError("El contenido del caché debe ser un objeto JSON.")

    return cache


def guardar_cache(cache):
    RUTA_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with RUTA_CACHE.open("w", encoding="utf-8") as archivo:
        json.dump(cache, archivo, ensure_ascii=False, indent=4)


def clave_ciudad(ciudad):
    return ciudad.strip().casefold()


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

    unidad_seleccionada = unidad.get()
    boton_calcular.config(state=tk.DISABLED)
    lbl_resultado.config(text="Calculando...")

    def trabajo():
        try:
            coord_origen = obtener_coordenadas_con_cache(origen, cache)
            coord_destino = obtener_coordenadas_con_cache(destino, cache)

            if coord_origen is None or coord_destino is None:
                resultado = ("no_encontrada", None)
            else:
                distancia_km = calcular_distancia(coord_origen, coord_destino)
                resultado = ("ok", obtener_distancias_y_tiempos(distancia_km))
        except (OSError, ValueError, TypeError) as error:
            resultado = ("error", str(error))

        cola_resultados.put(resultado)

    threading.Thread(target=trabajo, daemon=True).start()
    ventana.after(100, revisar_resultado)


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

        medio_seleccionado = medio.get()
        lineas = []
        if medio_seleccionado in ("avion", "ambos"):
            avion = resultado["avion"]
            lineas.append(
                "Avión: "
                f"{formatear(avion['distancia_km'])} | "
                f"{convertir_horas_a_horas_y_minutos(avion['tiempo_horas'])}"
            )
        if medio_seleccionado in ("carro", "ambos"):
            carro = resultado["carro"]
            lineas.append(
                "Carro: "
                f"{formatear(carro['distancia_km'])} | "
                f"{convertir_horas_a_horas_y_minutos(carro['tiempo_horas'])}"
            )
        lbl_resultado.config(text="\n".join(lineas))


ventana = tk.Tk()
ventana.title("Calculadora de Distancias")
ventana.geometry("390x390")

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
tk.Label(ventana, text="Medio de viaje:").pack(pady=(8, 0))
tk.Radiobutton(
    ventana, text="Avión", variable=medio, value="avion"
).pack()
tk.Radiobutton(
    ventana, text="Carro", variable=medio, value="carro"
).pack()
tk.Radiobutton(
    ventana, text="Ambos", variable=medio, value="ambos"
).pack()

boton_calcular = tk.Button(ventana, text="Calcular", command=calcular)
boton_calcular.pack(pady=10)

lbl_resultado = tk.Label(ventana, text="", font=("Arial", 10, "bold"))
lbl_resultado.pack()

boton_salir = tk.Button(
    ventana,
    text="Salir",
    command=ventana.destroy,
)
boton_salir.pack(pady=(10, 15))

ventana.mainloop()
