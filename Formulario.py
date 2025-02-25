from tkinter import ttk
from datetime import *

from Paginas.Ingreso_Solicitud import *
from Paginas.Bitacora import *
from Paginas.Cierres import *

responsables_dic = {"DDF": "Deni De Ferrari", "FMR": "Fabio Morety", "MCM": "Maricela Cortez", "PTV": "Pamela Toro", "CFM": "Clara Fuentes"}

def variable_global():
    global Contador2
    global Responsable
    Responsable = ""

class Registro:

    def __init__ (self,ventana):

        self.window = ventana
        self.window.title(f"Formulario para Base de Datos   -   Responsable: {responsables_dic[Responsable]}")

        self.original_geometry = "1025x425"
        self.expanded_geometry = "1250x425"
        self.little_geometry = "400x175"
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
        self.Page3 = ttk.Frame(self.notebook)

        # Agregar las páginas al contenedor (Notebook)
        self.notebook.add(self.Page1, text="Ingreso Solicitud")
        self.notebook.add(self.Page2, text="Mov. Bitácora")
        self.notebook.add(self.Page3, text="Cierres")

        Form_Ingreso_Solicitud(self.Page1,Responsable)
        Form_Bitacora(self.Page2,Responsable)
        Form_Cierres(self.Page3,Responsable)

    def on_tab_change(self, event):
        selected_tab = event.widget.tab(event.widget.index("current"))["text"]
        if selected_tab == "Mov. Bitácora":
            self.window.geometry(self.expanded_geometry)
        elif selected_tab == "Ingreso Solicitud":
            self.window.geometry(self.original_geometry)
        elif selected_tab == "Cierres":
            self.window.geometry(self.little_geometry)

def solicitar_responsable():
    global Responsable
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal temporalmente

    # Crear una ventana emergente para seleccionar el responsable
    top = Toplevel(root)
    top.title("Responsable")
    top.geometry("300x100")

    # Crear un Combobox con valores predefinidos
    responsables = list(responsables_dic.keys())
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

if __name__ == "__main__":
    variable_global()
    solicitar_responsable()
    root = tk.Tk()
    app = Registro(root)
    root.mainloop()