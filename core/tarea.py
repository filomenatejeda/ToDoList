class Tarea:
    def __init__(self, titulo, descripcion, estado="pendiente", fecha_vencimiento=None, prioridad="media", subtareas=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.fecha_vencimiento = fecha_vencimiento
        self.prioridad = prioridad
        # Subtareas: lista de dicts: {"nombre": str, "completada": bool}
        self.subtareas = subtareas if subtareas is not None else []

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_vencimiento": self.fecha_vencimiento,
            "prioridad": self.prioridad,
            "subtareas": self.subtareas
        }

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
