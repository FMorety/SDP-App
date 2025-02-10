import tkinter as tk
from tkinter import ttk
from Tools.CrearObj import agregar_linea

from datetime import datetime
from tkinter import messagebox
import re
import requests
from SQLConnect import SQLConsulta as SQL

Divisiones = {
    "Alameda": -1000,
    "Alonso Ovalle": -2600,
    "Antonio Varas": -800,
    "Arauco": -2500,
    "Concepción": -500,
    "Maipú": -1400,
    "Melipilla": -2400,
    "Nacimiento": -2900,
    "Plaza Norte": -1900,
    "Plaza Oeste": -1200,
    "Plaza Vespucio": -1100,
    "Puente Alto": -1300,
    "Puerto Montt": -2700,
    "San Bernardo": -1800,
    "San Carlos": -900,
    "San Joaquín": -1600,
    "Valparaíso": -400,
    "Villarrica": -2800,
    "Viña del Mar": -600,
    "Liceo Renca": -700,
}
Fondos_Centrales = {
    "Ren. Tecnologica": -8,
    "Des. Informatico": -7,
    "Seg. Integral": -6,
    "Acc. Universal": -5,
    "Infra. Crítica": -4,
    "Infraestructura": -3,
    "Contingencia": -2,
    "Emergentes": -1
}
Fondos_DIAITT = {
    "DIAITT -185": -185,
    "DIAITT -186": -186,
    "DIAITT -187": -187,
    "DIAITT -188": -188,
    "DIAITT -189": -189,
    "DIAITT -190": -190,
    "DIAITT -191": -191,
    "DIAITT -192": -192,
}

Fondos_Centrales = dict(reversed(list(Fondos_Centrales.items())))

Fondos = ["-----------------------"] + list(Fondos_Centrales.keys()) + ["-----------------------"] + list(Fondos_DIAITT.keys())

#Funciones simples para el manejo de los combobox
def expandir_combobox(event):
    global valor_previo
    valor_previo = event.widget.get()  # Almacena el valor anterior
    event.widget.config(width=20)
def restaurar_combobox(event):
    event.widget.config(width=10)

#Funcionalidad general para la hoja Bitacora
def Data_Bitacora():
    
    github_url = "https://raw.githubusercontent.com/FMorety/SDP-App/refs/heads/Original/SQL-Querys/Matriz_CAPEX.sql"
    response = requests.get(github_url)

    if response.status_code == 200:
        SQL_Select = response.text.strip()
    else:
        raise Exception("Error al obtener el archivo SQL desde GitHub")
    
    Data = SQL(SQL_Select,pandas=True)

    return Data

def actualizar_info(info, ID, parent):
    columna = 0
    n = 0
    if info is not None and not info.empty:
        info_dict = info.to_dict('records')[0]
        for key, value in info_dict.items():
            columna += 1 + 1 * n

            # Se formatean los datos para que se vean mejor en la interfaz
            if key == 'ID_Activo':
                continue
            elif key == 'OCO':
                try:
                    value = int(value)
                except:
                    value = "Pendiente"
            elif key == 'Post_Resolucion' or key == 'Post_Resolucion2':
                value = "${:,.0f}".format(int(value)).replace(',', '.')
            elif key == 'Nombre_Solicitud' or key == 'Item':
                value = value[:50] + "..." if len(value) > 50 else value

            n = 1

            for widget in parent.grid_slaves():
                fila_actual = ID.grid_info()["row"]

                if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual and widget.grid_info()["column"] == columna:
                    widget.config(text=value)
                    if key == "Nombre_Solicitud" or key == "Item":
                        widget.grid(padx=70 - len(value))
                    elif key == "OCO" or key == "ID_Solicitud":
                        widget.grid(padx=25 - len(str(value)))
                    break
    else:
        for widget in parent.grid_slaves():
            fila_actual = ID.grid_info()["row"]
            if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual:
                widget.config(text="-")

