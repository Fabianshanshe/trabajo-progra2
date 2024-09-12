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


class AplicacionConPestanas(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Biblioteca")
        self.geometry("1200x700")

        # Inicializar la Biblioteca
        self.total_precio = 0  # Variable para almacenar el precio total

        # Crear pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=500)
        self.tabview.pack(padx=20, pady=20)

        self.crear_pestanas()

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
        label_nombre = ctk.CTkLabel(frame_formulario, text="Nombre del Producto:")
        label_nombre.pack(pady=5)
        self.entry_nombre = ctk.CTkEntry(frame_formulario)
        self.entry_nombre.pack(pady=5)

        label_categoria = ctk.CTkLabel(frame_formulario, text="Categoria")
        label_categoria.pack(pady=5)
        self.entry_categoria = ctk.CTkEntry(frame_formulario)
        self.entry_categoria.pack(pady=5)

        # Botón de ingreso
        self.boton_ingresar = ctk.CTkButton(frame_formulario, text="Ingresar Producto", command=self.agregar_producto)
        self.boton_ingresar.pack(pady=10)

        # Botón para eliminar producto arriba del Treeview
        self.boton_eliminar = ctk.CTkButton(frame_treeview, text="Eliminar Producto", fg_color="black", text_color="white", command=self.eliminar_producto)
        self.boton_eliminar.pack(pady=10)

        # Treeview en el segundo frame
        self.tree = ttk.Treeview(frame_treeview, columns=("Nombre", "Categoria"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def configurar_pestana2(self):
        frame_superior = ctk.CTkFrame(self.tab2)
        frame_superior.pack(fill="both", expand=True, padx=10, pady=10)

        frame_inferior = ctk.CTkFrame(self.tab2)
        frame_inferior.pack(fill="both", expand=True, padx=20, pady=10)

        # Cargar imágenes
        imagen1 = PhotoImage(file="trabajo-progra2\\Hamburguesa.png")
        imagen2 = PhotoImage(file="trabajo-progra2\\Hotdog.png")
        imagen3 = PhotoImage(file="trabajo-progra2\\PapasFritas.png")
        imagen4 = PhotoImage(file="trabajo-progra2\\Bebida.png")

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

    def agregar_producto(self, nombre, cantidad, precio):
        # Buscar el producto en el Treeview
        for item in self.treeview.get_children():
            if self.treeview.item(item, 'values')[0] == nombre:
                # Si el producto ya existe, actualizar la cantidad y el precio
                current_values = self.treeview.item(item, 'values')
                new_cantidad = int(current_values[1]) + cantidad
                self.treeview.item(item, values=(nombre, new_cantidad, precio))
                self.total_precio += precio * cantidad  # Actualizar el total
                self.label_total.configure(text=f"Total: ${self.total_precio}")  # Actualizar la etiqueta del total
                return

        # Si el producto no existe, agregarlo al Treeview
        self.treeview.insert("", "end", values=(nombre, cantidad, precio))
        self.total_precio += precio * cantidad  # Actualizar el total
        self.label_total.configure(text=f"Total: ${self.total_precio}")  # Actualizar la etiqueta del total

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
