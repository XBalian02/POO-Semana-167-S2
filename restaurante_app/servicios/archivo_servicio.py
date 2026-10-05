import json
import os

class ArchivoServicio:
    """Servicio genérico para la lectura y escritura de archivos JSON de persistencia."""
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self._asegurar_directorio()

    def _asegurar_directorio(self):
        directorio = os.path.dirname(self.ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def cargar(self):
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def guardar(self, datos):
        with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)