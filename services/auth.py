from services.supabase_service import supabase

def login(correo, password):

    resultado = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("correo", correo)
        .eq("password", password)
        .execute()
    )

    if not resultado.data:
        return None

    return resultado.data[0]