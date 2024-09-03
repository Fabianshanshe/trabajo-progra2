class Libros_ejemplo:
    def __init__(self, nombre, ingrediente):
        self.nombre = nombre
        self.ingrediente = ingrediente


    def __str__(self):
        return f"{self.nombre} "
