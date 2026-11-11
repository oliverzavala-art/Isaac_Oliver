from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos
class Usuario(BaseModel):
    nombre: str
    email: str

# Base de datos ficticia en memoria
usuarios_db = []

# Ruta GET: Obtener todos los usuarios
@app.get("/usuarios")
def obtener_usuarios():
    return {"usuarios": usuarios_db}

# Ruta POST: Crear un nuevo usuario
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    usuarios_db.append(usuario.dict())
    return {"mensaje": "Usuario creado exitosamente", "usuario": usuario}
