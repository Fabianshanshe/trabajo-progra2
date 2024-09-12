import customtkinter as ctk
from tkinter import ttk
from productos import productos
from Biblioteca_ejemplo import Biblioteca_ejemplo
import re
from CTkMessagebox import CTkMessagebox
from tkinter import PhotoImage

class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Biblioteca")
        self.geometry("1200x700")

        # Inicializar la Biblioteca
        self.biblioteca = Biblioteca_ejemplo()

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()

    def crear_pestanas(self):
        # Crear y configurar las pestañas
        self.tab1 = self.tabview.add("Ingreso de Productos")
        self.tab2 = self.tabview.add("Menu")

        # Configurar el contenido de la pestaña 1
        self.configurar_pestana1()
        self.configurar_pestana2()

    def configurar_pestana1(self):
        # Dividir la pestaña en dos frames
        frame_formulario = ctk.CTkFrame(self.tab1)
        frame_formulario.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab1)
        frame_treeview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Formulario en el primer frame
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Producto:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)
        
        label_categoria = ctk.CTkLabel(frame_formulario, text = "Categoria")
        label_categoria.pack(pady=5)
        self.entry_categoria = ctk.CTkEntry(frame_formulario)
        self.entry_categoria.pack(pady = 5)


        #Boton de ingreso
        self.boton_eliminar = ctk.CTkButton(frame_formulario, text="Ingresar Producto")
        self.boton_eliminar.configure(command=self.ingresar_menu)
        self.boton_eliminar.pack(pady=10)
        
        # Botón para eliminar libro arriba del Treeview
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Libro", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_libro)
        self.boton_eliminar.pack(pady=10)

        # Treeview en el segundo frame
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre","Categoria"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Categoria", text="Categoria")
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack( fill="both", expand=True, padx=10, pady=10)

        frame_inferior= ctk.CTkFrame(self.tab2)
        frame_inferior.pack(fill="both", expand=True, padx= 20, pady=10)

        imagen1 = PhotoImage(file="trabajo-progra2\\Hamburguesa.png")
        imagen2 = PhotoImage(file="trabajo-progra2\\Hotdog.png")
        imagen3 = PhotoImage(file="trabajo-progra2\\PapasFritas.png")
        imagen4 = PhotoImage(file="trabajo-progra2\\Bebida.png")

        self.boton_imagen = ctk.CTkButton(frame_superior, text="Hamburguesa", image=imagen1, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top", command=lambda: self.agregar_producto("Hamburguesa", 1, 3500))
        self.boton_imagen.pack(side="left", padx="25", pady=10)

        #Boton Papas Fritas
        self.boton_imagen = ctk.CTkButton(frame_superior, text="Papas Fritas", image=imagen3, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top", command=lambda: self.agregar_producto("Papas Fritas", 1, 500))
        self.boton_imagen.pack(side="left", padx="25", pady=10)
        
        #Boton Hotdog
        self.boton_imagen = ctk.CTkButton(frame_superior, text="Hotdog", image=imagen2, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top", command=lambda: self.agregar_producto("Hotdog", 1, 1800))
        self.boton_imagen.pack(side="left", padx="25", pady=10)
        
        #Boton Bebida
        self.boton_imagen = ctk.CTkButton(frame_superior, text="Bebida", image=imagen4, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top", command=lambda: self.agregar_producto("Bebida", 1, 1100))
        self.boton_imagen.pack(side="left", padx="25", pady=10)

        boton_eliminar = ctk.CTkButton(frame_inferior, text="Eliminar Menu", compound= "right")
        boton_eliminar.configure(command=self.eliminar_producto_menu)
        boton_eliminar.pack(pady=10)

        self.treeview = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad", "Precio"), show="headings")
        self.treeview.heading("Nombre", text="Nombre del Producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Precio", text="Precio Unitario")
        self.treeview.pack(expand=True, fill="both", padx=10, pady=10)

        boton_generar = ctk.CTkButton(frame_inferior, text="Generar Boleta")
        boton_generar.configure(command=self.ingresar_menu)
        boton_generar.pack(pady=10)
        
    def agregar_producto(self, nombre, cantidad, precio):
        # Buscar el producto en el Treeview
        for item in self.treeview.get_children():
            if self.treeview.item(item, 'values')[0] == nombre:
                # Si el producto ya existe, actualizar la cantidad y el precio
                current_values = self.treeview.item(item, 'values')
                new_cantidad = int(current_values[1]) + cantidad
                self.treeview.item(item, values=(nombre, new_cantidad, precio))
                return

        # Si el producto no existe, agregarlo al Treeview
        self.treeview.insert("", "end", values=(nombre, cantidad, precio))




    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False
    def validar_precio(self, Categoria):
        if re.match(r"[1-999]", Categoria):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="la categoria debe contener solo numeros", icon="warning")
            return False

        
   

    def ingresar_menu(self):
        nombre = self.entry_nombre.get()
        categoria = self.entry_categoria.get()

        # Validar entradas
        if not self.validar_nombre(nombre):
            return
        if not self.validar_precio(categoria):
            return
        # Crear una instancia de Libro
        libro = productos(nombre,categoria)

        # Agregar el libro a la biblioteca
        if self.biblioteca.agregar_libro(libro):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El menu ya existe en la biblioteca.", icon="warning")

    def eliminar_libro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un menu para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion)
        nombre = item['values'][0]

        # Eliminar el libro de la biblioteca
        if self.biblioteca.eliminar_libro(nombre):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El libro no se pudo eliminar.", icon="warning")

    def eliminar_producto_menu(self):
    # Función para eliminar de la pestaña 2
        seleccion = self.treeview.selection()
    
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un producto para eliminar.", icon="warning")
            return

    # Eliminar el producto seleccionado
        for item in seleccion:
            self.treeview.delete(item)

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar todos los libros de la biblioteca al Treeview
        for libro in self.biblioteca.obtener_libros():
            self.tree.insert("", "end", values=(libro.nombre, libro.categoria))

                


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AplicacionConPestanas()
    app.mainloop()