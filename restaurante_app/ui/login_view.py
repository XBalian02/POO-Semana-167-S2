import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(tk.Tk):
    def __init__(self, servicio, al_autenticar_exito):
        super().__init__()
        self.servicio = servicio
        self.al_autenticar_exito = al_autenticar_exito

        self.title("Inicio de Sesión - restaurante_app")
        self.geometry("400x320")
        self.resizable(False, False)

        self._crear_interfaz()

    def _crear_interfaz(self):
        frame = ttk.Frame(self, padding=25)
        frame.pack(fill="both", expand=True)

        lbl_titulo = ttk.Label(frame, text="Acceso al Sistema", font=("Segoe UI", 16, "bold"))
        lbl_titulo.pack(pady=(0, 20))

        ttk.Label(frame, text="Nombre de Usuario:").pack(anchor="w", pady=(5, 2))
        self.ent_user = ttk.Entry(frame, width=30)
        self.ent_user.pack(fill="x", pady=(0, 10))
        self.ent_user.focus()

        ttk.Label(frame, text="Contraseña:").pack(anchor="w", pady=(5, 2))
        self.ent_pass = ttk.Entry(frame, show="*", width=30)
        self.ent_pass.pack(fill="x", pady=(0, 20))

        btn_login = ttk.Button(frame, text="Iniciar Sesión", command=self._login)
        btn_login.pack(fill="x", ipady=4)

        # Evento de teclado para ingresar directamente pulsando Enter
        self.bind("<Return>", lambda e: self._login())

    def _login(self):
        user = self.ent_user.get().strip()
        pwd = self.ent_pass.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Atención", "Ingrese sus credenciales completas.")
            return

        usuario = self.servicio.autenticar(user, pwd)
        if usuario:
            self.destroy()
            self.al_autenticar_exito(usuario)
        else:
            messagebox.showerror("Error de Acceso", "Usuario o contraseña incorrectos.")