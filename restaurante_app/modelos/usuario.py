class Usuario:
    ROLES_PERMITIDOS = ["Administrador", "Empleado", "Cliente"]

    def __init__(self, id_usuario, nombre, username, password, rol="Cliente"):
        self.id_usuario = str(id_usuario)
        self.nombre = nombre
        self.username = username
        self.password = password
        self.rol = rol if rol in self.ROLES_PERMITIDOS else "Cliente"

    def a_dict(self):
        """Convierte la entidad a un diccionario para persistencia JSON."""
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "username": self.username,
            "password": self.password,
            "rol": self.rol
        }

    @classmethod
    def desde_dict(cls, datos):
        """Crea una instancia de Usuario a partir de un diccionario."""
        return cls(
            id_usuario=datos.get("id_usuario"),
            nombre=datos.get("nombre", ""),
            username=datos.get("username", ""),
            password=datos.get("password", ""),
            rol=datos.get("rol", "Cliente")
        )

    def a_tupla_tabla(self):
        """Devuelve únicamente los datos seguros e informativos para la tabla Treeview."""
        return (self.id_usuario, self.nombre, self.username, self.rol)