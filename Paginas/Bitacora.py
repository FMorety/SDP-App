import tkinter as tk
from tkinter import ttk
from Tools.CrearObj import *

from Tools.FuncionesPage2 import *
from tkinter import Scrollbar

def Form_Bitacora(parent,window):

    Matriz_CAPEX = Data_Bitacora()

    marco = tk.LabelFrame(parent,text="Planilla Bitácora",font=("Arial",10,"bold")); marco.pack(side="top",padx=12,pady=5 ,ipady=5, ipadx=5, fill="both", expand="yes")
    canvas = tk.Canvas(marco)
    scrollbar_y = tk.Scrollbar(marco, orient="vertical", command=canvas.yview)
    scrollbar_x = tk.Scrollbar(marco, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    canvas.config(highlightthickness=0)

    scrollbar_x.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

    AgregarMovimiento = ttk.Button(scrollable_frame,text="+",width=3,command=lambda: Agregar_Movimiento(AgregarMovimiento,scrollable_frame,Matriz_CAPEX,linea))
    AgregarMovimiento.grid(row=1,column=0,sticky="e",padx=(8,0))
    
    Label_ID_Activo = tk.Label(scrollable_frame, text="ID Activo",font=("Arial",9,"bold")); Label_ID_Activo.grid(row=0,column=1,pady=2)
    ID_Activo = tk.Entry(scrollable_frame,bd=1, highlightthickness=1, highlightbackground="gray",width=4,justify="center",font=("Open Sans",10)); ID_Activo.grid(row=1,column=1)
    ID_Activo.bind("<KeyPress>",lambda event: Entrega_Info(ID_Activo,scrollable_frame,Matriz_CAPEX,event))

    Label_ID_Solicitud = tk.Label(scrollable_frame, text="ID Solicitud",font=("Arial",9,"bold")); Label_ID_Solicitud.grid(row=0,column=2,pady=2,padx=(0,25))
    ID_Solicitud = tk.Label(scrollable_frame, text="-",font=("Arial",9)); ID_Solicitud.grid(row=1,column=2,padx=(0,25))

    linea1 = agregar_linea(scrollable_frame,0,0,0,20); linea1.grid(row=1,column=3,sticky="ew")

    Label_OCO = tk.Label(scrollable_frame, text="OCO",font=("Arial",9,"bold")); Label_OCO.grid(row=0,column=4,pady=2,padx=25)
    OCO = tk.Label(scrollable_frame, text="-",font=("Arial",9)); OCO.grid(row=1,column=4,padx=25)

    linea2 = agregar_linea(scrollable_frame,0,0,0,20); linea2.grid(row=1,column=5,sticky="ew")

    Label_NomSol = tk.Label(scrollable_frame, text="Nombre Solicitud",font=("Arial",9,"bold")); Label_NomSol.grid(row=0,column=6,pady=2,padx=70)
    NomSol = tk.Label(scrollable_frame, text="-",font=("Arial",9)); NomSol.grid(row=1,column=6,padx=70)

    linea3 = agregar_linea(scrollable_frame,0,0,0,20); linea3.grid(row=1,column=7,sticky="ew")

    Label_Item = tk.Label(scrollable_frame, text="Ítem",font=("Arial",9,"bold")); Label_Item.grid(row=0,column=8,pady=2,padx=70)
    Item = tk.Label(scrollable_frame, text="-",font=("Arial",9)); Item.grid(row=1,column=8,padx=70)

    linea4 = agregar_linea(scrollable_frame,0,0,0,20); linea4.grid(row=1,column=9,sticky="ew")

    Label_Monto_PostRe = tk.Label(scrollable_frame, text="Post Resolución",font=("Arial",9,"bold")); Label_Monto_PostRe.grid(row=0,column=10,padx=4,pady=2)
    Monto_PostRe = tk.Label(scrollable_frame, text="-",font=("Arial",9)); Monto_PostRe.grid(row=1,column=10,padx=4)

    linea5 = agregar_linea(scrollable_frame,0,0,0,20); linea5.grid(row=1,column=11,sticky="ew")

    Label_Saldo = tk.Label(scrollable_frame, text="Saldo PostRe",font=("Arial",9,"bold")); Label_Saldo.grid(row=0,column=12,padx=(4,20),pady=2)
    Saldo = tk.Label(scrollable_frame, text="-",font=("Arial",9)); Saldo.grid(row=1,column=12,padx=(4,20))

    linea = agregar_linea(scrollable_frame,0,5,0,80); linea.grid(row=0,column=13,rowspan=2,sticky="ew") 

    Label_Movimiento = tk.Label(scrollable_frame, text="Monto",font=("Arial",9,"bold")); Label_Movimiento.grid(row=0,column=14,padx=(20,5),pady=2)
    Movimiento = tk.Entry(scrollable_frame, bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10),width=14); Movimiento.grid(row=1,column=14,padx=(20,5))
    Movimiento.bind("<KeyPress>",lambda event: Reglas_Monto(Movimiento,Saldo,Motivo,scrollable_frame,event))

    Label_Motivo = tk.Label(scrollable_frame, text="Motivo",font=("Arial",9,"bold")); Label_Motivo.grid(row=0,column=15,pady=2,padx=5)
    Motivo = ttk.Combobox(scrollable_frame, values=["Ahorro","Suplemento","Postergación","Bajar"], state="readonly"); Motivo.grid(row=1,column=15,padx=5)
    Motivo.set(Motivo['values'][1])
    Motivo.bind("<<ComboboxSelected>>",lambda event: Motivo_Seleccionado(Motivo,Monto_PostRe,Saldo,Movimiento))

    Label_Ticket = tk.Label(scrollable_frame, text="Ticket/Correo/Comentario",font=("Arial",9,"bold")); Label_Ticket.grid(row=0,column=16,pady=2,padx=5)
    Ticket = tk.Entry(scrollable_frame, bd=1, highlightthickness=1, highlightbackground="gray",width=40); Ticket.grid(row=1,column=16,padx=5)

    #Se agrega fila para el fondo seleccionado para este evento

    linea_horizontal = agregar_linea(scrollable_frame,25,0,1700,0); linea_horizontal.grid(row=2,column=0,columnspan=17,sticky="ew",pady=10)

    ID_Activo_Fondo = ttk.Combobox(scrollable_frame, values=Fondos, state="readonly",width=10); ID_Activo_Fondo.grid(row=3,column=0,columnspan=2)
    ID_Activo_Fondo.bind("<Button-1>", expandir_combobox)  # Ajusta el ancho al hacer clic
    ID_Activo_Fondo.bind("<<ComboboxSelected>>", lambda e: Entrega_Info_Fondo(ID_Activo_Fondo,scrollable_frame,Matriz_CAPEX))  # Restaura el ancho al seleccionar una opción
    ID_Activo_Fondo.bind("<FocusOut>", restaurar_combobox)  # Restaura el ancho al perder el foco

    ID_Solicitud_Fondo = tk.Label(scrollable_frame, text="-",font=("Arial",9)); ID_Solicitud_Fondo.grid(row=3,column=2,padx=(0,25))

    linea1 = agregar_linea(scrollable_frame,0,0,0,20); linea1.grid(row=3,column=3,sticky="ew")

    OCO_Fondo = tk.Label(scrollable_frame, text="-",font=("Arial",9)); OCO_Fondo.grid(row=3,column=4,padx=25)

    linea2 = agregar_linea(scrollable_frame,0,0,0,20); linea2.grid(row=3,column=5,sticky="ew")

    NomSol_Fondo = tk.Label(scrollable_frame, text="-",font=("Arial",9)); NomSol_Fondo.grid(row=3,column=6,padx=70)

    linea3 = agregar_linea(scrollable_frame,0,0,0,20); linea3.grid(row=3,column=7,sticky="ew")

    Item_Fondo = tk.Label(scrollable_frame, text="-",font=("Arial",9)); Item_Fondo.grid(row=3,column=8,padx=70)

    linea4 = agregar_linea(scrollable_frame,0,0,0,20); linea4.grid(row=3,column=9,sticky="ew")

    Monto_PostRe_Fondo = tk.Label(scrollable_frame, text="-",font=("Arial",9)); Monto_PostRe_Fondo.grid(row=3,column=10,padx=4)

    linea5 = agregar_linea(scrollable_frame,0,0,0,20); linea5.grid(row=3,column=11,sticky="ew")

    Saldo_Fondo = tk.Label(scrollable_frame, text="-",font=("Arial",9)); Saldo_Fondo.grid(row=3,column=12,padx=(4,20))

    linea_fondo = agregar_linea(scrollable_frame,0,0,0,30); linea_fondo.grid(row=3,column=13,sticky="ew") 

    Movimiento_Fondo = tk.Label(scrollable_frame, text="-" ,font=("Open Sans",10)); Movimiento_Fondo.grid(row=3,column=14,padx=(20,5))

    Motivo_Fondo = ttk.Combobox(scrollable_frame, values=[""], state="disabled"); Motivo_Fondo.grid(row=3,column=15,padx=5)

    Ticket_Fondo = tk.Entry(scrollable_frame, bd=1, highlightthickness=1, highlightbackground="gray",width=40); Ticket_Fondo.grid(row=3,column=16,padx=5)

    Label_Fondo = tk.Label(scrollable_frame, text="Fondo",font=("Arial",7,"bold")); Label_Fondo.grid(row=4,column=0,columnspan=2,sticky="n")