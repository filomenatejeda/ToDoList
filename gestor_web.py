# gestor_web.py

import json
from core.tarea import Tarea
from datetime import datetime, timedelta

class GestorTareasWeb:
    def __init__(self):
        self.lista_tareas = []

    def agregar_tarea(self, tarea):
        self.lista_tareas.append(tarea)
        self.guardar_en_archivo()

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.lista_tareas):
            self.lista_tareas.pop(indice)
            self.guardar_en_archivo()

    def marcar_completada(self, indice):
        if 0 <= indice < len(self.lista_tareas):
            self.lista_tareas[indice].estado = "completada"
            self.guardar_en_archivo()

    def cambiar_estado_tarea(self, indice):
        if 0 <= indice < len(self.lista_tareas):
            tarea = self.lista_tareas[indice]
            if tarea.estado == "pendiente":
                tarea.estado = "en progreso"
            elif tarea.estado == "en progreso":
                tarea.estado = "completada"
            self.guardar_en_archivo()

    def editar_tarea(self, indice, nuevo_titulo, nueva_desc, nueva_fecha, nueva_prioridad):
        tarea = self.lista_tareas[indice]
        if nuevo_titulo.strip():
            tarea.titulo = nuevo_titulo
        if nueva_desc.strip():
            tarea.descripcion = nueva_desc
        if nueva_fecha.strip():
            tarea.fecha_vencimiento = nueva_fecha
        if nueva_prioridad.strip().lower() in ["alta", "media", "baja"]:
            tarea.prioridad = nueva_prioridad.lower()
        self.guardar_en_archivo()

    def agregar_subtarea(self, indice, subtarea):
        tarea = self.lista_tareas[indice]
        tarea.subtareas.append(subtarea)
        self.guardar_en_archivo()

    def buscar_tareas(self, palabra_clave):
        palabra = palabra_clave.lower()
        resultados = []

        for t in self.lista_tareas:
            en_titulo = palabra in t.titulo.lower()
            en_descripcion = palabra in t.descripcion.lower()
            en_estado = palabra in t.estado.lower()
            en_fecha = t.fecha_vencimiento and palabra in t.fecha_vencimiento.lower()
            en_subtareas = any(palabra in subt["nombre"].lower() for subt in t.subtareas)

            if en_titulo or en_descripcion or en_estado or en_fecha or en_subtareas:
                resultados.append(t)

        return resultados

    def obtener_tareas_filtradas(self, filtro_estado=None, fecha_maxima=None, ordenar_por=None):
        tareas_filtradas = self.lista_tareas.copy()

        # Filtrar estado
        if filtro_estado:
            tareas_filtradas = [t for t in tareas_filtradas if t.estado.lower() == filtro_estado.lower()]

        # Filtrar por fecha
        if fecha_maxima:
            try:
                fecha_max_dt = datetime.strptime(fecha_maxima, "%d-%m-%Y")
                tareas_filtradas = [t for t in tareas_filtradas if t.fecha_vencimiento and datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y") <= fecha_max_dt]
            except ValueError:
                pass

        # Ordenar
        if ordenar_por == "fecha":
            tareas_filtradas.sort(key=lambda t: datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y") if t.fecha_vencimiento else datetime.max)
        elif ordenar_por == "estado":
            tareas_filtradas.sort(key=lambda t: t.estado)
        elif ordenar_por == "prioridad":
            tareas_filtradas.sort(key=lambda t: {"alta": 1, "media": 2, "baja": 3}.get(t.prioridad, 2))

        return tareas_filtradas

    def obtener_proximas_tareas(self, dias=3):
        hoy = datetime.today()
        limite = hoy + timedelta(days=dias)
        proximas = []
        for t in self.lista_tareas:
            if t.fecha_vencimiento:
                try:
                    fecha_tarea = datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y")
                    if hoy <= fecha_tarea <= limite:
                        proximas.append(t)
                except ValueError:
                    pass
        return proximas

    def guardar_en_archivo(self, archivo="data/tareas.json"):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.lista_tareas], f, indent=4)
        except Exception as e:
            print(f"Error al guardar: {e}")

    def cargar_desde_archivo(self, archivo="data/tareas.json"):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                tareas_cargadas = json.load(f)
                self.lista_tareas = [Tarea.from_dict(t) for t in tareas_cargadas]
        except FileNotFoundError:
            print("No se encontró archivo, empezando con lista vacía.")
        except Exception as e:
            print(f"Error al cargar: {e}")
    
    def agregar_subtarea(self, titulo, nombre_subtarea):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.subtareas.append({"nombre": nombre_subtarea, "completada": False})
                print("Subtarea agregada.")
                self.guardar_en_archivo()
                return
        print(f"No se encontró tarea con título '{titulo}'.")
    def agregar_subtarea(self, indice, texto):
        if 0 <= indice < len(self.lista_tareas):
         subtarea = { "nombre": texto, "completada": False }
         self.lista_tareas[indice].subtareas.append(subtarea)
         self.guardar_en_archivo()
    def buscar_tareas_avanzada(self, texto="", estado="", prioridad=""):
        texto = texto.lower()
        estado = estado.lower()
        prioridad = prioridad.lower()

        resultados = []

        for t in self.lista_tareas:
            match_texto = texto in t.titulo.lower() or texto in t.descripcion.lower()
            match_estado = (estado == "" or t.estado.lower() == estado)
            match_prioridad = (prioridad == "" or t.prioridad.lower() == prioridad)

            if match_texto and match_estado and match_prioridad:
                resultados.append(t)

        return resultados

