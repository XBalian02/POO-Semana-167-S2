from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

def iniciar_aplicacion():
    # Instanciación del servicio central
    servicio = RestauranteServicio()

    def al_autenticar(usuario_autenticado):
        # Abre la ventana principal pasándole el objeto del usuario logueado
        app = MainView(servicio, usuario_autenticado)
        app.mainloop()

    # Muestra primero el inicio de sesión
    login = LoginView(servicio, al_autenticar)
    login.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()