import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class MainView(tk.Tk):
    def __init__(self, servicio, usuario_actual):
        super().__init__()
        self.servicio = servicio
        self.usuario_actual = usuario_actual

        self.title("Agachaditos Don Xavi UEA - Gestión Principal")
        self.geometry("1024x660")
        self.minsize(920, 580)

        # Fondo general negro profundo
        self.configure(bg="#0d0d0d")

        self.logo_img = None 
        self.usuario_seleccionado_id = None

        # Tema Neón
        self._aplicar_tema_neon()
        self._construir_interfaz()

    def _aplicar_tema_neon(self):
        """Aplica una paleta de colores estilo Dark Neón."""
        style = ttk.Style(self)
        style.theme_use("clam")

        # Paleta Neón
        BG_DARK = "#0d0d0d"       # Negro de fondo general
        BG_PANEL = "#16161a"      # Negro panel
        BG_INPUT = "#22222a"      # Fondo entradas
        TEXT_WHITE = "#ffffff"    # Texto puro
        NEON_GREEN = "#00ffcc"    # Verde/Turquesa Neón (Resaltado principal)
        NEON_PINK = "#ff0055"     # Rosa Neón (Botones y alertas)
        NEON_PINK_HOVER = "#cc0044"

        # Estilo general
        style.configure(".", background=BG_DARK, foreground=TEXT_WHITE, font=("Segoe UI", 10))
        style.configure("TFrame", background=BG_DARK)
        
        # Tipografía de la marca y usuario
        style.configure("TLabel", background=BG_DARK, foreground=TEXT_WHITE)
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=NEON_GREEN)
        style.configure("User.TLabel", font=("Segoe UI", 9, "italic"), foreground="#888899")

        # Contenedores / Paneles
        style.configure("TLabelframe", background=BG_PANEL, bordercolor=NEON_GREEN, relief="solid", borderwidth=1)
        style.configure("TLabelframe.Label", background=BG_PANEL, foreground=NEON_GREEN, font=("Segoe UI", 10, "bold"))

        # Entradas de texto y combos
        style.configure("TEntry", fieldbackground=BG_INPUT, foreground=TEXT_WHITE, bordercolor=NEON_GREEN, insertcolor=NEON_GREEN)
        style.configure("TCombobox", fieldbackground=BG_INPUT, background=BG_PANEL, foreground=TEXT_WHITE, arrowcolor=NEON_GREEN)
        style.map("TCombobox", fieldbackground=[("readonly", BG_INPUT)], foreground=[("readonly", TEXT_WHITE)])

        # Botones Neón
        style.configure("TButton", background=NEON_PINK, foreground=TEXT_WHITE, borderwidth=0, font=("Segoe UI", 9, "bold"), padding=6)
        style.map("TButton", background=[("active", NEON_PINK_HOVER)])

        # Pestañas (Notebook)
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_PANEL, foreground="#888899", padding=[14, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", NEON_GREEN)], foreground=[("selected", "#000000")])

        # Tabla (Treeview)
        style.configure("Treeview", background=BG_PANEL, fieldbackground=BG_PANEL, foreground=TEXT_WHITE, rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background=BG_INPUT, foreground=NEON_GREEN, font=("Segoe UI", 9, "bold"), borderwidth=1)
        style.map("Treeview", background=[("selected", NEON_GREEN)], foreground=[("selected", "#000000")])
        style.map("Treeview.Heading", background=[("active", NEON_GREEN)], foreground=[("active", "#000000")])

    def _construir_interfaz(self):
        # Cabecera
        frame_top = ttk.Frame(self, padding=12)
        frame_top.pack(fill="x")

        # Carga del logo
        ruta_logo = os.path.join("assets", "logo.png")
        if os.path.exists(ruta_logo):
            try:
                imagen_original = Image.open(ruta_logo)
                imagen_resaltada = imagen_original.resize((38, 38), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(imagen_resaltada)

                lbl_logo = ttk.Label(frame_top, image=self.logo_img)
                lbl_logo.pack(side="left", padx=(0, 10))
            except Exception as e:
                print(f"[Aviso Visual]: No se pudo cargar el logo: {e}")

        # Nombre personalizado
        lbl_brand = ttk.Label(frame_top, text="Agachaditos Don Xavi UEA", style="Header.TLabel")
        lbl_brand.pack(side="left")

        user_info = f"Usuario: {self.usuario_actual.nombre}  |  Rol: {self.usuario_actual.rol}"
        lbl_user = ttk.Label(frame_top, text=user_info, style="User.TLabel")
        lbl_user.pack(side="right")

        # Contenedor de Pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Pestañas
        self.frame_ventas = ttk.Frame(self.notebook, padding=12)
        self.frame_productos = ttk.Frame(self.notebook, padding=12)
        
        self.notebook.add(self.frame_ventas, text=" Ventas ")
        self.notebook.add(self.frame_productos, text=" Menú / Productos ")

        self._construir_pestana_ventas()
        self._construir_pestana_productos()

        # Pestaña Exclusiva de Usuarios
        if self.usuario_actual.rol == "Administrador":
            self.frame_usuarios = ttk.Frame(self.notebook, padding=12)
            self.notebook.add(self.frame_usuarios, text=" Gestión de Usuarios ")
            self._construir_pestana_usuarios()

    def _construir_pestana_ventas(self):
        ttk.Label(self.frame_ventas, text="Módulo de Ventas y Facturación", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        tree = ttk.Treeview(self.frame_ventas, columns=("id", "usuario", "total", "fecha"), show="headings")
        tree.heading("id", text="ID Venta")
        tree.heading("usuario", text="ID Cliente")
        tree.heading("total", text="Total ($)")
        tree.heading("fecha", text="Fecha")
        tree.pack(fill="both", expand=True)

        for v in self.servicio.obtener_todas_ventas():
            tree.insert("", "end", values=(v.id_venta, v.usuario_id, f"${v.total:.2f}", v.fecha))

    def _construir_pestana_productos(self):
        ttk.Label(self.frame_productos, text="Catálogo de Platos y Bebidas", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        tree = ttk.Treeview(self.frame_productos, columns=("id", "nombre", "precio", "stock"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Producto")
        tree.heading("precio", text="Precio ($)")
        tree.heading("stock", text="Stock")
        tree.pack(fill="both", expand=True)

        for p in self.servicio.obtener_todos_productos():
            tree.insert("", "end", values=(p.id_producto, p.nombre, f"${p.precio:.2f}", p.stock))

    def _construir_pestana_usuarios(self):
        # Panel Izquierdo: Formulario
        frame_form = ttk.LabelFrame(self.frame_usuarios, text=" Formulario de Usuario ", padding=15)
        frame_form.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(frame_form, text="Nombre Completo:").grid(row=0, column=0, sticky="w", pady=6)
        self.ent_nombre = ttk.Entry(frame_form, width=26)
        self.ent_nombre.grid(row=0, column=1, pady=6)

        ttk.Label(frame_form, text="Nombre de Usuario:").grid(row=1, column=0, sticky="w", pady=6)
        self.ent_username = ttk.Entry(frame_form, width=26)
        self.ent_username.grid(row=1, column=1, pady=6)

        ttk.Label(frame_form, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=6)
        self.ent_password = ttk.Entry(frame_form, show="*", width=26)
        self.ent_password.grid(row=2, column=1, pady=6)

        ttk.Label(frame_form, text="Rol Asignado:").grid(row=3, column=0, sticky="w", pady=6)
        self.cmb_rol = ttk.Combobox(frame_form, values=["Administrador", "Empleado", "Cliente"], state="readonly", width=24)
        self.cmb_rol.current(1)
        self.cmb_rol.grid(row=3, column=1, pady=6)

        # Botones Principales (command=)
        frame_acciones = ttk.Frame(frame_form)
        frame_acciones.grid(row=4, column=0, columnspan=2, pady=18)

        btn_registrar = ttk.Button(frame_acciones, text="Registrar", command=self._accion_registrar)
        btn_registrar.grid(row=0, column=0, padx=3, pady=3)

        btn_actualizar = ttk.Button(frame_acciones, text="Actualizar", command=self._accion_actualizar)
        btn_actualizar.grid(row=0, column=1, padx=3, pady=3)

        btn_eliminar = ttk.Button(frame_acciones, text="Eliminar", command=self._accion_eliminar)
        btn_eliminar.grid(row=1, column=0, padx=3, pady=3)

        btn_limpiar = ttk.Button(frame_acciones, text="Limpiar", command=self._accion_limpiar)
        btn_limpiar.grid(row=1, column=1, padx=3, pady=3)

        # Panel Derecho: Tabla Treeview
        frame_tabla = ttk.LabelFrame(self.frame_usuarios, text=" Usuarios Registrados ", padding=10)
        frame_tabla.pack(side="right", fill="both", expand=True)

        cols = ("id", "nombre", "username", "rol")
        self.tree_usuarios = ttk.Treeview(frame_tabla, columns=cols, show="headings", selectmode="browse")

        self.tree_usuarios.heading("id", text="ID")
        self.tree_usuarios.heading("nombre", text="Nombre Completo")
        self.tree_usuarios.heading("username", text="Usuario")
        self.tree_usuarios.heading("rol", text="Rol")

        self.tree_usuarios.column("id", width=70, anchor="center")
        self.tree_usuarios.column("nombre", width=160)
        self.tree_usuarios.column("username", width=110)
        self.tree_usuarios.column("rol", width=100, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscroll=scroll.set)

        self.tree_usuarios.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # EVENTOS (bind) - Requisitos Semana 16
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.cmb_rol.bind("<<ComboboxSelected>>", self._on_combobox_rol_changed)
        self.bind_all("<Return>", self._on_tecla_enter)
        self.bind_all("<Escape>", self._on_tecla_escape)

        self._cargar_tabla_usuarios()

    # --- MÉTODOS DE APOYO ---
    def _cargar_tabla_usuarios(self):
        for row in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(row)
        for u in self.servicio.obtener_todos_usuarios():
            self.tree_usuarios.insert("", "end", iid=u.id_usuario, values=u.a_tupla_tabla())

    def _limpiar_formulario(self):
        self.usuario_seleccionado_id = None
        self.ent_nombre.delete(0, tk.END)
        self.ent_username.delete(0, tk.END)
        self.ent_password.delete(0, tk.END)
        self.cmb_rol.current(1)
        if self.tree_usuarios.selection():
            self.tree_usuarios.selection_remove(self.tree_usuarios.selection())

    # --- CALLBACKS DE EVENTOS ---
    def _on_tree_select(self, event):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            return

        id_sel = seleccion[0]
        usuario = self.servicio.obtener_usuario_por_id(id_sel)

        if usuario:
            self.usuario_seleccionado_id = usuario.id_usuario
            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, usuario.nombre)
            self.ent_username.delete(0, tk.END)
            self.ent_username.insert(0, usuario.username)
            self.ent_password.delete(0, tk.END)
            self.cmb_rol.set(usuario.rol)

    def _on_combobox_rol_changed(self, event):
        print(f"[EVENTO ComboboxSelected]: Cambio de rol a '{self.cmb_rol.get()}'")

    def _on_tecla_enter(self, event):
        if hasattr(self, 'frame_usuarios') and self.notebook.select():
            if "frame_usuarios" in str(self.notebook.select()):
                self._accion_registrar()

    def _on_tecla_escape(self, event):
        self._limpiar_formulario()

    # --- ACCIONES DE BOTONES ---
    def _accion_registrar(self):
        try:
            self.servicio.registrar_usuario(
                self.ent_nombre.get(),
                self.ent_username.get(),
                self.ent_password.get(),
                self.cmb_rol.get()
            )
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self._cargar_tabla_usuarios()
            self._limpiar_formulario()
        except ValueError as err:
            messagebox.showwarning("Validación", str(err))

    def _accion_actualizar(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla para actualizar.")
            return
        try:
            self.servicio.actualizar_usuario(
                self.usuario_seleccionado_id,
                self.ent_nombre.get(),
                self.ent_username.get(),
                self.ent_password.get(),
                self.cmb_rol.get()
            )
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            self._cargar_tabla_usuarios()
            self._limpiar_formulario()
        except ValueError as err:
            messagebox.showwarning("Validación", str(err))

    def _accion_eliminar(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un usuario de la tabla para eliminar.")
            return

        if messagebox.askyesno("Confirmación", "¿Desea eliminar al usuario seleccionado?"):
            try:
                self.servicio.eliminar_usuario(self.usuario_seleccionado_id)
                messagebox.showinfo("Éxito", "Usuario eliminado.")
                self._cargar_tabla_usuarios()
                self._limpiar_formulario()
            except ValueError as err:
                messagebox.showerror("Error de Seguridad", str(err))

    def _accion_limpiar(self):
        self._limpiar_formulario()