def Entrega_Info(ID, parent, matriz, event):
    
    # Se busca el ID en la matriz de la Bitácora, asegurándose de que no esté vacío el campo ID_Activo
    ID_Activo = ID.get() + (event.char if event.char.isdigit() else "")
    
    if ID_Activo == "":
        return "break"

    info = matriz.loc[matriz['ID_Activo'] == int(ID_Activo)] if ID_Activo.isdigit() else None

    # Primero se restringe el ingreso de caracteres no numéricos y se limita la cantidad de caracteres
    if event.keysym in ("BackSpace", "Delete"):

        # Extrae el último caracter de la celda y busca la información en la matriz
        info = matriz.loc[matriz['ID_Activo'] == int(ID_Activo[:-1])] if ID_Activo[:-1] != "" else None

        if ID.get()[:-1] == "":
            for widget in parent.grid_slaves():
                fila_actual = ID.grid_info()["row"]
                if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual:
                    widget.config(text="-")
            Obtener_Fondos(parent,matriz)
        else:
            actualizar_info(info, ID, parent)
            Obtener_Fondos(parent,matriz)
        return
        
    if event.keysym == "Tab":
        return
    
    elif not event.char.isdigit():
        return "break"
    elif len(ID.get()) >= 4:
        return "break"
    
    actualizar_info(info, ID, parent)
    Obtener_Fondos(parent,matriz)

def Agregar_Movimiento(boton,parent,matriz,linea):
    #Se crea una nueva fila en la Bitácora
    # Se crea un nuevo botón para agregar un nuevo movimiento luego
        
    fila_nueva = boton.grid_info()["row"]+1

    for widget in parent.grid_slaves():
        if widget.grid_info()["row"] >= fila_nueva:
            widget.grid(row=widget.grid_info()["row"]+1)

    boton.grid(row=fila_nueva)

    Eliminar_fila = ttk.Button(parent,text="-",width=3,command=lambda: Eliminar_Movimiento(Eliminar_fila,parent,linea,matriz))
    Eliminar_fila.grid(row=fila_nueva-1,column=0,sticky="e",padx=(8,0))
    
    ID_Activo = tk.Entry(parent,bd=1, highlightthickness=1, highlightbackground="gray",width=4,justify="center",font=("Open Sans",10)); ID_Activo.grid(row=fila_nueva,column=1)
    ID_Activo.bind("<KeyPress>",lambda event: Entrega_Info(ID_Activo,parent,matriz,event))

    ID_Solicitud = tk.Label(parent, text="-",font=("Arial",9)); ID_Solicitud.grid(row=fila_nueva,column=2,padx=(0,25))

    linea1 = agregar_linea(parent,0,0,0,20); linea1.grid(row=fila_nueva,column=3,sticky="ew")

    OCO = tk.Label(parent, text="-",font=("Arial",9)); OCO.grid(row=fila_nueva,column=4,padx=25)

    linea2 = agregar_linea(parent,0,0,0,20); linea2.grid(row=fila_nueva,column=5,sticky="ew")

    NomSol = tk.Label(parent, text="-",font=("Arial",9)); NomSol.grid(row=fila_nueva,column=6,padx=70)

    linea3 = agregar_linea(parent,0,0,0,20); linea3.grid(row=fila_nueva,column=7,sticky="ew")

    Item = tk.Label(parent, text="-",font=("Arial",9)); Item.grid(row=fila_nueva,column=8,padx=70)

    linea4 = agregar_linea(parent,0,0,0,20); linea4.grid(row=fila_nueva,column=9,sticky="ew")

    Monto_PostRe = tk.Label(parent, text="-",font=("Arial",9)); Monto_PostRe.grid(row=fila_nueva,column=10,padx=4)

    linea5 = agregar_linea(parent,0,0,0,20); linea5.grid(row=fila_nueva,column=11,sticky="ew")

    Saldo = tk.Label(parent, text="-",font=("Arial",9)); Saldo.grid(row=fila_nueva,column=12,padx=(4,20))

    Movimiento = tk.Entry(parent, bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10),width=14,justify="center"); Movimiento.grid(row=fila_nueva,column=14,padx=(20,5))
    Movimiento.bind("<KeyPress>",lambda event: Reglas_Monto(Movimiento,Saldo,Motivo,parent,event))

    Motivo = ttk.Combobox(parent, values=["Ahorro","Suplemento","Postergación","Bajar"], state="readonly"); Motivo.grid(row=fila_nueva,column=15,padx=5)
    Motivo.set(Motivo['values'][1])
    Motivo.bind("<<ComboboxSelected>>",lambda event: Motivo_Seleccionado(Motivo,Monto_PostRe,Saldo,Movimiento))

    Ticket = tk.Entry(parent, bd=1, highlightthickness=1, highlightbackground="gray",width=40); Ticket.grid(row=fila_nueva,column=16,padx=5)

     # Obtener la altura actual de la línea y agregarle 40 unidades. Actualizar el rowspan de la línea también.

    for widget in parent.grid_slaves():
        if widget.grid_info()["column"] == 13 and widget.grid_info()["row"] == 0:
            widget.destroy()
            break

    linea = agregar_linea(parent, 0, 5, 0, 80 + 40 * (fila_nueva-1) )
    linea.grid(row=0, column=13, rowspan=2+(fila_nueva-1), sticky="ew")

