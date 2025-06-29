# Proyecto To-Do List (Gestor de Tareas)

Este proyecto corresponde al desarrollo de un **Administrador de Tareas Personales** (To-Do List), como parte de la evaluación del curso. Es una aplicación desarrollada en **Python** que permite gestionar tareas desde dos entornos: una **interfaz web moderna con Flask** y una **interfaz de línea de comandos (terminal)**.

---

## Estudiantes

- **Ignacio León** - ignleon@alumnos.uai.cl
- **Alonso Tamayo** - atamayo@alumnos.uai.cl
- **Filomena Tejeda** - ftejeda@alumnos.uai.cl

---

## Contexto del Proyecto

Este proyecto fue desarrollado en base al [enunciado oficial del proyecto](./Enunciado_Proyecto_ToDoList.pdf), el cual establece los siguientes requisitos:

- Crear, editar y eliminar tareas
- Asignar categorías y prioridades
- Marcar tareas como completadas
- Filtrar tareas por estado y fecha
- Gestionar subtareas por cada tarea
- Visualizar tareas próximas a vencer
- Aplicar los **tres paradigmas de programación**:
  - Paradigma **Procedural**
  - Paradigma **Orientado a Objetos**
  - Paradigma **Funcional**

También se siguió la [rúbrica oficial de evaluación](./Rubrica_Proyecto_ToDoList.pdf), asegurando modularidad, claridad, documentación y uso de Git.

---

###  Idea Base: Terminal como núcleo del proyecto

La versión en terminal fue la idea original del proyecto. Este enfoque inicial sirvió como base para construir una arquitectura clara, modular y extensible.

A medida que el desarrollo avanzó, y con el objetivo de mejorar la experiencia del usuario, decidimos ampliar el proyecto incorporando una interfaz web usando Flask. Esta expansión permitió aprovechar herramientas visuales como Bootstrap, mejorar la navegación, aplicar filtros interactivos y facilitar la visualización de las tareas y subtareas, manteniendo siempre la lógica central del sistema.

Así, la terminal representa la raíz del proyecto y la interfaz web, su evolución natural.

---

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/todolist
```

2. Instala Flask (si no lo tienes):
```bash
pip install flask
```

---

## Modo Web (Flask)

Para ejecutar la aplicación web, usa:

```bash
python app.py
```

Abre tu navegador en `http://127.0.0.1:5000` y podrás:

- Ver todas tus tareas en tarjetas interactivas
- Agregar nuevas tareas y subtareas
- Editar, eliminar, y marcar tareas como completadas
- Filtrar por prioridad, estado y categoría
- Buscar tareas por palabra clave

---

## Modo Terminal

También puedes usar la aplicación desde la terminal con:

```bash
python -m terminal.main
```

Este modo permite una gestión simple basada en texto, ideal para quienes prefieren trabajar sin interfaz gráfica.

Se recomienda usar la interfaz web para una mayor experiencia de usuario, ya que ofrece una navegación más intuitiva y con mayor interactividad.

---

##  Estructura del Proyecto

```
todolist/
├── app.py                # Entrada para el servidor web
├── gestor_web.py         # Lógica web
├── terminal/             # Modo terminal
│   ├── main.py
│   └── gestor.py
├── core/                 # Modelo de tarea y validaciones
│   ├── tarea.py
│   └── validacion.py
├── templates/            # HTML con Jinja2 y Bootstrap
├── data/                 # JSON con persistencia
│   └── tareas.json
└── README.md
```

---

## Funcionalidades Implementadas

- CRUD de tareas  
- Subtareas por tarea  
- Filtros por estado, prioridad y categoría  
- Ordenamiento por fecha y estado  
- Visualización de próximas tareas  
- Almacenamiento persistente en archivo JSON  
- Búsqueda por texto  
- Interfaz responsiva (Bootstrap)  
- Estructura modular, clara y validada  

---

##  Notas Finales

El diseño de este proyecto busca demostrar el uso práctico de múltiples paradigmas de programación, la construcción de interfaces usables y la capacidad de integración entre distintos módulos y formatos de interacción.

