from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("URL:", SUPABASE_URL)
print("KEY:", SUPABASE_KEY[:10] if SUPABASE_KEY else None)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def obtener_usuarios():

    respuesta = (
        supabase
        .table("usuarios")
        .select("*")
        .execute()
    )

    return respuesta.data

def guardar_declaracion(datos):

    resultado = (
        supabase
        .table("declaraciones")
        .insert(datos)
        .execute()
    )

    return resultado

def obtener_declaraciones():

    resultado = (
        supabase
        .table("declaraciones")
        .select("*")
        .execute()
    )

    return resultado.data

def actualizar_estado(codigo, estado):

    supabase.table(
        "declaraciones"
    ).update({
        "estado_revision": estado
    }).eq(
        "codigo",
        codigo
    ).execute()