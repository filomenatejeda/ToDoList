# gestor.py

import json
from core.tarea import Tarea
from datetime import datetime, timedelta

class GestorTareas:
    def __init__(self):
        self.lista_tareas = []

    def agregar_tarea(self, tarea):
        self.lista_tareas.append(tarea)
        self.guardar_en_archivo()

    def eliminar_tarea(self):
        if not self.lista_tareas:
            print("No hay tareas para eliminar.")
            return

        print("\n=== TAREAS DISPONIBLES ===")
        for idx, tarea in enumerate(self.lista_tareas, 1):
            print(f"{idx}. [{tarea.estado.upper()}] {tarea.titulo} - {tarea.descripcion} (Vence: {tarea.fecha_vencimiento})")

        try:
            seleccion = int(input("Ingrese el número de la tarea a eliminar: "))
            if 1 <= seleccion <= len(self.lista_tareas):
                tarea_eliminada = self.lista_tareas[seleccion - 1]

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

    def marcar_pendiente(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.estado = "pendiente"
                print(f"Tarea '{titulo}' marcada como pendiente.")
                self.guardar_en_archivo()
                return

        print(f"No se encontró la tarea con título '{titulo}'.")

    def marcar_progreso(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.estado = "en progreso"
                print(f"Tarea '{titulo}' marcada como en progreso.")
                self.guardar_en_archivo()
                return

        print(f"No se encontró la tarea con título '{titulo}'.")

    def marcar_completada(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                tarea.estado = "completada"
                print(f"Tarea '{titulo}' marcada como completada.")
                self.guardar_en_archivo()
                return

        print(f"No se encontró la tarea con título '{titulo}'.")

    def mostrar_tareas(self, filtro_estado=None, fecha_maxima=None, ordenar_por=None):
        if not self.lista_tareas:
            print("No hay tareas.")
            return

        fecha_max_dt = None
        if fecha_maxima:
            try:
                fecha_max_dt = datetime.strptime(fecha_maxima, "%d-%m-%Y")
            except ValueError:
                print(" Fecha máxima inválida. Ignorando filtro de fecha.")
                fecha_max_dt = None

        tareas_filtradas = []
        for t in self.lista_tareas:
            incluir = True

            if filtro_estado and t.estado.lower() != filtro_estado.lower():
                incluir = False

            if fecha_max_dt and t.fecha_vencimiento:
                try:
                    fecha_tarea_dt = datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y")
                    if fecha_tarea_dt > fecha_max_dt:
                        incluir = False
                except ValueError:
                    incluir = False

            if incluir:
                tareas_filtradas.append(t)

        if ordenar_por == "fecha":
            tareas_filtradas.sort(key=lambda t: datetime.strptime(t.fecha_vencimiento, "%d-%m-%Y") if t.fecha_vencimiento else datetime.max)
        elif ordenar_por == "estado":
            tareas_filtradas.sort(key=lambda t: t.estado)
        elif ordenar_por == "prioridad":
            tareas_filtradas.sort(key=lambda t: {"alta": 1, "media": 2, "baja": 3}.get(t.prioridad, 2))

        print("\n=== LISTA DE TAREAS ===")
        hoy = datetime.today()

        for tarea in tareas_filtradas:
            vencida = ""
            if tarea.fecha_vencimiento:
                try:
                    fecha_tarea_dt = datetime.strptime(tarea.fecha_vencimiento, "%d-%m-%Y")
                    if fecha_tarea_dt < hoy:
                        vencida = "  VENCIDA"
                except ValueError:
                    vencida = "  Fecha inválida"

            print(f"[{tarea.estado.upper()}] {tarea.titulo} - {tarea.descripcion} (Vence: {tarea.fecha_vencimiento}) [Prioridad: {tarea.prioridad.upper()}]{vencida}")

            if tarea.subtareas:
                print("  Subtareas:")
                for idx, subtarea in enumerate(tarea.subtareas, 1):
                    print(f"    {idx}. {subtarea}")

    def guardar_en_archivo(self, archivo="data/tareas.json"):
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump([tarea.to_dict() for tarea in self.lista_tareas], f, indent=4)
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

    def editar_tarea(self, titulo):
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

    def buscar_tareas(self, palabra_clave):
        resultados = [t for t in self.lista_tareas if palabra_clave.lower() in t.titulo.lower() or palabra_clave.lower() in t.descripcion.lower()]
        if resultados:
            print("\n=== RESULTADOS DE BÚSQUEDA ===")
            for tarea in resultados:
                print(f"[{tarea.estado.upper()}] {tarea.titulo} - {tarea.descripcion} (Vence: {tarea.fecha_vencimiento})")
        else:
            print("No se encontraron tareas con esa palabra clave.")

    def agregar_subtarea(self, titulo):
        for tarea in self.lista_tareas:
            if tarea.titulo.lower() == titulo.lower():
                subtarea = input("Ingrese subtarea: ")
                tarea.subtareas.append(subtarea)
                print("Subtarea agregada.")
                self.guardar_en_archivo()
                return
        print(f"No se encontró tarea con título '{titulo}'.")

    def mostrar_proximas_tareas(self, dias=3):
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

        if proximas:
            print(f"\nEstas tareas vencen en los próximos {dias} días:")
            for t in proximas:
                print(f"[{t.estado.upper()}] {t.titulo} (Vence: {t.fecha_vencimiento})")
        else:
            print("\nNo hay tareas próximas a vencer.")

def eliminar_tarea_por_titulo(self, titulo):
    self.lista_tareas = [t for t in self.lista_tareas if t.titulo != titulo]
    self.guardar_en_archivo()
