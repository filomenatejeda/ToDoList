# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

# Se importa las clases necesarias para el desarrollo de la aplicación
from gestor_web import GestorTareasWeb
from core.tarea import Tarea

# Se importa las funciones de validación para asegurar que los datos ingresados sean correctos
from core.validacion import validar_titulo, validar_fecha, formatear_fecha


# Se crea una instancia de la clase Flask y se asigna el nombre de la aplicación
app = Flask(__name__)
# Se crea una instancia de la clase GestorTareasWeb y se carga la lista de tareas desde un archivo JSON 
gestor = GestorTareasWeb()
gestor.cargar_desde_archivo()

# Se define la ruta de la página principal
@app.route("/")
# Se define la función para mostrar el menú principal
def menu():
    return render_template("menu.html")

# Se define la ruta para mostrar las tareas
@app.route("/tareas")
# Se define la función para mostrar las tareas
def ver_tareas():
    filtro_estado = request.args.get("estado")
    fecha_maxima = request.args.get("fecha_maxima")
    ordenar_por = request.args.get("ordenar_por")

    tareas = gestor.obtener_tareas_filtradas(filtro_estado, fecha_maxima, ordenar_por)
    # Se muestra la página de tareas
    return render_template("tareas.html", tareas=tareas)

# Se define la ruta para agregar una tarea
@app.route("/agregar", methods=["GET", "POST"])
# Se define la función para agregar una tarea
def agregar_tarea():
    titulo = ""
    descripcion = ""
    fecha = ""
    prioridad = "media"
    categoria = ""

    # Se verifica si se envió datos en el método POST
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        fecha = request.form.get("fecha")
        prioridad = request.form.get("prioridad", "media")
        categoria = request.form.get("categoria", "")

        # Se verifica si el título es válido
        if not validar_titulo(titulo):
            return render_template("agregar.html", 
                error="Título inválido.",
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha,
                prioridad=prioridad
        )

        # Se verifica si la fecha es válida
        if not validar_fecha(fecha):
            return render_template("agregar.html", 
                error="Fecha inválida. Debe ser formato dd-mm-aaaa.",
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha,
                prioridad=prioridad
        )

    # Se formatea la fecha ingresada para que sea compatible con el formato de la clase Tarea
        fecha_formateada = formatear_fecha(fecha)

    # Se crea una nueva tarea con los datos ingresados
        tarea = Tarea(titulo, descripcion, "pendiente", datetime.today().strftime("%d-%m-%Y"), None, fecha_formateada, prioridad, categoria=categoria)
        gestor.agregar_tarea(tarea)
        return redirect(url_for("ver_tareas"))

    # Se muestra la página de agregar tarea
    return render_template("agregar.html",
        titulo=titulo,
        descripcion=descripcion,
        fecha=fecha,
        prioridad=prioridad,
        categoria=categoria
    )


# Se define la ruta para eliminar una tarea
@app.route("/eliminar/<int:indice>")
# Se define la función para eliminar una tarea
def eliminar_tarea(indice):
    gestor.eliminar_tarea(indice)
    return redirect(url_for("ver_tareas"))

# Se define la ruta para eliminar una tarea a través de la búsqueda
@app.route("/eliminar_tarea_buscar/<int:indice>")
# Se define la función para eliminar una tarea a través de la búsqueda
def eliminar_tarea_buscar(indice):
    gestor.eliminar_tarea(indice)
    return redirect(url_for("buscar_tareas"))

# Se define la ruta para marcar una tarea como pendiente
@app.route("/marcar_pendiente/<int:indice>")
# Se define la función para marcar una tarea como pendiente
def marcar_pendiente(indice):
    gestor.marcar_pendiente(indice)
    return redirect(url_for("ver_tareas"))

# Se define la ruta para marcar una tarea como en progreso
@app.route("/marcar_progreso/<int:indice>")
# Se define la función para marcar una tarea como en progreso
def marcar_progreso(indice):
    gestor.marcar_progreso(indice)
    return redirect(url_for("ver_tareas"))

# Se define la ruta para marcar una tarea como completada
@app.route("/marcar_completada/<int:indice>")
# Se define la función para marcar una tarea como completada
def marcar_completada(indice):
    gestor.marcar_completada(indice)
    return redirect(url_for("ver_tareas"))

