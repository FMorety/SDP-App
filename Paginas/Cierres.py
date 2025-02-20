import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from datetime import datetime
from SQLConnect import SQLActualizar

def Form_Cierres(parent,responsable):
    marco = tk.LabelFrame(parent,text="Seguimiento Cierres de OCOS.",font=("Arial",9,"bold")); marco.pack(side="top",padx=12,pady=5 ,ipady=5, ipadx=5, fill="both", expand="yes")

    Label_OCO = tk.Label(marco, text="OCO",font=("Arial",9,"bold")); Label_OCO.grid(row=0,column=0,pady=2,padx=5)
    OCO = tk.Entry(marco,bd=1, highlightthickness=1, highlightbackground="gray",width=15,justify="center",font=("Open Sans",10)); OCO.grid(row=1,column=0,pady=2,padx=5)
    OCO.bind("<KeyPress>",lambda event: FormatoOCO(OCO,event))

    Label_Estado = tk.Label(marco, text="Estado Cierre",font=("Arial",9,"bold")); Label_Estado.grid(row=0,column=1,pady=2,padx=5)
    Estado = ttk.Combobox(marco, values=["Por Solicitar","Solicitado","Cerrado"], state="readonly",width=10); Estado.grid(row=1,column=1,pady=2,padx=5); Estado.set("Por Solicitar")

    Registrar = tk.Button(marco,text="Registrar",width=8, command= lambda : Registrar_Cierres(responsable,OCO,Estado));Registrar.grid(row=1,column=2,pady=2,padx=5)


def FormatoOCO(widget,event):
    
    try:
        widget.get()[0]
    except:
        return
    
    if event.keysym in ("BackSpace", "Delete"):
        return
    elif event.keysym == "Tab":
        return
    elif not event.char.isdigit():
        return "break"
    
    if event.keysym not in ("BackSpace", "Delete"):
        if widget.get()[0] == "1" and len(widget.get()) == 9:
            return "break"
        elif widget.get()[0] != "1" and len(widget.get()) == 8:
            return "break"
        
def Registrar_Cierres(responsable,oco,estado):
    
    if oco.get()[0] == "1" and len(oco.get()) != 9:
        return messagebox.showerror("Error: OCO","Ingrese un código de OCO válido. La OCO debe tener 9 digitos.")
    elif oco.get()[0] != "1" and len(oco.get()) != 8:
        return messagebox.showerror("Error: OCO","Ingrese un código de OCO válido. La OCO debe tener 8 digitos.")
    
    Validacion = SQLActualizar(f"SELECT [OCO] FROM [Subdireccion de Proyectos BBDD].[dbo].[Cierres] WHERE [OCO] = {oco.get()}")

    if not Validacion:
        cierre_nuevo = messagebox.askyesno("OCO no encontrada.","La OCO señalada no se encontró en el listado de OCOs en proceso de cierre. ¿Desea incluir esta nueva OCO al listado?")
        

