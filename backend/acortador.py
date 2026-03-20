import string
import random

class Acortador:
    @staticmethod
    def generar_link_corto(longitud=6):
        # Generamos una cadena aleatoria de 6 caracteres (letras y dígitos)
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(longitud))
