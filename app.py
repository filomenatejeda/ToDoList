# app.py

from flask import Flask, render_template, request, redirect, url_for
from gestor_web import GestorTareasWeb
from core.tarea import Tarea
from core.validacion import validar_titulo, validar_fecha, formatear_fecha


app = Flask(__name__)
gestor = GestorTareasWeb()
gestor.cargar_desde_archivo()

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/tareas")
def ver_tareas():
    filtro_estado = request.args.get("estado")
    fecha_maxima = request.args.get("fecha_maxima")
    ordenar_por = request.args.get("ordenar_por")

    tareas = gestor.obtener_tareas_filtradas(filtro_estado, fecha_maxima, ordenar_por)
    return render_template("tareas.html", tareas=tareas)

@app.route("/agregar", methods=["GET", "POST"])
def agregar_tarea():
    titulo = ""
    descripcion = ""
    fecha = ""
    prioridad = "media"

    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        fecha = request.form.get("fecha")
        prioridad = request.form.get("prioridad", "media")

        if not validar_titulo(titulo):
            return render_template("agregar.html", 
                error="Título inválido.",
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha,
                prioridad=prioridad
        )

        if not validar_fecha(fecha):
            return render_template("agregar.html", 
                error="Fecha inválida. Debe ser formato dd-mm-aaaa.",
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha,
                prioridad=prioridad
        )

    # ✅ FORMATEAR:
        fecha_formateada = formatear_fecha(fecha)

    # Crear tarea:
        tarea = Tarea(titulo, descripcion, "pendiente", fecha_formateada, prioridad)
        gestor.agregar_tarea(tarea)
        return redirect(url_for("ver_tareas"))


    return render_template("agregar.html",
        titulo=titulo,
        descripcion=descripcion,
        fecha=fecha,
        prioridad=prioridad
    )



@app.route("/eliminar/<int:indice>")
def eliminar_tarea(indice):
    gestor.eliminar_tarea(indice)
    return redirect(url_for("ver_tareas"))

@app.route("/marcar_completada/<int:indice>")
def marcar_completada(indice):
    gestor.marcar_completada(indice)
    return redirect(url_for("ver_tareas"))

@app.route("/cambiar_estado/<int:indice>")
def cambiar_estado(indice):
    gestor.cambiar_estado_tarea(indice)
    return redirect(url_for("ver_tareas"))

@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar_tarea(indice):
    tarea = gestor.lista_tareas[indice]
    if request.method == "POST":
        nuevo_titulo = request.form.get("titulo")
        nueva_desc = request.form.get("descripcion")
        nueva_fecha = request.form.get("fecha")
        nueva_prioridad = request.form.get("prioridad", "media")

        gestor.editar_tarea(indice, nuevo_titulo, nueva_desc, nueva_fecha, nueva_prioridad)
        return redirect(url_for("ver_tareas"))

    return render_template("editar.html", tarea=tarea, indice=indice)

@app.route("/buscar", methods=["GET", "POST"])
def buscar_tareas():
    texto = ""
    estado_seleccionado = ""
    prioridad_seleccionada = ""

    if request.method == "POST":
        texto = request.form.get("texto", "")
        estado_seleccionado = request.form.get("estado", "")
        prioridad_seleccionada = request.form.get("prioridad", "")

        resultados = gestor.buscar_tareas_avanzada(texto, estado_seleccionado, prioridad_seleccionada)

    else:  # Si es GET → mostrar todas las tareas
        resultados = gestor.lista_tareas

    return render_template("buscar.html", 
        resultados=resultados, 
        texto=texto, 
        estado_seleccionado=estado_seleccionado, 
        prioridad_seleccionada=prioridad_seleccionada
    )



@app.route("/agregar_subtarea/<int:indice>", methods=["GET", "POST"])
def agregar_subtarea(indice):
    if 0 <= indice < len(gestor.lista_tareas):
        tarea = gestor.lista_tareas[indice]

        if request.method == "POST":
            subtarea_texto = request.form.get("subtarea")
            gestor.agregar_subtarea(indice, subtarea_texto)
            return redirect(url_for("ver_tareas"))

        return render_template("agregar_subtarea.html", tarea=tarea)

    return redirect(url_for("ver_tareas"))


@app.route("/proximas")
def proximas_tareas():
    tareas = gestor.obtener_proximas_tareas()
    return render_template("proximas.html", tareas=tareas)

@app.route("/toggle_subtarea/<int:tarea_idx>/<int:subtarea_idx>", methods=["POST"])
def toggle_subtarea(tarea_idx, subtarea_idx):
    t = gestor.lista_tareas[tarea_idx]
    subt = t.subtareas[subtarea_idx]
    subt["completada"] = not subt["completada"]
    gestor.guardar_en_archivo()
    return redirect(url_for('ver_tareas'))


if __name__ == "__main__":
    app.run(debug=True)
