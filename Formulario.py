from tkinter import ttk
from datetime import *

from Paginas.Ingreso_Solicitud import *
from Paginas.Bitacora import *

def variable_global():
    global Contador2
    global Responsable
    Responsable = ""

class Registro:

    def __init__ (self,ventana):

        self.window = ventana
        self.window.title("Formulario para Base de Datos")

        self.original_geometry = "1025x425"
        self.expanded_geometry = "1250x425"
        self.window.geometry(self.original_geometry)

        self.window.resizable(0,0)
        self.window.config(bd=10)

        # Crear el contenedor de pestañas (Notebook)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill='both')

        self.create_pages()

        # Bind the tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def create_pages(self):

        # Crear las páginas (pestañas)
        self.Page1 = ttk.Frame(self.notebook)
        self.Page2 = ttk.Frame(self.notebook)

        # Agregar las páginas al contenedor (Notebook)
        self.notebook.add(self.Page1, text="Ingreso Solicitud")
        self.notebook.add(self.Page2, text="Mov. Bitácora")

        Form_Ingreso_Solicitud(self.Page1, self.window)
        Form_Bitacora(self.Page2, self.window,Responsable)

    def on_tab_change(self, event):
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]
        if selected_tab == "Mov. Bitácora":
            self.window.geometry(self.expanded_geometry)
        else:
            self.window.geometry(self.original_geometry)

def solicitar_responsable():
    global Responsable
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal temporalmente

    # Crear una ventana emergente para seleccionar el responsable
    top = Toplevel(root)
    top.title("Responsable")
    top.geometry("300x100")

    # Crear un Combobox con valores predefinidos
    responsables = ["DDF", "FMR", "MCM", "PTV", "CFM"]
    responsable_var = StringVar()
    label = tk.Label(top,text="Ingrese el responsable:")
    label.pack(side="top")
    combobox = ttk.Combobox(top, textvariable=responsable_var, values=responsables, state="readonly")
    combobox.pack(pady=5)

    def on_select():
        global Responsable
        Responsable = responsable_var.get()
        top.destroy()
        root.destroy()

        # Botón para confirmar la selección
    Button(top, text="Aceptar", command=on_select).pack(pady=10)
    root.mainloop()

if __name__ =="__main__":
    variable_global()
    solicitar_responsable()
    root = tk.Tk()
    app = Registro(root)
    root.mainloop()