class Biblioteca_ejemplo:
    def __init__(self):
        self.lista_libros = []

    def agregar_libro(self, libro):
        self.lista_libros.append(libro)
        return True  # Libro agregado como nuevo

    def eliminar_libro(self, nombre_libro, cantidad=1):
        for lib in self.lista_libros:
            if lib.nombre == nombre_libro:
                self.lista_libros.remove(lib)
                return True
            else: 
                return False



    def obtener_libros(self):
        return [libro for libro in self.lista_libros]
