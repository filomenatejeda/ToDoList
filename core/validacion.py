# validacion.py
# Se importa la librería de datetime para manejar fechas
# Se definen funciones para validar y formatear títulos y fechas
from datetime import datetime

# Se define la función para validar y formatear títulos 
def validar_titulo(titulo):
    return bool(titulo.strip()) # verifica si el título no está vacío

# Se define la función para validar fechas
# La función recibe una cadena de texto y verifica si es una fecha válida en el formato 'd-m-Y'
def validar_fecha(fecha_str):
    if not fecha_str.strip():
        return True  # permitir fecha vacía (opcional)
    try:
        datetime.strptime(fecha_str, "%d-%m-%Y") # intenta convertir la cadena a un objeto datetime
        return True  # si no falla, es válida
    except ValueError:  # si falla, no es válida
        return False

# Se define la función para formatear fechas
# La función recibe una cadena de texto con una fecha y la devuelve en el formato 'dd-mm-aaaa'
def formatear_fecha(fecha_str):
    """
    Recibe una fecha '2-2-2005' y devuelve '02-02-2005'
    """
    try:
        fecha_dt = datetime.strptime(fecha_str.strip(), "%d-%m-%Y")  # intenta convertir la cadena a un objeto datetime
        return fecha_dt.strftime("%d-%m-%Y") # si no falla, devuelve la fecha formateada
    except ValueError:
        return fecha_str  # si falla, retorna la original
