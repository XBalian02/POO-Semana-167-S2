import uuid
from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    """Servicio principal que coordina las reglas de negocio y la persistencia de datos."""
    def __init__(self, ruta_usuarios="datos/usuarios.json", 
                 ruta_productos="datos/productos.json", 
                 ruta_ventas="datos/ventas.json"):
        self.archivo_usuarios = ArchivoServicio(ruta_usuarios)
        self.archivo_productos = ArchivoServicio(ruta_productos)
        self.archivo_ventas = ArchivoServicio(ruta_ventas)
        self.usuario_autenticado = None

    # --- AUTENTICACIÓN ---
    def autenticar(self, username, password):
        usuarios_data = self.archivo_usuarios.cargar()
        for u in usuarios_data:
            if u.get("username") == username and u.get("password") == password:
                self.usuario_autenticado = Usuario.desde_dict(u)
                return self.usuario_autenticado
        return None

    # --- CRUD USUARIOS CON REGLAS DE NEGOCIO ---
    def obtener_todos_usuarios(self):
        data = self.archivo_usuarios.cargar()
        return [Usuario.desde_dict(item) for item in data]

    def obtener_usuario_por_id(self, id_usuario):
        for usuario in self.obtener_todos_usuarios():
            if usuario.id_usuario == str(id_usuario):
                return usuario
        return None

    def registrar_usuario(self, nombre, username, password, rol):
        if not nombre.strip() or not username.strip() or not password.strip():
            raise ValueError("Todos los campos (Nombre, Usuario y Contraseña) son obligatorios.")

        usuarios = self.obtener_todos_usuarios()
        if any(u.username.lower() == username.strip().lower() for u in usuarios):
            raise ValueError(f"El usuario '{username}' ya existe. Elija otro nombre de usuario.")

        nuevo_id = str(uuid.uuid4())[:8]
        nuevo_usuario = Usuario(nuevo_id, nombre.strip(), username.strip(), password.strip(), rol)
        usuarios.append(nuevo_usuario)

        self.archivo_usuarios.guardar([u.a_dict() for u in usuarios])
        return nuevo_usuario

    def actualizar_usuario(self, id_usuario, nombre, username, password, rol):
        if not nombre.strip() or not username.strip():
            raise ValueError("El nombre y el usuario no pueden estar vacíos.")

        usuarios = self.obtener_todos_usuarios()
        encontrado = False

        for i, u in enumerate(usuarios):
            if u.id_usuario == str(id_usuario):
                # Si no se ingresa nueva contraseña, se conserva la actual
                pwd_final = password.strip() if password.strip() else u.password
                usuarios[i] = Usuario(id_usuario, nombre.strip(), username.strip(), pwd_final, rol)
                encontrado = True
                break

        if not encontrado:
            raise ValueError("El usuario seleccionado no existe en el sistema.")

        self.archivo_usuarios.guardar([u.a_dict() for u in usuarios])

    def eliminar_usuario(self, id_usuario):
        if self.usuario_autenticado and self.usuario_autenticado.id_usuario == str(id_usuario):
            raise ValueError("Seguridad: No puede eliminar la cuenta con la que está actualmente autenticado.")

        usuarios = self.obtener_todos_usuarios()
        usuarios_filtrados = [u for u in usuarios if u.id_usuario != str(id_usuario)]

        if len(usuarios) == len(usuarios_filtrados):
            raise ValueError("El usuario a eliminar no existe.")

        self.archivo_usuarios.guardar([u.a_dict() for u in usuarios_filtrados])

    # --- CONSULTA DE PRODUCTOS Y VENTAS ---
    def obtener_todos_productos(self):
        return [Producto.desde_dict(item) for item in self.archivo_productos.cargar()]

    def obtener_todas_ventas(self):
        return [Venta.desde_dict(item) for item in self.archivo_ventas.cargar()]