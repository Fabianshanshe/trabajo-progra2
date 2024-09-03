class Inventario:
    def __init__(self):
        self.lista_ingredientes = []

    def agregar_ingrediente(self, ingrediente):
        self.lista_ingredientes.append(ingrediente)
        return True  # Ingrediente agregado como nuevo

    def eliminar_ingrediente(self, nombre_ingrediente, cantidad=1):
        for ing in self.lista_ingredientes:
            if ing.nombre == nombre_ingrediente:
                self.lista_ingredientes.remove(ing)
                return True
            else:
                return False

    def obtener_ingredientes(self):
        return [ingrediente for ingrediente in self.lista_ingredientes]