# Se define la ruta para marcar una tarea como pendiente a través de la búsqueda
@app.route("/marcar_pendiente_buscar/<int:indice>")
# Se define la función para marcar una tarea como pendiente a través de la búsqueda
def marcar_pendiente_buscar(indice):
    gestor.marcar_pendiente(indice)
    return redirect(url_for("buscar_tareas"))

# Se define la ruta para marcar una tarea como en progreso a través de la búsqueda
@app.route("/marcar_progreso_buscar/<int:indice>")
# Se define la función para marcar una tarea como en progreso a través de la búsqueda
def marcar_progreso_buscar(indice):
    gestor.marcar_progreso(indice)
    return redirect(url_for("buscar_tareas"))

# Se define la ruta para marcar una tarea como completada a través de la búsqueda
@app.route("/marcar_completada_buscar/<int:indice>")
# Se define la función para marcar una tarea como completada a través de la búsqueda
def marcar_completada_buscar(indice):
    gestor.marcar_completada(indice)
    return redirect(url_for("buscar_tareas"))

# Se define la ruta para editar una tarea
@app.route("/editar/<int:indice>", methods=["GET", "POST"])
# Se define la función para editar una tarea
def editar_tarea(indice):
    tarea = gestor.lista_tareas[indice]
    # Se verifica si se envió datos en el método POST
    if request.method == "POST":
        nuevo_titulo = request.form.get("titulo")
        nueva_desc = request.form.get("descripcion")
        nueva_fecha = request.form.get("fecha")
        nueva_prioridad = request.form.get("prioridad", "media")
        nueva_categoria = request.form.get("categoria", "")

        # Se muestra la página de editar tarea
        gestor.editar_tarea(indice, nuevo_titulo, nueva_desc, nueva_fecha, nueva_prioridad, nueva_categoria)
        # Se redirige a la página de tareas después de editar
        return redirect(url_for("ver_tareas"))
    
    # Se muestra la página de editar tarea
    return render_template("editar.html", tarea=tarea, indice=indice, origen="tareas")

# Se define la ruta para editar una tarea a través de la búsqueda
@app.route("/editar_tarea_buscar/<int:indice>", methods=["GET", "POST"])
# Se define la función para editar una tarea a través de la búsqueda
def editar_tarea_buscar(indice):
    tarea = gestor.lista_tareas[indice]
    # Se verifica si se envió datos en el método POST
    if request.method == "POST":
        nuevo_titulo = request.form.get("titulo")
        nueva_desc = request.form.get("descripcion")
        nueva_fecha = request.form.get("fecha")
        nueva_prioridad = request.form.get("prioridad", "media")
        nueva_categoria = request.form.get("categoria", "")

        # Se muestra la página de editar tarea a través de la búsqueda
        gestor.editar_tarea(indice, nuevo_titulo, nueva_desc, nueva_fecha, nueva_prioridad, nueva_categoria)
        # Se redirige a la página de búsqueda después de editar
        return redirect(url_for("buscar_tareas"))

    # Se muestra la página de editar tarea a través de la búsqueda
    return render_template("editar.html", tarea=tarea, indice=indice, origen="buscar")

# Se define la ruta para buscar las tareas
@app.route("/buscar", methods=["GET", "POST"])
# Se define la función para buscar las tareas
def buscar_tareas():
    # Se obtiene los datos de la búsqueda
    texto = ""
    estado_seleccionado = ""
    prioridad_seleccionada = ""

    if request.method == "POST":
        texto = request.form.get("texto", "")
        estado_seleccionado = request.form.get("estado", "")
        prioridad_seleccionada = request.form.get("prioridad", "")

        # Se verifica si se ingresó un texto para buscar
        resultados = gestor.buscar_tareas_avanzada(texto, estado_seleccionado, prioridad_seleccionada)

    else:  # Si es GET → mostrar todas las tareas
        resultados = gestor.lista_tareas

    # Se muestra la página de búsqueda con los resultados obtenidos
    return render_template("buscar.html", 
        resultados=resultados, 
        texto=texto, 
        estado_seleccionado=estado_seleccionado, 
        prioridad_seleccionada=prioridad_seleccionada
    )