def Eliminar_Movimiento(boton,parent_in,linea,matriz):
    # Elimina la fila de la Bitácora y reacomoda las filas restantes
    # Se elimina el botón de eliminación de fila y se reacomodan los botones restantes

    fila = boton.grid_info()["row"]

    for widget in parent_in.grid_slaves():
        if widget.grid_info()["column"] == 13 and widget.grid_info()["row"] == 0:
            linea = widget
        elif widget.grid_info()["row"] == fila:
            widget.destroy()
        elif widget.grid_info()["row"] > fila:
            widget.grid(row=widget.grid_info()["row"]-1)
    
    # Se obtiene la altura actual de la línea y se le restan 40 unidades. Se actualiza el rowspan de la línea también.+

    current_rowspan = int(linea.grid_info().get("rowspan", 1))
    linea.destroy()
    linea = agregar_linea(parent_in, 0, 5, 0, 80 + 40 * (current_rowspan-3))
    linea.grid(row=0, column=13, rowspan=2+(current_rowspan-3), sticky="ew")

    Obtener_Fondos(parent_in,matriz)
    Control_Monto_Fondo(parent_in)
    
def Formato_Monto(monto, saldo, motivo, event):
    
    if saldo.cget("text") == "-":
        messagebox.showerror("ID activo vacío", "Primero debe ingresar un ID de Activo")
        return "break"
    
    # Se obtiene el valor actual de la Post Resolución
    saldo_value = int(saldo.cget("text").replace('$','').replace('.',''))
    
    def formatear_e_insertar(monto_value, saldo_value):
        saldo_value = "${:,.0f}".format(saldo_value).replace(',', '.')
        saldo.config(text=saldo_value)
        monto_value = re.sub(r'[^\d]', '', str(monto_value))
        monto_value = "${:,.0f}".format(int(monto_value)).replace(',', '.')
        monto.delete(0, tk.END)
        monto.insert(0, monto_value)

    # Primero se restringe el ingreso de caracteres no numéricos y se limita la cantidad de caracteres
    if event.keysym in ("BackSpace", "Delete"):
        if monto.get() == "":
            return "break"
        monto_value = monto.get().replace('$','').replace('.','')
        try:
            if motivo.get() == "Ahorro":
                saldo_value = saldo_value + int(monto_value) - int(monto_value[:-1])
            elif motivo.get() == "Suplemento":
                saldo_value = saldo_value - int(monto_value) + int(monto_value[:-1])
            formatear_e_insertar(monto_value[:-1], saldo_value)
        except:
            if motivo.get() == "Ahorro":
                saldo_value = saldo_value + int(monto_value)
            elif motivo.get() == "Suplemento":
                saldo_value = saldo_value - int(monto_value)
            formatear_e_insertar(123, saldo_value)
            monto.delete(0, tk.END)
        return 'break'
    elif event.keysym == "Tab":
        return
    elif not event.char.isdigit():
        return "break"
    elif len(monto.get()) == 12:
        return "break"
    
    # Formatea el monto ingresado para que se vea mejor en la interfaz
    monto_value = monto.get().replace('$','').replace('.','') + (event.char if event.char.isdigit() else "")

    if motivo.get() == "Ahorro":
        saldo_value = saldo_value + int(monto_value[:-1] if monto.get()!='' else 0) - int(monto_value)
        if saldo_value < 0:
            return "break"
    elif motivo.get() == "Suplemento":
        saldo_value = saldo_value - int(monto_value[:-1] if monto.get()!='' else 0) + int(monto_value)
    
    formatear_e_insertar(monto_value, saldo_value)
    
    return "break"  # Prevent the default behavior of inserting the character twice

