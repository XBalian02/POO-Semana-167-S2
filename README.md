# Agachaditos Don Xavi UEA - Semana 16: Manejo de Eventos en Tkinter

## Descripción General
La presente actividad corresponde a la Semana 16 de la asignatura **Programación Orientada a Objetos**. En esta entrega se evidencia la evolución del proyecto **`restaurante_app`** (*Agachaditos Don Xavi UEA*), manteniendo la arquitectura modular en tres capas, la persistencia en archivos JSON y aplicando el manejo de eventos en Tkinter dentro de la gestión administrativa de usuarios.

======================================================================

## Credenciales de Acceso para Evaluación Docente
Para la comprobación del sistema y revisión de los permisos por rol, utilice las siguientes cuentas de prueba registradas en `datos/usuarios.json`:

* **Administrador (Acceso total a la Gestión de Usuarios):**
  * **Usuario:** `Xavichi`
  * **Contraseña:** `contraseñaxd`
* **Empleado / Cajero (Acceso restringido):**
  * **Usuario:** `DonCajero`
  * **Contraseña:** `contraseñacajeroxd`

======================================================================

## Estructura esperada del repositorio
Repositorio GitHub
├── restaurante_app/
│   ├── datos/
│   │   ├── productos.json
│   │   ├── usuarios.json
│   │   └── ventas.json
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── producto.py
│   │   ├── usuario.py
│   │   └── venta.py
│   ├── servicios/
│   │   ├── __init__.py
│   │   ├── archivo_servicio.py
│   │   └── restaurante_servicio.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── login_view.py
│   │   └── main_view.py
│   ├── assets/              (obligatorio: íconos, logo/logotipo y recursos visuales)
│   └── main.py
└── README.md

======================================================================

## Manejo de Eventos e Interacciones
El sistema demuestra el flujo de interacción `usuario → evento → bind() → callback → servicio → persistencia → respuesta visual` mediante la siguiente implementación:

1. **`<<TreeviewSelect>>` (`bind`)**: Al hacer clic en una fila de la tabla de usuarios, el callback captura el identificador único del registro y consulta el objeto correspondiente en `RestauranteServicio` para cargar sus datos en el formulario sin exponer contraseñas en la tabla.
2. **`<<ComboboxSelected>>` (`bind`)**: Responde de manera inmediata al cambio de selección de rol dentro del desplegable `Combobox`.
3. **`<Return>` (`bind_all`)**: Atajo de teclado que ejecuta automáticamente el método de registro de usuario cuando el formulario está activo.
4. **`<Escape>` (`bind_all`)**: Atajo de teclado para limpiar el formulario, cancelar la selección actual en el `Treeview` y devolver la interfaz a su estado inicial.
5. **Botones Principales (`command=`)**: Las operaciones de **Registrar**, **Actualizar**, **Eliminar** y **Limpiar** se mantienen vinculadas explícitamente mediante el parámetro `command=`.

======================================================================

## Control de Acceso y Reglas de Negocio
- **Control de Roles:** Únicamente los usuarios autenticados con el rol **Administrador** pueden acceder a la sección administrativa de gestión de usuarios.
- **Protección de Cuenta Activa:** Por regla de seguridad en la capa de servicio, el administrador autenticado no puede eliminar su propia cuenta en uso.
- **Persistencia Desacoplada:** La interfaz gráfica no lee ni escribe directamente en los archivos JSON; todas las validaciones y operaciones CRUD se delegan a `RestauranteServicio`.