# Se define la ruta para agregar una subtarea a una tarea existente
@app.route("/agregar_subtarea/<int:indice>", methods=["GET", "POST"])
# Se define la función para agregar una subtarea a una tarea existente
def agregar_subtarea(indice):
    if 0 <= indice < len(gestor.lista_tareas):
        tarea = gestor.lista_tareas[indice]

        if request.method == "POST":
            subtarea_texto = request.form.get("subtarea")
            gestor.agregar_subtarea(indice, subtarea_texto)
            # Se redirige a la página de tareas después de agregar la subtarea
            return redirect(url_for("ver_tareas"))

        # Se muestra la página de agregar subtarea
        return render_template("agregar_subtarea.html", tarea=tarea, origen="tareas")

    # Si el índice es inválido, se redirige a la página de tareas
    return redirect(url_for("ver_tareas"))

# Se define la ruta para agregar una subtarea a una tarea existente a través de la búsqueda
@app.route("/agregar_subtarea_buscar/<int:indice>", methods=["GET", "POST"])
# Se define la función para agregar una subtarea a una tarea existente a través de la búsqueda
def agregar_subtarea_buscar(indice):
    if 0 <= indice < len(gestor.lista_tareas):
        tarea = gestor.lista_tareas[indice]

        if request.method == "POST":
            subtarea_texto = request.form.get("subtarea")
            gestor.agregar_subtarea(indice, subtarea_texto)
            # Se redirige a la página de búsqueda después de agregar la subtarea
            return redirect(url_for("buscar_tareas"))

        # Se muestra la página de agregar subtarea a través de la búsqueda
        return render_template("agregar_subtarea.html", tarea=tarea, origen="buscar")

    # Si el índice es inválido, se redirige a la página de búsqueda
    return redirect(url_for("buscar_tareas"))


# Se define la ruta para mostrar las próximas tareas que vencen en un plazo determinado de días
@app.route("/proximas")
# Se define la función para mostrar las próximas tareas que vencen en un plazo determinado de días
def proximas_tareas():
    tareas = gestor.obtener_proximas_tareas()
    # Se muestra la página de próximas tareas
    return render_template("proximas.html", tareas=tareas)

# Se define la ruta para alternar la completación de una subtarea
@app.route("/toggle_subtarea/<int:tarea_idx>/<int:subtarea_idx>", methods=["POST"])
# Se define la función para alternar la completación de una subtarea
def toggle_subtarea(tarea_idx, subtarea_idx):
    t = gestor.lista_tareas[tarea_idx]
    subt = t.subtareas[subtarea_idx]
    subt["completada"] = not subt["completada"]
    
    if all(s["completada"] for s in t.subtareas):
        gestor.marcar_completada(tarea_idx)
    elif any(s["completada"] for s in t.subtareas):
        gestor.marcar_progreso(tarea_idx)
    else:
        gestor.marcar_pendiente(tarea_idx)
    
    return jsonify({
        "nuevo_estado": t.estado,
        "indice": tarea_idx
    })


# Se define la ruta para ver las estadísticas de las tareas
@app.route("/estadisticas")
# Se define la función para ver las estadísticas de las tareas
def ver_estadisticas():
    # Se obtienen las cantidades de tareas por estado
    cantidades_tareas = [len(lista_tareas) for lista_tareas in gestor.obtener_tareas_por_estado()]
    suma = sum(cantidades_tareas)

    # Se verifica si hay tareas para mostrar las estadísticas
    hay_tareas = suma > 0

    # Se calcula el porcentaje de tareas por estado y se crea un conjunto con los nombres, cantidades y porcentajes
    nombres_estados = ["completadas", "en progreso", "pendientes"]
    porcentajes_tareas = [round((cantidad_tareas / suma) * 100, 1) for cantidad_tareas in cantidades_tareas]
    conjunto_porcentajes_tareas = [[nombres_estados[i], cantidades_tareas[i], porcentajes_tareas[i]] for i in range(len(nombres_estados))]

    # Se obtienen las cantidades de tareas completadas en los últimos días
    cantidades_ultimas_tareas_completadas = [[i, len(gestor.obtener_ultimas_tareas_completadas(dias=i))] for i in [0, 1, 7, 30]]


    # Se muestra la página de estadísticas con los datos obtenidos
    return render_template("estadisticas.html",
        hay_tareas=hay_tareas,
        conjunto_porcentajes_tareas=conjunto_porcentajes_tareas,
        cantidades_ultimas_tareas_completadas=cantidades_ultimas_tareas_completadas
    )


# Se ejecuta el servidor web
if __name__ == "__main__":
    app.run(debug=True)