def Motivo_Seleccionado(motivo,postre,saldo,monto):

    if monto.get() == "" and motivo.get() != "Bajar":
        return "break"

    postre_value = int(postre.cget("text").replace('$','').replace('.',''))
    saldo_value = int(saldo.cget("text").replace('$','').replace('.',''))
    monto_value = int(monto.get().replace('$','').replace('.','')) if monto.get() != "" else 0

    if motivo.get() != "Bajar":
        monto.config(state="normal")

    if motivo.get() == "Ahorro" and postre_value < saldo_value:
        monto.config(state="normal")
        if postre_value - monto_value < 0:
            saldo.config(text="${:,.0f}".format(postre_value).replace(',', '.'))
            monto.delete(0, tk.END)
        else:
            saldo.config(text="${:,.0f}".format(postre_value - monto_value).replace(',', '.'))
    
    elif motivo.get() == "Suplemento" and postre_value > saldo_value:
        monto.config(state="normal")
        saldo.config(text="${:,.0f}".format(postre_value + monto_value).replace(',', '.'))

    elif motivo.get() == "Bajar":
        monto.delete(0, tk.END)
        monto.insert(0, "${:,.0f}".format(postre_value).replace(',', '.'))
        monto.config(state="disabled")
        saldo.config(text="${:,.0f}".format(0).replace(',', '.'))
    
    Control_Monto_Fondo(monto.master)

def Entrega_Info_Fondo(ID, parent, matriz):
    global valor_previo
    ID_Activo = ID.get()

    if ID_Activo == "":
        for widget in parent.grid_slaves(row=ID.grid_info()["row"]):
            if widget.winfo_class() == "Label":
                widget.config(text="-")

    if ID_Activo in Divisiones:
        ID_Activo = Divisiones[ID_Activo]
    elif ID_Activo in Fondos_Centrales:
        ID_Activo = Fondos_Centrales[ID_Activo]
    elif ID_Activo in Fondos_DIAITT:
        ID_Activo = Fondos_DIAITT[ID_Activo]
    else:
        ID.set(valor_previo)  # Restaura el valor anterior si el ítem no es válido

    info = matriz.loc[matriz['ID_Activo'] == ID_Activo]

    actualizar_info(info, ID, parent)
    Control_Monto_Fondo(parent)

def Control_Monto_Fondo(parent):
    
    # Se obtiene el ID_Activo_Fondo y se verifica que no esté vacío
    ID_Activo_Fondo = parent.grid_slaves(row=parent.grid_size()[1] - 2, column=0)[0]
    if ID_Activo_Fondo.get() == "":
        return "break"

    total = 0
    for widget in parent.grid_slaves():
        if widget.winfo_class() == "Entry" and widget.grid_info()["column"] == 14:
            row = widget.grid_info()["row"]
            motivo_widget = parent.grid_slaves(row=row, column=15)[0]
            motivo = motivo_widget.get()
            monto = widget.get().replace('$', '').replace('.', '')
            if monto:
                monto = int(monto)
                if motivo == "Suplemento":
                    total -= monto
                elif motivo in ["Ahorro", "Bajar"]:
                    total += monto

    Movimiento_Fondo = parent.grid_slaves(row=parent.grid_size()[1] - 2, column=14)[0]
    Motivo_Fondo = parent.grid_slaves(row=parent.grid_size()[1] - 2, column=15)[0]

    if total < 0:
        Motivo_Fondo.set("Suplemento")
    else:
        Motivo_Fondo.set("Ahorro")
    Movimiento_Fondo.config(text="${:,.0f}".format(abs(total)).replace(',', '.'))

    Saldo_Fondo = parent.grid_slaves(row=parent.grid_size()[1] - 2, column=12)[0]
    PostResolucion_Fondo_value = parent.grid_slaves(row=parent.grid_size()[1] - 2, column=10)[0] .cget("text").replace('$','').replace('.','')
    Movimiento_Fondo_value = Movimiento_Fondo.cget("text").replace('$','').replace('.','')

    # Se actualiza el saldo del fondo
    if motivo in ["Ahorro", "Bajar"]:
        Saldo_Fondo_value = int(PostResolucion_Fondo_value) + int(Movimiento_Fondo_value)
    elif motivo == "Suplemento":
        Saldo_Fondo_value = int(PostResolucion_Fondo_value) - int(Movimiento_Fondo_value)
    
    # Se cambia el color del texto si el saldo es negativo
    if Saldo_Fondo_value < 0:
        Saldo_Fondo.config(fg="red")
        Movimiento_Fondo.config(fg="red")
    else:
        Saldo_Fondo.config(fg="black")
        Movimiento_Fondo.config(fg="black")
            
    Saldo_Fondo_value = "${:,.0f}".format(Saldo_Fondo_value).replace(',', '.')   
    Saldo_Fondo.config(text=Saldo_Fondo_value) 

    return "break" # Previne el comportamiento por defecto de insertar el caracter dos veces

