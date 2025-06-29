class Tarea:  # Se define la clase Tarea
    # Se define el constructor de la clase Tarea con los atributos necesarios para una tarea, iniciando la tarea como pendiente y con prioridad media
    def __init__(self, titulo, descripcion, estado="pendiente", fecha_vencimiento=None, prioridad="media", subtareas=None): 
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_vencimiento = fecha_vencimiento
        self.prioridad = prioridad
        # Subtareas: lista de dicts: {"nombre": str, "completada": bool}
        self.subtareas = subtareas if subtareas is not None else []

    # Se define el método to_dict para convertir la clase a un diccionario
    def to_dict(self):  
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_vencimiento": self.fecha_vencimiento,
            "prioridad": self.prioridad,
            "subtareas": self.subtareas
        }

    # Se define un método estático de clase Tarea para crear una tarea a partir de un diccionario
    @staticmethod
    def from_dict(data):  
        return Tarea(
            titulo=data["titulo"],
            descripcion=data["descripcion"],
            estado=data.get("estado", "pendiente"),
            fecha_vencimiento=data.get("fecha_vencimiento"),
            prioridad=data.get("prioridad", "media"),
            subtareas=data.get("subtareas", [])
        )
