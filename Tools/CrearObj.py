import tkinter as tk
from tkinter import ttk
from Tools.FuncionesPage1 import *

def crear_entry(parent, label_text, row, column,width1=45):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"bold"))
    label.grid(row=row, column=column, sticky='e', padx=(0,2), pady=(10,0))
    entry = tk.Entry(parent,bd=1, highlightthickness=1, highlightbackground="gray",width=width1)
    entry.grid(row=row, column=column+1, sticky="w",padx=(0,0), pady=(10,0))
    return entry

def crear_entry2(parent, width):
    entry = tk.Entry(parent ,width=width,bd=1, highlightthickness=1, highlightbackground="gray")
    return entry

def crear_combobox(parent, label_text, options, row, column,width1=42,estado="readonly"):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"bold"))
    label.grid(row=row, column=column, sticky='e', padx=(0,2), pady=(10,0))
    combobox = ttk.Combobox(parent, values=options,width=width1,state=estado)
    combobox.grid(row=row, column=column+1, padx=(0,7), pady=(10,0))
    return combobox

def crear_checkbox(parent, label_text, columns, variable):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"italic")).grid(row=1,column=columns,sticky="e",padx=0,pady=0)
    checkbutton = tk.Checkbutton(parent,
                                 variable=variable)
    checkbutton.grid(row=1,column=columns+1, padx=0, pady=0)
    return checkbutton

def crear_text(parent, label_text, row, column, height=2, width=45):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"bold"))
    label.grid(row=row, column=column, sticky='ne', padx=(0,2), pady=(10,0))
    text = tk.Text(parent, height=height, width=width,bd=1, highlightthickness=1, highlightbackground="gray",font=("Segoe UI",8))
    text.grid(row=row, column=column+1, sticky="w",padx=0, pady=(10,0), ipady=10)
    return text

def crear_Frame(parent,rows,pad=0):
    frame = tk.Frame(parent)
    frame.grid(row=rows,column=0,sticky="ew",pady=pad)
    return frame

def agregar_linea(parent, x1, y1, x2, y2, color="black", grosor=1):

    canvas = tk.Canvas(parent, height=abs(y2 - y1), width=abs(x2 - x1), bg=parent["bg"], highlightthickness=0)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor)
    canvas.grid(sticky="n")
    return canvas

def Frame_de_Item(parent, listamarcos):

    MesActual = (datetime.now().month)-1
    Numero = len(listamarcos)

    ### ---------- Frames ---------- ###

    MarcoItem_Nuevo = crear_Frame(parent,0,0); MarcoItem_Nuevo.grid(row=Numero,sticky="n")
    Frame_Titulo = crear_Frame(MarcoItem_Nuevo,0,0); Frame_Titulo.grid(row=0,column=0,columnspan=2,sticky="n")
    Frame_Right = crear_Frame(MarcoItem_Nuevo,1,5); Frame_Right.grid(column=1,padx=(0,15),sticky="ew")
    Frame_Left = crear_Frame(MarcoItem_Nuevo,1,5); Frame_Left.grid(column=0,padx=(15,10),sticky="ew")
    Frame_MontoMes = crear_Frame(MarcoItem_Nuevo,2,15); Frame_MontoMes.grid(column=0,columnspan=2,padx=(20,0),sticky="n")

    listamarcos += [MarcoItem_Nuevo]

    
    ### ---------- Campos ---------- ###

    LineaSep = agregar_linea(Frame_Titulo,10,0,220,0,"gray",grosor=2); LineaSep.grid(row=0,column=0,columnspan=2,sticky="n")

        #Título Item#
    Label_Item = tk.Label(Frame_Titulo,text=f"Item {Numero+1}",anchor="center",font=("Times New Roman",11,"bold")); Label_Item.grid(row=1,column=0,sticky="e",pady=(10,0))

        # Boton de eliminar Item#
    Eliminar_Item = Button(Frame_Titulo,text="Eliminar",command=lambda: eliminar_item(MarcoItem_Nuevo,listamarcos),width=8)
    Eliminar_Item.grid(row=1,column=1,sticky="w",padx=0,pady=(10,0))

        #OCO#
    OCO = crear_entry(Frame_Left, "*OCO:",0,0,15)
    
        #CECO#
    CECO = crear_entry(Frame_Left, "CECO:",1,0,15)
    limitar_caracteres(CECO,15,1)
    
        #Cuenta#
    Cuenta = crear_combobox(Frame_Left, "Cuenta:", [61070000,61075000,61080000],2,0,12); Cuenta.set(Cuenta['values'][0])

        #Tipo ítem#
    Lista_TipoItem = ["Equipamiento", "Mobiliario", "Tecnología", "Infraestructura"]
    TipoItem = crear_combobox(Frame_Right, "Tipo de ítem:",Lista_TipoItem,0,0,14)

        #Ítem#
    Item = crear_entry(Frame_Right, "Ítem Solicitud:",1,0,17)
    Item.grid(padx=(0,7)); limitar_caracteres2(Item)

        #Monto Total Aprobado#
    Label_MontoTotal = Label(Frame_Right,text="Total Aprobado:",font=("Arial",9,"bold")); Label_MontoTotal.grid(row=2,column=0,sticky="ew",padx=(0,2),pady=(10,0))
    MontoTotal = Entry(Frame_Right,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10),width=14); MontoTotal.grid(row=2, column=1,sticky="ew",padx=(0,7),pady=(10,0))
    FormatearNumero(MontoTotal,Frame_Right);     MontoTotal.bind("<KeyRelease>", lambda e: actualizar_total(Frame_Right, Label_Total))
    
        #Monto Aprobado#
    Label_Monto = Label(Frame_MontoMes,text="Monto",anchor="center",font=("Arial",9,"bold")).grid(row=0,column=1,sticky='ew')  
    Monto = Entry(Frame_MontoMes,width=22,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10)); Monto.grid(row=1, column=1,sticky="w", padx=(0,5))
    FormatearNumero(Monto);    Monto.bind("<KeyRelease>", lambda e: actualizar_total(Frame_MontoMes, Label_Total))

        #Mes#
    Lista_Mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    Label_Mes = Label(Frame_MontoMes,text="Mes",anchor="center",font=("Arial",9,"bold")).grid(row=0,column=2,sticky="ew")
    Mes = ttk.Combobox(Frame_MontoMes, values=Lista_Mes,width=15,state="readonly") ; Mes.grid(row=1,column=2,sticky="ew")
    Mes.set(Lista_Mes[MesActual])
    
        #Etiqueta para visualizar el total de lo que corresponde a cada mes
    Label_Total= Label(Frame_MontoMes, text="Total: 0", anchor="w", font=("Arial", 9, "bold")); Label_Total.grid(row=2,column=1,pady=(0,0))
        
        #Botón para agregar mes de imputación
    AgregarMonto = ttk.Button(Frame_MontoMes,text="+",width=3,command=lambda: agregar_fila(Frame_MontoMes,Lista_Mes,AgregarMonto,Label_Total)); AgregarMonto.grid(row=1,column=0,sticky="e",padx=(0,0))