def Reglas_Monto(monto, saldo, motivo, parent, event):
    
    Formato_Monto(monto, saldo, motivo, event)
    Control_Monto_Fondo(parent)

    return "break"  # Previne el comportamiento por defecto de insertar el caracter dos veces

def Obtener_Fondos(parent,matriz):

    fondos_combobox = parent.grid_slaves(row=parent.grid_size()[1] - 2, column=0)[0]
    # Obtener a división a la que pertenece el ID_Activo por medio del ID_Solicitud y agregar su fondo al Combobox de los fondos.
    N_Filas = parent.grid_size()[1]-4
    fondos_combobox['values'] = Fondos
    fondos_registrados = list(fondos_combobox['values']).copy()
    lista_Divisiones = list(Divisiones.keys())

    switch = False

    for fila in range(1,N_Filas+1):
        ID_Solicitud = parent.grid_slaves(row=fila, column=2)[0].cget("text")
        if ID_Solicitud == "-":
            continue
        else:
            switch = True
        ID_Division = -int(ID_Solicitud[5:9])
        
        Division = next((key for key, value in Divisiones.items() if value == ID_Division), None)

        if Division and Division not in fondos_registrados:
            for indice, valor in enumerate(fondos_registrados):
                if "---" in valor:
                    if Division not in fondos_registrados:
                        fondos_registrados.insert(indice, Division)
                        fondos_combobox['values'] = fondos_registrados
                    break
                elif lista_Divisiones.index(Division) < lista_Divisiones.index(valor):
                    fondos_registrados.insert(indice, Division)
                    fondos_combobox['values'] = fondos_registrados
                    break

    if "---" in fondos_registrados[0]:
        if switch:
            fondos_combobox.set(fondos_registrados[1])
        else:
            fondos_combobox.set("")
    else:
        fondos_combobox.set(fondos_registrados[0])

    Entrega_Info_Fondo(fondos_combobox,parent,matriz)

def Registrar_Valores(parent,responsable):

    N_Filas = parent.grid_size()[1]-4

    github_url1 = "https://raw.githubusercontent.com/FMorety/SDP-App/refs/heads/Original/SQL-Querys/ID_Evento_Max.sql"
    github_url2 = "https://raw.githubusercontent.com/FMorety/SDP-App/refs/heads/Original/SQL-Querys/ID_Corr_Max.sql"
    response1 = requests.get(github_url1)
    response2 = requests.get(github_url2)

    if response1.status_code == 200 and response2.status_code == 200:
        SQL_Select1 = response1.text.strip()
        SQL_Select2 = response2.text.strip()
    else:
        raise Exception("Error al obtener el archivo SQL desde GitHub")
    
        #Se extrae el ID Solicitud e ID Activo maximo 
    Evento_Max = SQL(SQL_Select1)+1
    ID_Correlativo_Max = SQL(SQL_Select2)

    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for fila in range(1,N_Filas+1):
        ID_Correlativo_Max += 1
        Datos = [];    Datos += [ID_Correlativo_Max];     Datos += [Evento_Max]

        Datos_Fila = parent.grid_slaves(row=fila)
        Datos_Fila = Datos_Fila[::-1]

        for index, widget in enumerate(Datos_Fila):
            
            if index in [1,4,6,8,14,15,16]:
                try:
                    valor_widget = widget.get()
                except:
                    valor_widget = widget.cget("text")
            else:
                continue
                        
            if index == 6:
                valor_widget = responsable
            elif index == 8:
                valor_widget = fecha_hora_actual
            elif index != 4 and valor_widget.isdigit():
                valor_widget = int(valor_widget.replace('$','').replace('.',''))
                
            if index == 14:
                Motivo = parent.grid_slaves(row=fila,column=index+1)[0].get()
                if "Ahorro" in Motivo or "Bajar" == Motivo:
                    valor_widget = -valor_widget

            Datos += [valor_widget]
            print(Datos)




