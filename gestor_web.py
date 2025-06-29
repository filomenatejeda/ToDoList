# gestor_web.py

# Se importa la clase Tarea para crear y manipular tareas, así como la clase datetime y timedelta para manejar fechas y horas
import json
from core.tarea import Tarea
from datetime import datetime, timedelta

# Se define la clase GestorTareasWeb para gestionar las tareas y sus operaciones
class GestorTareasWeb:
    # Se define el constructor de la clase GestorTareasWeb para inicializar la lista de tareas vacía
    def __init__(self):
        self.lista_tareas = []

    # Se define el método agregar_tarea para agregar una tarea a la lista de tareas y guardar el archivo
    def agregar_tarea(self, tarea):
        self.lista_tareas.append(tarea)
        self.guardar_en_archivo()

    # Se define el método eliminar_tarea para eliminar una tarea de la lista de tareas y guardar el archivo
    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.lista_tareas):
            self.lista_tareas.pop(indice)
            self.guardar_en_archivo()

    # Se define el método marcar_pendiente para marcar una tarea como pendiente y guardar el archivo
    def marcar_pendiente(self, indice):
        if 0 <= indice < len(self.lista_tareas):
            self.lista_tareas[indice].estado = "pendiente"
            self.guardar_en_archivo()

    # Se define el método marcar_progreso para marcar una tarea como en progreso y guardar el archivo
    def marcar_progreso(self, indice):
        if 0 <= indice < len(self.lista_tareas):
            if (self.lista_tareas[indice].estado == "completada"):
                self.lista_tareas[indice].fecha_completada = None
            self.lista_tareas[indice].estado = "en progreso"
            self.guardar_en_archivo()

    # Se define el método marcar_completada para marcar una tarea como completada, establecer la fecha de completado y guardar el archivo
    def marcar_completada(self, indice):
        if 0 <= indice < len(self.lista_tareas):
            self.lista_tareas[indice].estado = "completada"
            self.lista_tareas[indice].fecha_completada = datetime.today().strftime("%d-%m-%Y")
            self.guardar_en_archivo()

    # Se define el método editar_tarea para editar una tarea y guardar el archivo
    def editar_tarea(self, indice, nuevo_titulo, nueva_desc, nueva_fecha, nueva_prioridad, nueva_categoria):
        tarea = self.lista_tareas[indice]

        # Se verifica si los nuevos valores no están vacíos y se actualizan los atributos de la tarea
        if nuevo_titulo and nuevo_titulo.strip():
            tarea.titulo = nuevo_titulo.strip()

        # Se verifica si la descripción no está vacía y se actualiza el atributo de la tarea
        if nueva_desc and nueva_desc.strip():
            tarea.descripcion = nueva_desc.strip()

        # Se verifica si la fecha de vencimiento no está vacía y se actualiza el atributo de la tarea
        if nueva_fecha and nueva_fecha.strip():
            tarea.fecha_vencimiento = nueva_fecha.strip()

        # Se verifica si la prioridad es válida y se actualiza el atributo de la tarea
        if nueva_prioridad and nueva_prioridad.strip().lower() in ["alta", "media", "baja"]:
            tarea.prioridad = nueva_prioridad.strip().lower()
        # Se verifica si la nueva categoría no está vacía y se actualiza el atributo de la tarea
        if nueva_categoria is not None:
            tarea.categoria = nueva_categoria.strip()
        self.guardar_en_archivo()

    # Se define el método buscar_tareas para buscar las tareas según una palabra clave en título o descripción
    def buscar_tareas(self, palabra_clave):
        palabra = palabra_clave.lower()
        resultados = []

        # Se recorre la lista de tareas y se busca la tarea con el título o descripción especificado
        for t in self.lista_tareas:
            en_titulo = palabra in t.titulo.lower()
            en_descripcion = palabra in t.descripcion.lower()
            en_estado = palabra in t.estado.lower()
            en_fecha = t.fecha_vencimiento and palabra in t.fecha_vencimiento.lower()
            en_subtareas = any(palabra in subt["nombre"].lower() for subt in t.subtareas)

            # Si la tarea cumple con los filtros, se agrega a la lista de tareas filtradas
            if en_titulo or en_descripcion or en_estado or en_fecha or en_subtareas:
                resultados.append(t)

        return resultados

    # Se define el método obtener_tareas_filtradas para obtener las tareas filtradas según los filtros de estado, fecha máxima y orden
    def obtener_tareas_filtradas(self, filtro_estado=None, fecha_maxima=None, ordenar_por=None):
        tareas_filtradas = self.lista_tareas.copy()

        # Filtrar por estado
        if filtro_estado:
            tareas_filtradas = [t for t in tareas_filtradas if t.estado.lower() == filtro_estado.lower()]

        # Filtrar por fecha
        if fecha_maxima:
            try:
                # Se intenta convertir la fecha máxima a un objeto datetime
                fecha_max_dt = datetime.strptime(fecha_maxima, "%d-%m-%Y")
                tareas_filtradas = [t for t in tareas_filtradas if t.fecha_vencimiento and datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y") <= fecha_max_dt]
            except ValueError:
                pass

        # Ordenar las tareas filtradas según el criterio especificado
        if ordenar_por == "fecha":
            tareas_filtradas.sort(key=lambda t: datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y") if t.fecha_vencimiento else datetime.max)
        elif ordenar_por == "estado":
            tareas_filtradas.sort(key=lambda t: t.estado)
        elif ordenar_por == "prioridad":
            tareas_filtradas.sort(key=lambda t: {"alta": 1, "media": 2, "baja": 3}.get(t.prioridad, 2))

        return tareas_filtradas

    # Se define el método obtener_proximas_tareas para obtener las próximas tareas que vencen en un plazo determinado de días
    def obtener_proximas_tareas(self, dias=3):
        # Se obtiene la fecha actual y se calcula la fecha límite sumando los días especificados
        hoy = datetime.today()
        limite = hoy + timedelta(days=dias)
        proximas = []
        # Se recorre la lista de tareas y se verifica si la fecha de vencimiento está dentro del rango límite
        for t in self.lista_tareas:
            if t.fecha_vencimiento:
                try:
                    # Se intenta convertir la fecha de vencimiento de la tarea a un objeto datetime
                    fecha_tarea = datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y")
                    # Se verifica si la fecha de vencimiento es dentro del rango límite
                    if hoy <= fecha_tarea <= limite:
                        proximas.append(t)
                except ValueError:
                    pass
        return proximas

    # Se define el método para guardar las tareas en un archivo JSON
    def guardar_en_archivo(self, archivo="data/tareas.json"):
        try:
            # Se abre el archivo en modo escritura y se guarda la lista de tareas en formato JSON
            with open(archivo, "w", encoding="utf-8") as f:
                # Se convierte cada tarea a un diccionario y se guarda en el archivo
                json.dump([t.to_dict() for t in self.lista_tareas], f, indent=4)
        except Exception as e:
            print(f"Error al guardar: {e}")

    # Se define el método para cargar las tareas desde un archivo JSON
    def cargar_desde_archivo(self, archivo="data/tareas.json"):
        try:
            # Se intenta abrir el archivo en modo lectura y cargar las tareas desde el archivo JSON
            with open(archivo, "r", encoding="utf-8") as f:
                tareas_cargadas = json.load(f)
                # Se crea una lista de tareas a partir de los diccionarios cargados
                self.lista_tareas = [Tarea.from_dict(t) for t in tareas_cargadas]
        except FileNotFoundError:
            print("No se encontró archivo, empezando con lista vacía.")
        except Exception as e:
            print(f"Error al cargar: {e}")

    # Se define el método agregar_subtarea para agregar una subtarea a una tarea existente y guardar el archivo
    def agregar_subtarea(self, indice, texto):
        # Se verifica si el índice es válido y se agrega la subtarea al diccionario de la tarea
        if 0 <= indice < len(self.lista_tareas):
         subtarea = { "nombre": texto, "completada": False }
         self.lista_tareas[indice].subtareas.append(subtarea)
         self.guardar_en_archivo()
         
    # Se define el método buscar_tareas_avanzada para buscar las tareas avanzadas según un texto, un estado o una prioridad
    def buscar_tareas_avanzada(self, texto="", estado="", prioridad=""):
        # Se convertir los parámetros a minúsculas
        texto = texto.lower()
        estado = estado.lower()
        prioridad = prioridad.lower()

        resultados = []

        # Se recorre la lista de tareas y se busca la tarea con el título o descripción especificado
        for t in self.lista_tareas:
            match_texto = texto in t.titulo.lower() or texto in t.descripcion.lower()
            match_estado = (estado == "" or t.estado.lower() == estado)
            match_prioridad = (prioridad == "" or t.prioridad.lower() == prioridad)

            # Si la tarea cumple con los filtros, se agrega a la lista de tareas filtradas
            if match_texto and match_estado and match_prioridad:
                resultados.append(t)

        return resultados
    
    # Se define el método obtener_tareas_por_estado para obtener las tareas agrupadas por estado
    def obtener_tareas_por_estado(self):
        # Se crean listas para almacenar las tareas por estado
        tareas_completadas = []
        tareas_en_progreso = []
        tareas_pendientes = []

        # Se recorre la lista de tareas y se agregan las tareas por estado
        for t in self.lista_tareas:
            if t.estado == "completada":
                tareas_completadas.append(tareas_completadas)
            elif t.estado == "en progreso":
                tareas_en_progreso.append(tareas_en_progreso)
            else:
                tareas_pendientes.append(tareas_pendientes)
        
        return tareas_completadas, tareas_en_progreso, tareas_pendientes
    
    # Se define el método obtener_ultimas_tareas_completadas para obtener las últimas tareas completadas en un plazo determinado de días
    def obtener_ultimas_tareas_completadas(self, dias=7):
        # Se obtiene la fecha actual y se calcula la fecha límite sumando los días especificados
        hoy = datetime.today()
        limite = hoy - timedelta(days=dias)
        ultimas = []
        # Se recorre la lista de tareas y se verifica si la fecha de vencimiento está dentro del rango límite
        for t in self.lista_tareas:
            if t.fecha_completada:
                try:
                    # Se intenta convertir la fecha de vencimiento de la tarea a un objeto datetime
                    fecha_tarea = datetime.strptime(t.fecha_completada, "%d-%m-%Y")
                    # Se verifica si la fecha de vencimiento es dentro del rango límite
                    if limite <= fecha_tarea <= hoy or fecha_tarea.strftime("%d-%m-%Y").__eq__(hoy.strftime("%d-%m-%Y")):
                        ultimas.append(t)
                except ValueError:
                    pass
        return ultimas