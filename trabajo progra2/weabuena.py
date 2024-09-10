# Libreria_app_ejemplo.py
import customtkinter as ctk
from tkinter import ttk
from Ingredientes import Ingredientes
from Inventario import Inventario
import re
from CTkMessagebox import CTkMessagebox

class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventario de Ingredientes")
        self.geometry("1200x700")

        # Inicializar el Inventario
        self.inventario = Inventario()

        # Definir recetas predefinidas
        self.recetas = {
            "hamburguesa": [("Pan", "2"), ("Lechuga", "1"), ("Carne", "1"),("Tomate", "1"),("Tomate", "1")],
            "papas fritas":[("Papas","2")],
            "bebida":[("Cocacola","1")],
            "completo":[("Pan","1"), ("Vienesa","1"),("Palta","1"),("Tomate","1")]
            
            
            
            # Agregar más recetas según se necesiten
        }

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)
        self.crear_pestanas()

    def crear_pestanas(self):
        # Crear y configurar las pestañas
        self.tab1 = self.tabview.add("Ingreso de Ingredientes")
        self.configurar_pestana1()

    def configurar_pestana1(self):
        # Dividir la pestaña en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Ingrediente:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)
        
        label_cantidad = ctk.CTkLabel(frame_formulario, text="Cantidad")
        label_cantidad.pack(pady=5)
        self.entry_cantidad = ctk.CTkEntry(frame_formulario)
        self.entry_cantidad.pack(pady=5)

        # Botón de ingreso
        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Ingrediente")
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)
        
        # Botón para eliminar ingrediente arriba del Treeview
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Ingrediente", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_ingrediente)
        self.boton_eliminar.pack(pady=10)

        # Treeview en el segundo frame
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Cantidad"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def validar_nombre(self, nombre):
        # Validar que el nombre contenga solo letras y espacios
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

    def ingresar_ingrediente(self):
        nombre = self.entry_nombre.get().lower().strip()  # Convertir a minúsculas y quitar espacios
        cantidad_str = self.entry_cantidad.get()

        # Validar que la cantidad ingresada sea un número
        if not cantidad_str.isdigit():
            CTkMessagebox(title="Error", message="La cantidad debe ser un número entero.", icon="warning")
            return

        cantidad = int(cantidad_str)

        # Verificar si el nombre ingresado es una receta predefinida
        if nombre in self.recetas:
            self.agregar_receta_predefinida(nombre, cantidad)
            CTkMessagebox(title="Receta Agregada", message=f"Se han agregado los ingredientes para la receta '{nombre}' con la cantidad especificada.", icon="info")
        else:
            # Validar entradas normales
            if not nombre or cantidad <= 0:
                CTkMessagebox(title="Error", message="Debe ingresar un nombre y una cantidad mayor que cero.", icon="warning")
                return

            # Crear una instancia de Ingrediente
            ingrediente = Ingredientes(nombre, str(cantidad))

            # Agregar el ingrediente al inventario
            if self.inventario.agregar_ingrediente(ingrediente):
                self.actualizar_treeview()
            else:
                CTkMessagebox(title="Error", message="El ingrediente ya existe en el inventario.", icon="warning")

    def agregar_receta_predefinida(self, receta_nombre, cantidad_receta):
        # Obtener los ingredientes de la receta
        ingredientes = self.recetas.get(receta_nombre, [])
        
        # Agregar cada ingrediente de la receta al inventario multiplicado por la cantidad de recetas
        for nombre, cantidad_base in ingredientes:
            cantidad_total = int(cantidad_base) * cantidad_receta  # Multiplicar cantidad base por cantidad de recetas
            ingrediente = Ingredientes(nombre, str(cantidad_total))
            self.inventario.agregar_ingrediente(ingrediente)

        # Actualizar el Treeview para mostrar los ingredientes agregados
        self.actualizar_treeview()

    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un ingrediente para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion)
        nombre = item['values'][0]

        if self.inventario.eliminar_ingrediente(nombre):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El ingrediente no se pudo eliminar.", icon="warning")

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar todos los ingredientes del inventario al Treeview
        for ingrediente in self.inventario.obtener_ingredientes():
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AplicacionConPestanas()
    app.mainloop()
