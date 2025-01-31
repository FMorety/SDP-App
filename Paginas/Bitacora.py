import tkinter as tk
from tkinter import ttk
from Tools.CrearObj import *

def Form_Bitacora(parent,window):

    marco = tk.LabelFrame(parent,text="Planilla Bitácora",font=("Arial",10,"bold")); marco.pack(side="top",padx=12,pady=5 ,ipady=5, ipadx=5, fill="both", expand="yes")

    AgregarMovimiento = ttk.Button(marco,text="+",width=3)
    AgregarMovimiento.grid(row=1,column=0,sticky="e",padx=(8,0))
    
    Label_ID_Activo = tk.Label(marco, text="ID Activo",font=("Arial",9,"bold")); Label_ID_Activo.grid(row=0,column=1,padx=5,pady=2)
    ID_Activo = tk.Entry(marco,bd=1, highlightthickness=1, highlightbackground="gray",width=8,font=("Arial",9)); ID_Activo.grid(row=1,column=1,padx=5)

    Label_ID_Solicitud = tk.Label(marco, text="ID Solicitud",font=("Arial",9,"bold")); Label_ID_Solicitud.grid(row=0,column=2,padx=5,pady=2)
    ID_Solicitud = tk.Label(marco, text="-",font=("Arial",9)); ID_Solicitud.grid(row=1,column=2,padx=5)

    Label_OCO = tk.Label(marco, text="OCO",font=("Arial",9,"bold")); Label_OCO.grid(row=0,column=3,padx=5,pady=2)
    OCO = tk.Label(marco, text="-",font=("Arial",9)); OCO.grid(row=1,column=3,padx=5)

    Label_NomSol = tk.Label(marco, text="Nombre Solicitud",font=("Arial",9,"bold")); Label_NomSol.grid(row=0,column=4,padx=5,pady=2)
    NomSol = tk.Label(marco, text="-",font=("Arial",9)); NomSol.grid(row=1,column=4,padx=5)

    Label_Item = tk.Label(marco, text="Ítem",font=("Arial",9,"bold")); Label_Item.grid(row=0,column=5,padx=5,pady=2)
    Item = tk.Label(marco, text="-",font=("Arial",9)); Item.grid(row=1,column=5,padx=5)

    Label_Monto_PostRe = tk.Label(marco, text="Post Resolución",font=("Arial",9,"bold")); Label_Monto_PostRe.grid(row=0,column=6,padx=(5,10),pady=2)
    Monto_PostRe = tk.Label(marco, text="-",font=("Arial",9)); Monto_PostRe.grid(row=1,column=6,padx=(5,10))

    linea = agregar_linea(marco,0,10,0,80); linea.grid(row=0,column=7,rowspan=2,sticky="ew") 

    Label_Movimiento = tk.Label(marco, text="Monto",font=("Arial",9,"bold")); Label_Movimiento.grid(row=0,column=8,padx=(10,5),pady=2)
    Movimiento = tk.Entry(marco, bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10),width=14); Movimiento.grid(row=1,column=8,padx=(10,5))

    Label_Motivo = tk.Label(marco, text="Motivo",font=("Arial",9,"bold")); Label_Motivo.grid(row=0,column=9,padx=5,pady=2)
    Motivo = ttk.Combobox(marco, values=["Ahorro","Suplemento","Postergación","Cierre"], state="readonly"); Motivo.grid(row=1,column=9,padx=5)

    Label_Ticket = tk.Label(marco, text="Ticket/Correo",font=("Arial",9,"bold")); Label_Ticket.grid(row=0,column=10,padx=5,pady=2)
    Ticket = tk.Entry(marco, bd=1, highlightthickness=1, highlightbackground="gray"); Ticket.grid(row=1,column=10,padx=5)