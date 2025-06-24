# validacion.py

from datetime import datetime

def validar_titulo(titulo):
    return bool(titulo.strip())

def validar_fecha(fecha_str):
    if not fecha_str.strip():
        return True  # permitir fecha vacía (opcional)
    try:
        datetime.strptime(fecha_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False

def formatear_fecha(fecha_str):
    """
    Recibe una fecha '2-2-2005' y devuelve '02-02-2005'
    """
    try:
        fecha_dt = datetime.strptime(fecha_str.strip(), "%d-%m-%Y")
        return fecha_dt.strftime("%d-%m-%Y")
    except ValueError:
        return fecha_str  # si falla, retorna la original
