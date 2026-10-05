class Producto:
    def __init__(self, id_producto, nombre, precio, stock, categoria="General"):
        self.id_producto = str(id_producto)
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)
        self.categoria = categoria

    def a_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria
        }

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            id_producto=datos.get("id_producto"),
            nombre=datos.get("nombre", ""),
            precio=datos.get("precio", 0.0),
            stock=datos.get("stock", 0),
            categoria=datos.get("categoria", "General")
        )