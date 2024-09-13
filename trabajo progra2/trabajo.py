from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import customtkinter as ctk
from tkinter import ttk
from tkinter import PhotoImage
from CTkMessagebox import CTkMessagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
import customtkinter as ctk
from tkinter import ttk
from Ingredientes import Ingredientes
from Inventario import Inventario
import re
from CTkMessagebox import CTkMessagebox

class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Comida")
        self.geometry("1200x700")

        # Inicializar la Biblioteca
        self.total_precio = 0  # Variable para almacenar el precio total

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()
        
        self.inventario = Inventario()
    
    def crear_pestanas(self):
        # Crear y configurar las pestañas
        self.tab1 = self.tabview.add("Ingreso de Productos")
        self.tab2 = self.tabview.add("Menu")

        # Configurar el contenido de las pestañas
        self.configurar_pestana1()
        self.configurar_pestana2()

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

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(fill="both", expand=True, padx=10, pady=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(fill="both", expand=True, padx=20, pady=10)

        # Cargar imágenes
        imagen1 = PhotoImage(file="trabajo progra2\\imagenes\\Hamburguesa.png")
        imagen2 = PhotoImage(file="trabajo progra2\\imagenes\\Hotdog.png")
        imagen3 = PhotoImage(file="trabajo progra2\\imagenes\\PapasFritas.png")
        imagen4 = PhotoImage(file="trabajo progra2\\imagenes\\Bebida.png")

        # Botones para agregar productos
        self.boton_imagen = ctk.CTkButton(frame_superior, text="Hamburguesa", image=imagen1, 
                                          fg_color="black", hover_color="red", width=100, height=100,
                                          compound="top", command=lambda: self.agregar_producto("Hamburguesa", 1, 3500))
        self.boton_imagen.pack(side="left", padx="25", pady=10)

        self.boton_imagen = ctk.CTkButton(frame_superior, text="Papas Fritas", image=imagen3, 
                                          fg_color="black", hover_color="red", width=100, height=100,
                                          compound="top", command=lambda: self.agregar_producto("Papas Fritas", 1, 500))
        self.boton_imagen.pack(side="left", padx="25", pady=10)

        self.boton_imagen = ctk.CTkButton(frame_superior, text="Hotdog", image=imagen2, 
                                          fg_color="black", hover_color="red", width=100, height=100,
                                          compound="top", command=lambda: self.agregar_producto("Hotdog", 1, 1800))
        self.boton_imagen.pack(side="left", padx="25", pady=10)

        self.boton_imagen = ctk.CTkButton(frame_superior, text="Bebida", image=imagen4, 
                                          fg_color="black", hover_color="red", width=100, height=100,
                                          compound="top", command=lambda: self.agregar_producto("Bebida", 1, 1100))
        self.boton_imagen.pack(side="left", padx="25", pady=10)

        # Frame inferior con boton de eliminar y total
        frame_eliminar_total = ctk.CTkFrame(frame_inferior)
        frame_eliminar_total.pack(fill="x", padx=20, pady=10)

        # Botón para eliminar el menú
        boton_eliminar = ctk.CTkButton(frame_eliminar_total, text="Eliminar Menu", compound="right", command=self.eliminar_producto)
        boton_eliminar.pack(side="left", pady=10)

        # Etiqueta para mostrar el total, al lado del botón eliminar
        self.label_total = ctk.CTkLabel(frame_eliminar_total, text="Total: $0")
        self.label_total.pack(side="left", padx=20, pady=10)

        # Treeview para mostrar los productos agregados
        self.treeview = ttk.Treeview(frame_inferior, columns=("Nombre", "Cantidad", "Precio"), show="headings")
        self.treeview.heading("Nombre", text="Nombre del Producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Precio", text="Precio Unitario")
        self.treeview.pack(expand=True, fill="both", padx=10, pady=10)

        # Botón para generar boleta
        boton_generar = ctk.CTkButton(frame_inferior, text="Generar Boleta", command=self.generar_boleta)
        boton_generar.pack(pady=10)
    
    ingredientes_por_producto = {
    "Papas Fritas": {"papas": 5},
    "Bebida": {"bebida": 1},
    "Hotdog": {"vienesa": 1, "pan": 1, "tomate": 1, "palta": 1},
    "Hamburguesa": {"pan de hamburguesa": 1, "queso": 1, "churrasco de carne": 1}
    }
    
    def verificar_ingredientes(self, producto):
        if producto not in self.ingredientes_por_producto:
            return False, "Producto no definido"

        for ingrediente, cantidad_necesaria in self.ingredientes_por_producto[producto].items():
            # Busca el ingrediente en el inventario
            encontrado = False
            for ing in self.inventario.lista_ingredientes:
                if ing.nombre == ingrediente:
                    encontrado = True
                    # Verifica si hay suficiente cantidad
                    if int(ing.cantidad) < cantidad_necesaria:
                        return False, f"No hay suficientes {ingrediente}."
            if not encontrado:
                return False, f"No hay {ingrediente} en el inventario."
        return True, ""
    
    
    def descontar_ingredientes(self, producto):
        for ingrediente, cantidad_necesaria in self.ingredientes_por_producto[producto].items():
            for ing in self.inventario.lista_ingredientes:
                if ing.nombre == ingrediente:
                    ing.cantidad = str(int(ing.cantidad) - cantidad_necesaria)
                    
                    
    def agregar_producto(self, nombre, cantidad, precio):
        # Verificar si hay suficientes ingredientes
        disponible, mensaje = self.verificar_ingredientes(nombre)
        if not disponible:
            CTkMessagebox(title="Error", message=mensaje, icon="warning")
            return

        # Si hay suficientes ingredientes, proceder a agregar el producto
        for item in self.treeview.get_children():
            if self.treeview.item(item, 'values')[0] == nombre:
                current_values = self.treeview.item(item, 'values')
                new_cantidad = int(current_values[1]) + cantidad
                self.treeview.item(item, values=(nombre, new_cantidad, precio))
                self.total_precio += precio * cantidad
                self.label_total.configure(text=f"Total: ${self.total_precio}")
                self.descontar_ingredientes(nombre)
                self.actualizar_treeview()  # Actualizar inventario en la interfaz
                return

        # Agregar producto si no existe previamente
        self.treeview.insert("", "end", values=(nombre, cantidad, precio))
        self.total_precio += precio * cantidad
        self.label_total.configure(text=f"Total: ${self.total_precio}")

        # Descontar los ingredientes utilizados del inventario
        self.descontar_ingredientes(nombre)
        self.actualizar_treeview()  # Actualizar inventario en la interfaz
        

    def eliminar_producto(self):
        seleccion = self.treeview.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un producto para eliminar.", icon="warning")
            return

        # Obtener los valores del producto seleccionado
        item = self.treeview.item(seleccion)
        nombre = item['values'][0]
        cantidad = int(item['values'][1])
        precio = int(item['values'][2])

        # Restar el precio del total
        self.total_precio -= precio * cantidad
        self.label_total.configure(text=f"Total: ${self.total_precio}")  # Actualizar la etiqueta del total

        # Eliminar el producto del Treeview
        self.treeview.delete(seleccion)

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
            # Validar entradas normales
        if not nombre or cantidad <= 0:
            CTkMessagebox(title="Error", message="Debe ingresar un nombre y una cantidad mayor que cero.", icon="warning")
            return
        for ingrediente in self.inventario.lista_ingredientes:
            if ingrediente.nombre == nombre:
                # Si el ingrediente ya existe, actualizar la cantidad
                ingrediente.cantidad = str(int(ingrediente.cantidad) + cantidad)
                CTkMessagebox(title="Actualizado", message=f"Se ha actualizado la cantidad del ingrediente '{nombre}'.", icon="info")
                self.actualizar_treeview()
                return
            # Crear una instancia de Ingrediente
        ingrediente = Ingredientes(nombre, str(cantidad))

            # Agregar el ingrediente al inventario
        if self.inventario.agregar_ingrediente(ingrediente):
            self.actualizar_treeview()
        else:
            CTkMessagebox(title="Error", message="El ingrediente ya existe en el inventario.", icon="warning")



    def eliminar_ingrediente(self):
        seleccion = self.tree.selection()
        if not seleccion:
            CTkMessagebox(title="Error", message="Por favor selecciona un ingrediente para eliminar.", icon="warning")
            return

        # Obtener el nombre del ingrediente seleccionado desde el Treeview
        item = self.tree.item(seleccion)
        nombre = item['values'][0]

        # Eliminar el ingrediente del inventario
        for ing in self.inventario.lista_ingredientes:
            if ing.nombre == nombre:
                self.inventario.lista_ingredientes.remove(ing)
                CTkMessagebox(title="Éxito", message=f"El ingrediente '{nombre}' ha sido eliminado.", icon="check")
                self.actualizar_treeview()
                return

    def actualizar_treeview(self):
        # Limpiar el Treeview actual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener los ingredientes desde el inventario
        ingredientes = self.inventario.obtener_ingredientes()
        if not ingredientes:
            print("No hay ingredientes en el inventario.")  # Verificar si el inventario está vacío
        else:
            print("Actualizando Treeview con ingredientes.")  # Verificar si se actualiza
            for ingrediente in ingredientes:
                print(f"Insertando: {ingrediente.nombre}, {ingrediente.cantidad}")
                self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.cantidad))

    def generar_boleta(self):
        # Crear un archivo PDF
        c = canvas.Canvas("boleta_restaurante.pdf", pagesize=letter)
        width, height = letter

        # Título y detalles del negocio
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, height - 100, "BOLETA RESTAURANTE")
        
        c.setFont("Helvetica", 12)
        c.drawString(100, height - 140, "Razón Social: Restaurante Ejemplo")
        c.drawString(100, height - 160, "RUT: 12345678-9")
        c.drawString(100, height - 180, "Dirección: Calle Falsa 123")
        c.drawString(100, height - 200, "Teléfono: +56 9 12345678")

        # Espacio antes de la tabla de productos
        y_position = height - 240

        # Datos para la tabla de productos
        data = [["Producto", "Cantidad", "Precio Unitario", "Subtotal"]]

        total = 0
        for item in self.treeview.get_children():
            nombre, cantidad, precio = self.treeview.item(item, "values")
            cantidad = int(cantidad)
            precio = float(precio)
            subtotal = cantidad * precio
            total += subtotal
            data.append([nombre, cantidad, f"${precio:,.0f}", f"${subtotal:,.0f}"])

        # Crear la tabla
        table = Table(data, colWidths=[2 * inch, 1 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Dibujar la tabla
        table.wrapOn(c, width, height)
        table.drawOn(c, 100, y_position - len(data) * 20)

        # Subtotal, IVA y Total (fuera de la tabla)
        iva = total * 0.19
        total_con_iva = total + iva

        y_position -= len(data) * 20 + 30  # Ajustar la posición debajo de la tabla

        c.setFont("Helvetica", 12)
        c.drawString(400, y_position, f"Subtotal: ${total:,.0f}")
        y_position -= 20
        c.drawString(400, y_position, f"IVA (19%): ${iva:,.0f}")
        y_position -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y_position, f"Total: ${total_con_iva:,.0f}")

        # Mensaje de agradecimiento
        c.setFont("Helvetica-Oblique", 12)
        c.drawString(100, 50, "¡Gracias por su compra!")

        # Guardar el archivo PDF
        c.save()

        # Mostrar un mensaje de confirmación
        CTkMessagebox(title="Boleta Generada", message="Boleta generada con éxito.", icon="check")

# Iniciar la aplicación
if __name__ == "__main__":
    app = AplicacionConPestanas()
    app.mainloop()
