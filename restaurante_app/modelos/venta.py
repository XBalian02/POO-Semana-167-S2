class Venta:
    def __init__(self, id_venta, usuario_id, total, fecha, items=None):
        self.id_venta = str(id_venta)
        self.usuario_id = str(usuario_id)
        self.total = float(total)
        self.fecha = fecha
        self.items = items if items else []

    def a_dict(self):
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "total": self.total,
            "fecha": self.fecha,
            "items": self.items
        }

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            id_venta=datos.get("id_venta"),
            usuario_id=datos.get("usuario_id"),
            total=datos.get("total", 0.0),
            fecha=datos.get("fecha", ""),
            items=datos.get("items", [])
        )