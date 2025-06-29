# main.py
# Se importa la clase GestorTareas y Tarea para gestionar las tareas y sus operaciones.
# También se importan funciones de validación para asegurar que los datos ingresados sean correctos
from terminal.gestor import GestorTareas
from core.tarea import Tarea
from core.validacion import validar_titulo, validar_fecha

# Se define la función para mostrar el menú principal del programa
def mostrar_menu():
    print("\n=== MENÚ TO-DO LIST ===")
    print("1. Agregar tarea")
    print("2. Eliminar tarea")
    print("3. Marcar como completada")
    print("4. Mostrar tareas")
    print("5. Editar tarea")
    print("6. Cambiar estado de tarea")
    print("7. Buscar tareas")
    print("8. Agregar subtarea")
    print("9. Mostrar próximas tareas")
    print("0. Salir")

# Se define la función principal del programa
def main():
    # Se crea un objeto GestorTareas para gestionar las tareas y se carga la lista de tareas desde un archivo
    gestor = GestorTareas()
    gestor.cargar_desde_archivo()

    # Se muestra la lista de tareas próximas a vencer
    print("\n Bienvenida a tu TO-DO LIST!")
    gestor.mostrar_proximas_tareas()

    # Se ejecuta un bucle infinito para mostrar el menú principal y realizar operaciones
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        # Agrega una tarea nueva
        if opcion == "1":
            while True:
                titulo = input("Título: ")
                if validar_titulo(titulo):
                    break
                else:
                    print("El título no puede estar vacío.")

            descripcion = input("Descripción: ")

            # Se solicita la fecha de vencimiento de la tarea
            while True:
                fecha = input("Fecha de vencimiento (dd-mm-aaaa) o enter: ")
                if validar_fecha(fecha):
                    break
                else:
                    print("Fecha inválida. Formato correcto: dd-mm-aaaa.")

            # Se solicita la prioridad de la tarea
            prioridad = input("Prioridad (alta / media / baja): ").strip().lower()
            if prioridad not in ["alta", "media", "baja"]:
                prioridad = "media"

            # Se crea una nueva tarea con los datos solicitados
            tarea = Tarea(titulo, descripcion, "pendiente", fecha, prioridad)
            gestor.agregar_tarea(tarea)
            print("Tarea agregada.")

        # Elimina una tarea
        elif opcion == "2":
            gestor.eliminar_tarea()

        # Marca una tarea como completada según su título
        elif opcion == "3":
            titulo = input("Título de la tarea a marcar completada: ")
            gestor.marcar_completada(titulo)

        # Mostrar las tareas según los filtros y ordenamientos seleccionados
        elif opcion == "4":
            filtro = input("Filtrar por estado (pendiente, en progreso, completada) o enter para ver todas: ")
            fecha = input("Mostrar solo tareas con vencimiento hasta (dd-mm-aaaa) o enter para todas: ")
            orden = input("Ordenar por (fecha / estado / prioridad) o enter para no ordenar: ")

            gestor.mostrar_tareas(filtro_estado=filtro if filtro else None,
                                  fecha_maxima=fecha if fecha else None,
                                  ordenar_por=orden if orden else None)

        # Edita una tarea según su título
        elif opcion == "5":
            titulo = input("Título de la tarea a editar: ")
            gestor.editar_tarea(titulo)

        # Cambia el estado de una tarea según su título
        elif opcion == "6":
            titulo = input("Título de la tarea a cambiar estado: ")
            gestor.cambiar_estado_tarea(titulo)

        # Busca las tareas según una palabra clave
        elif opcion == "7":
            palabra = input("Ingrese palabra a buscar: ")
            gestor.buscar_tareas(palabra)

        # Agrega una subtarea a una tarea según su título
        elif opcion == "8":
            titulo = input("Título de la tarea a la cual agregar subtarea: ")
            gestor.agregar_subtarea(titulo)

        # Mostrar las próximas tareas según el número de días
        elif opcion == "9":
            try:
                dias = int(input("¿Mostrar tareas que vencen en cuántos días? (default 3): ") or "3")
            except ValueError:
                dias = 3
            gestor.mostrar_proximas_tareas(dias)

        # Salir del programa y guardar las tareas en el archivo
        elif opcion == "0":
            print("¡Adiós! Tareas guardadas.")
            gestor.guardar_en_archivo()
            break

        # Si la opción no es válida, se muestra un mensaje de error
        else:
            print("Opción no válida. Intente nuevamente.")

# Se ejecuta el programa principal
if __name__ == "__main__":
    main()
