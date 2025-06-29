# gestor.py

# Se importa la clase Tarea para crear y manipular tareas, así como la clase datetime y timedelta para manejar fechas y horas
import json
from core.tarea import Tarea
from datetime import datetime, timedelta

# Se define la clase GestorTareas para gestionar las tareas y sus operaciones
class GestorTareas:
    # Se define el constructor de la clase GestorTareas para inicializar la lista de tareas vacía
    def __init__(self):
        self.lista_tareas = []

    # Se define el método agregar_tarea para agregar una tarea a la lista de tareas y guardar el archivo
    def agregar_tarea(self, tarea):
        self.lista_tareas.append(tarea)
        self.guardar_en_archivo()

    # Se define el método eliminar_tarea para eliminar una tarea de la lista de tareas y guardar el archivo
    def eliminar_tarea(self):
        if not self.lista_tareas:
            print("No hay tareas para eliminar.")
            return

        # Se muestra la lista de tareas y se solicita al usuario que seleccione la tarea a eliminar
        print("\n=== TAREAS DISPONIBLES ===")
        for idx, tarea in enumerate(self.lista_tareas, 1):
            print(f"{idx}. [{tarea.estado.upper()}] {tarea.titulo} - {tarea.descripcion} (Vence: {tarea.fecha_vencimiento})")

        try:
            # Se solicita al usuario que seleccione la tarea a eliminar
            seleccion = int(input("Ingrese el número de la tarea a eliminar: "))
            if 1 <= seleccion <= len(self.lista_tareas):
                tarea_eliminada = self.lista_tareas[seleccion - 1]

                # Se solicita al usuario si desea eliminar la tarea
                confirm = input(f"¿Está seguro que desea eliminar '{tarea_eliminada.titulo}'? (s/n): ")
                if confirm.lower() == "s":
                    self.lista_tareas.pop(seleccion - 1)
                    print(f"Tarea '{tarea_eliminada.titulo}' eliminada.")
                    self.guardar_en_archivo()
                else:
                    print("Eliminación cancelada.")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada no válida. Ingrese un número.")

    # Se define el método marcar_pendiente para marcar una tarea como pendiente y guardar el archivo
    def marcar_pendiente(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.estado = "pendiente"
                print(f"Tarea '{titulo}' marcada como pendiente.")
                self.guardar_en_archivo()
                return

        print(f"No se encontró la tarea con título '{titulo}'.")

    # Se define el método marcar_progreso para marcar una tarea como en progreso y guardar el archivo
    def marcar_progreso(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.estado = "en progreso"
                print(f"Tarea '{titulo}' marcada como en progreso.")
                self.guardar_en_archivo()
                return

        print(f"No se encontró la tarea con título '{titulo}'.")

    # Se define el método marcar_completada para marcar una tarea como completada y guardar el archivo
    def marcar_completada(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.estado = "completada"
                print(f"Tarea '{titulo}' marcada como completada.")
                self.guardar_en_archivo()
                return

        print(f"No se encontró la tarea con título '{titulo}'.")

    # Se define el método mostrar_tareas para mostrar las tareas filtradas y ordenadas según los parámetros
    def mostrar_tareas(self, filtro_estado=None, fecha_maxima=None, ordenar_por=None):
        # Se verifica si hay tareas para mostrar
        if not self.lista_tareas:
            print("No hay tareas.")
            return

        # Se crea una variable fecha_max_dt para almacenar la fecha máxima filtrada
        fecha_max_dt = None
        if fecha_maxima:
            try:
                # Se intenta convertir la fecha máxima a un objeto datetime
                fecha_max_dt = datetime.strptime(fecha_maxima, "%d-%m-%Y")
            except ValueError:
                print(" Fecha máxima inválida. Ignorando filtro de fecha.")
                fecha_max_dt = None

        # Se filtran las tareas según el estado y la fecha máxima
        tareas_filtradas = []
        for t in self.lista_tareas:
            incluir = True

            # Se filtra la tarea según el estado
            if filtro_estado and t.estado.lower() != filtro_estado.lower():
                incluir = False

            # Se filtra la tarea según la fecha máxima
            if fecha_max_dt and t.fecha_vencimiento:
                try:
                    # Se intenta convertir la fecha de vencimiento de la tarea a un objeto datetime
                    fecha_tarea_dt = datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y")
                    if fecha_tarea_dt > fecha_max_dt:
                        incluir = False
                except ValueError:
                    incluir = False

            # Si la tarea cumple con los filtros, se agrega a la lista de tareas filtradas
            if incluir:
                tareas_filtradas.append(t)

        # Se ordenan las tareas filtradas según el criterio especificado
        if ordenar_por == "fecha":
            tareas_filtradas.sort(key=lambda t: datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y") if t.fecha_vencimiento else datetime.max)
        elif ordenar_por == "estado":
            tareas_filtradas.sort(key=lambda t: t.estado)
        elif ordenar_por == "prioridad":
            tareas_filtradas.sort(key=lambda t: {"alta": 1, "media": 2, "baja": 3}.get(t.prioridad, 2))

        # Se muestra la lista de tareas filtradas
        print("\n=== LISTA DE TAREAS ===")
        # Se obtiene la fecha actual para verificar si las tareas están vencidas
        hoy = datetime.today()

        # Se recorre la lista de tareas filtradas, se muestra su estado y fecha de vencimiento
        for tarea in tareas_filtradas:
            vencida = ""
            if tarea.fecha_vencimiento:
                try:
                    # Se intenta convertir la fecha de vencimiento de la tarea a un objeto datetime
                    fecha_tarea_dt = datetime.strptime(tarea.fecha_vencimiento, "%d-%m-%Y")
                    # Se verifica si la tarea está vencida
                    if fecha_tarea_dt < hoy:
                        vencida = "  VENCIDA"
                except ValueError:
                    vencida = "  Fecha inválida"

            print(f"[{tarea.estado.upper()}] {tarea.titulo} - {tarea.descripcion} (Vence: {tarea.fecha_vencimiento}) [Prioridad: {tarea.prioridad.upper()}]{vencida}")

            # Si la tarea tiene subtareas, se muestran
            if tarea.subtareas:
                print("  Subtareas:")
                for idx, subtarea in enumerate(tarea.subtareas, 1):
                    print(f"    {idx}. {subtarea}")

    # Se define el método para guardar las tareas en un archivo JSON
    def guardar_en_archivo(self, archivo="data/tareas.json"):
        try:
            # Se abre el archivo en modo escritura y se guarda la lista de tareas en formato JSON
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump([tarea.to_dict() for tarea in self.lista_tareas], f, indent=4)
        except Exception as e:
            print(f"Error al guardar: {e}")

    # Se define el método para cargar las tareas desde un archivo JSON
    def cargar_desde_archivo(self, archivo="data/tareas.json"):
        try:
            # Se abre el archivo en modo lectura y se carga la lista de tareas desde formato JSON
            with open(archivo, "r", encoding="utf-8") as f:
                tareas_cargadas = json.load(f)
                self.lista_tareas = [Tarea.from_dict(t) for t in tareas_cargadas]
        # Si no se encuentra el archivo, se muestra un mensaje de error
        except FileNotFoundError:
            print("No se encontró archivo, empezando con lista vacía.")
        except Exception as e:
            print(f"Error al cargar: {e}")

    # Se define el método para editar una tarea
    def editar_tarea(self, titulo):
        # Se recorre la lista de tareas y se busca la tarea con el título especificado
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                print(f"Editando tarea: {tarea.titulo}")
                nuevo_titulo = input("Nuevo título (enter para mantener): ")
                nueva_desc = input("Nueva descripción (enter para mantener): ")
                nueva_fecha = input("Nueva fecha de vencimiento (enter para mantener): ")
                nueva_prioridad = input("Nueva prioridad (alta / media / baja) (enter para mantener): ")

                if nuevo_titulo.strip():
                    tarea.titulo = nuevo_titulo
                if nueva_desc.strip():
                    tarea.descripcion = nueva_desc
                if nueva_fecha.strip():
                    tarea.fecha_vencimiento = nueva_fecha
                if nueva_prioridad.strip().lower() in ["alta", "media", "baja"]:
                    tarea.prioridad = nueva_prioridad.lower()

                print("Tarea actualizada.")
                self.guardar_en_archivo()
                return
        print(f"No se encontró tarea con título '{titulo}'.")

    # Se define el método para cambiar el estado de una tarea
    def cambiar_estado_tarea(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                print(f"Estado actual: {tarea.estado}")
                if tarea.estado == "pendiente":
                    tarea.estado = "en progreso"
                elif tarea.estado == "en progreso":
                    tarea.estado = "completada"
                else:
                    print("La tarea ya está completada.")
                    return
                print(f"Estado actualizado a {tarea.estado}.")
                self.guardar_en_archivo()
                return
        print(f"No se encontró tarea con título '{titulo}'.")

    # Se define el método para buscar tareas por palabra clave en título o descripción
    def buscar_tareas(self, palabra_clave):
        resultados = [t for t in self.lista_tareas if palabra_clave.lower() in t.titulo.lower() or palabra_clave.lower() in t.descripcion.lower()]
        if resultados:
            print("\n=== RESULTADOS DE BÚSQUEDA ===")
            for tarea in resultados:
                print(f"[{tarea.estado.upper()}] {tarea.titulo} - {tarea.descripcion} (Vence: {tarea.fecha_vencimiento})")
        else:
            print("No se encontraron tareas con esa palabra clave.")

    # Se define el método para agregar una subtarea a una tarea existente
    def agregar_subtarea(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                subtarea = input("Ingrese subtarea: ")
                tarea.subtareas.append(subtarea)
                print("Subtarea agregada.")
                self.guardar_en_archivo()
                return
        print(f"No se encontró tarea con título '{titulo}'.")

    # Se define el método para mostrar las próximas tareas que vencen en un plazo determinado de días
    def mostrar_proximas_tareas(self, dias=3):
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
                    if hoy <= fecha_tarea <= limite:
                        proximas.append(t)
                except ValueError:
                    pass

        # Se muestra la lista de tareas próximas a vencer
        if proximas:
            print(f"\nEstas tareas vencen en los próximos {dias} días:")
            for t in proximas:
                print(f"[{t.estado.upper()}] {t.titulo} (Vence: {t.fecha_vencimiento})")
        else:
            print("\nNo hay tareas próximas a vencer.")

# Se define el método para eliminar una tarea por título
def eliminar_tarea_por_titulo(self, titulo):
    self.lista_tareas = [t for t in self.lista_tareas if t.titulo != titulo]
    self.guardar_en_archivo()
