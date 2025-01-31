import tkinter as tk
from tkinter import ttk
from Tools.CrearObj import agregar_linea

import re
import requests
from SQLConnect import SQLConsulta as SQL

def Data_Bitacora():
    
    github_url = "https://raw.githubusercontent.com/FMorety/SDP-App/refs/heads/Original/SQL-Querys/Matriz_CAPEX.sql"
    response = requests.get(github_url)

    if response.status_code == 200:
        SQL_Select = response.text.strip()
    else:
        raise Exception("Error al obtener el archivo SQL desde GitHub")
    
    Data = SQL(SQL_Select,pandas=True)

    return Data

def Entrega_Info(ID,parent,matriz,event):

    #Primero se restringe el ingreso de caracteres no numéricos y se limita la cantidad de caracteres
    if event.keysym in ("BackSpace", "Delete"):
        if ID.get()[:-1] == "":
            for widget in parent.grid_slaves():
                fila_actual = ID.grid_info()["row"]
                if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual:
                    widget.config(text="-")
        return    
    elif not event.char.isdigit():
        return "break"
    elif len(ID.get()) >= 4:
        return "break"
    
    #Luego, se busca el ID en la matriz de la Bitácora, asegurándose de que no esté vacío el campo ID_Activo

    ID_Activo = ID.get()+event.char
    
    if ID_Activo == "":
        return "break"

    info = matriz.loc[matriz['ID_Activo'] == int(ID_Activo)]
    columna = 0; n=0

    print(info) if not info.empty else print("No se encontró información")

    if not info.empty:
        info_dict = info.to_dict('records')[0]
        for key, value in info_dict.items():
            columna += 1+1*n
            
            #Se formatean los datos para que se vean mejor en la interfaz
            if key == 'ID_Activo':
                continue
            elif key == 'OCO':
                value = int(value)
            elif key == 'Post_Resolucion':
                value = "${:,.0f}".format(int(value)).replace(',', '.')
            elif key == 'Nombre_Solicitud' or key == 'Item':
                value = value[:50]+"..." if len(value) > 50 else value

            n=1

            for widget in parent.grid_slaves():
                
                fila_actual = ID.grid_info()["row"]
                
                if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual and widget.grid_info()["column"] == columna:
                    widget.config(text=value)
                    if key == "Nombre_Solicitud" or key == "Item":
                        widget.grid(padx=70-len(value))
                    elif key == "OCO" or key == "ID_Solicitud":
                        widget.grid(padx=25-len(str(value)))
                    
                        
                    
                    break
    else:
        for widget in parent.grid_slaves():
                fila_actual = ID.grid_info()["row"]
                if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual:
                    widget.config(text="-")

def Agregar_Movimiento(boton,parent,matriz,linea):
    #Se crea una nueva fila en la Bitácora
    # Se crea un nuevo botón para agregar un nuevo movimiento luego
        
    fila_nueva = boton.grid_info()["row"]+1

    boton.grid(row=fila_nueva)
    
    ID_Activo = tk.Entry(parent,bd=1, highlightthickness=1, highlightbackground="gray",width=4,justify="center",font=("Open Sans",10)); ID_Activo.grid(row=fila_nueva,column=1)
    ID_Activo.bind("<KeyPress>",lambda event: Entrega_Info(ID_Activo,parent,matriz,event))

    ID_Solicitud = tk.Label(parent, text="-",font=("Arial",9)); ID_Solicitud.grid(row=fila_nueva,column=2,padx=25)

    linea1 = agregar_linea(parent,0,0,0,20); linea1.grid(row=fila_nueva,column=3,sticky="ew")

    OCO = tk.Label(parent, text="-",font=("Arial",9)); OCO.grid(row=fila_nueva,column=4,padx=25)

    linea2 = agregar_linea(parent,0,0,0,20); linea2.grid(row=fila_nueva,column=5,sticky="ew")

    NomSol = tk.Label(parent, text="-",font=("Arial",9)); NomSol.grid(row=fila_nueva,column=6,padx=70)

    linea3 = agregar_linea(parent,0,0,0,20); linea3.grid(row=fila_nueva,column=7,sticky="ew")

    Item = tk.Label(parent, text="-",font=("Arial",9)); Item.grid(row=fila_nueva,column=8,padx=70)

    linea4 = agregar_linea(parent,0,0,0,20); linea4.grid(row=fila_nueva,column=9,sticky="ew")

    Monto_PostRe = tk.Label(parent, text="-",font=("Arial",9)); Monto_PostRe.grid(row=fila_nueva,column=10,padx=(4,10))

    linea = agregar_linea(parent,0,5,0,80); linea.grid(row=0,column=11,rowspan=2,sticky="ew") 

    Movimiento = tk.Entry(parent, bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10),width=14); Movimiento.grid(row=fila_nueva,column=12,padx=(10,5))

    Motivo = ttk.Combobox(parent, values=["Ahorro","Suplemento","Postergación","Cierre"], state="readonly"); Motivo.grid(row=fila_nueva,column=13,padx=5)

    Ticket = tk.Entry(parent, bd=1, highlightthickness=1, highlightbackground="gray"); Ticket.grid(row=fila_nueva,column=14,padx=5)


    
    