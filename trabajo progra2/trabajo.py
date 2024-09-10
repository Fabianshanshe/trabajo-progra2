import customtkinter as ctk
from tkinter import ttk
from Libros_ejemplo import Libros_ejemplo
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
        self.tab2 = self.tabview.add("Pedido")

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
        label_nombre = ctk.CTkLabel(frame_formulario, text="Producto:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)
        
        label_nombre = ctk.CTkLabel(frame_formulario, text="Precio:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)


        #Boton de ingreso
        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar producto")
        self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        self.boton_ingresar.pack(pady=10)

        # Botón para eliminar libro arriba del Treeview
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar producto", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_libro)
        self.boton_eliminar.pack(pady=10)

        # Treeview en el segundo frame
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre","Nombre2"), show="headings")
        self.tree.heading("Nombre", text="Producto")
        self.tree.heading("Nombre2", text = "wea")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        
    def configurar_pestana2(self):
        # Dividir la pestaña en dos frames
        frame_formulario = ctk.CTkFrame(self.tab2)
        frame_formulario.pack(side="top", fill="x", expand=True, padx=10, pady=10)

        frame_treeview = ctk.CTkFrame(self.tab2)
        frame_treeview.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        #Nro1 Meli Arreglo
        imagen1 = PhotoImage(file="C:\\Users\\Meliq\\OneDrive\\Desktop\\TrabajoProgra2\\Hamburguesa.png")
        imagen2 = PhotoImage(file="C:\\Users\\Meliq\\OneDrive\\Desktop\\TrabajoProgra2\\Hotdog.png")
        imagen3 = PhotoImage(file="C:\\Users\\Meliq\\OneDrive\\Desktop\\TrabajoProgra2\\PapasFritas.png")
        imagen4 = PhotoImage(file="C:\\Users\\Meliq\\OneDrive\\Desktop\\TrabajoProgra2\\Bebida.png")
        
        #Boton Hamburguesa
        self.boton_imagen = ctk.CTkButton(frame_formulario, text="Hamburguesa", image=imagen1, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top")
        self.boton_imagen.pack(side="left", padx="25", pady=10)
        
        #Boton Papas Fritas
        self.boton_imagen = ctk.CTkButton(frame_formulario, text="Papas Fritas", image=imagen3, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top")
        self.boton_imagen.pack(side="left", padx="25", pady=10)
        
        #Boton Hotdog
        self.boton_imagen = ctk.CTkButton(frame_formulario, text="Hotdog", image=imagen2, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top")
        self.boton_imagen.pack(side="left", padx="25", pady=10)
        
        #Boton Bebida
        self.boton_imagen = ctk.CTkButton(frame_formulario, text="Bebida", image=imagen4, 
                                  fg_color="black", hover_color="red", width=100, height=100,
                                  compound="top")
        self.boton_imagen.pack(side="left", padx="25", pady=10)


        #Boton de ingreso
        #self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar producto")
        #self.boton_ingresar.configure(command=self.ingresar_ingrediente)
        #self.boton_ingresar.pack(pady=10)

        # Botón para eliminar libro arriba del Treeview
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar producto", fg_color="black", text_color="white")
        self.boton_eliminar.configure(command=self.eliminar_libro)
        self.boton_eliminar.pack(pady=10)

        # Treeview en el segundo frame
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)


    def validar_nombre(self, nombre):
        if re.match(r"^[a-zA-Z\s]+$", nombre):
            return True
        else:
            CTkMessagebox(title="Error de Validación", message="El nombre debe contener solo letras y espacios.", icon="warning")
            return False

        
   

    def ingresar_ingrediente (self):
        nombre = self.entry_nombre.get()

        # Validar entradas
        if not self.validar_nombre(nombre):
            return
        
        # Crear una instancia de Libro
        libro = Libros_ejemplo(nombre)

        # Agregar el libro a la biblioteca
        if self.biblioteca.agregar_libro(libro):
            self.actualizar_treeview()

    def eliminar_libro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un producto para eliminar.", icon="warning")
            return

        item = self.tree.item(seleccion)
        nombre = item['values'][0]

        # Eliminar el libro de la biblioteca
        if self.biblioteca.eliminar_libro(nombre):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El libro no se pudo eliminar.", icon="warning")

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar todos los libros de la biblioteca al Treeview
        for libro in self.biblioteca.obtener_libros():
            self.tree.insert("", "end", values=(libro.nombre))


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = AplicacionConPestanas()
    app.mainloop()