from tkinter import ttk
from datetime import *

from Paginas.Ingreso_Solicitud import *

#Python image Library
from PIL import ImageTk, Image

def variable_global():
    global Contador, Contador2


class Registro:

    def __init__ (self,ventana):

        self.window = ventana
        self.window.title("Formulario para Base de Datos")
        self.window.geometry("600x700")
        self.window.resizable(0,0)
        self.window.config(bd=10)

        # Crear el contenedor de pestañas (Notebook)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill='both')

        self.create_pages()

    def create_pages(self):

        # Crear las páginas (pestañas)
        self.Page1 = ttk.Frame(self.notebook)
        self.Page2 = ttk.Frame(self.notebook)

        # Agregar las páginas al contenedor (Notebook)
        self.notebook.add(self.Page1, text="Ingreso Solicitud")
        self.notebook.add(self.Page2, text="Mov. Bitácora")

        Form_Ingreso_Solicitud(self.Page1)

if __name__ =="__main__":
    variable_global()
    root = tk.Tk()
    app = Registro(root)
    root.mainloop()
