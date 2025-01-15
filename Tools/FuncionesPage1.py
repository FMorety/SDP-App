from datetime import datetime

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import re
import requests

from SQLConnect import SQLConsulta as SQL

Divisiones = {
    "Alameda": 1000,
    "Alonso Ovalle": 2600,
    "Antonio Varas": 800,
    "Arauco": 2500,
    "Concepción": 500,
    "Maipú": 1400,
    "Melipilla": 2400,
    "Nacimiento": 2900,
    "Plaza Norte": 1900,
    "Plaza Oeste": 1200,
    "Plaza Vespucio": 1100,
    "Puente Alto": 1300,
    "Puerto Montt": 2700,
    "San Bernardo": 1800,
    "San Carlos": 900,
    "San Joaquín": 1600,
    "Valparaíso": 400,
    "Villarrica": 2800,
    "Viña del Mar": 600,
    "Ed. Continua": 3000,
    "Casa Central": 100,
    "Liceo Renca": 700,
    "Campus Virtual": 6000
}
Contador2 = 0

def MostrarID(checkbox, Col1, NumCol,Frames):
    if checkbox.get():  # Verificar si el Checkbutton está marcado
        Col1.grid(row=1, column=NumCol, sticky='e',padx=(0,15),pady=0)  # Mostrar la fila adicional
        if NumCol==2:

            #Explicación del código que se ingresa al hacer click en el CheckBox de ID Solicitud

            #                Año          +  "-"  +     División según lo que dice el forms         +   "-"  +   [Ingresar Código]

            texto = str(datetime.now().year)+"-"+str(Divisiones[str(Frames[2].grid_slaves()[4].get())]).zfill(4)+"-"
            Col1.insert(0,texto)

    else:
        Col1.grid_forget()  # Ocultar la fila adicional
        Col1.delete(0,tk.END)

def limitar_caracteres(entry_widget, max_length, EsNumero=0):
    """
    Limita la cantidad de caracteres que se pueden ingresar en un widget Entry.
    
    Args:
    entry_widget (tk.Entry): Widget Entry al que se aplicará la restricción.
    max_length (int): Cantidad máxima de caracteres permitidos.
    """
   
    def validar_entrada(event):
        
        if event.keysym in ("BackSpace", "Delete"):
            if str(datetime.now().year) in str(entry_widget.get()) and len(entry_widget.get())<11:
                return "break"
            else:
                return  # Permite borrar caracteres
        if len(entry_widget.get()) >= max_length:
            # Cancelar entrada si ya se alcanzó el límite
            return "break"
        

        #Parte que revisa si es dígito en caso de que EsNumero = 1
        if EsNumero==1:
            nuevo_texto = event.char
            if not nuevo_texto.isdigit() and event.char not in ("\b", "\x7f"):
                return "break"
            if len(entry_widget.get())==0 and event.char=="0":
                return "break"

    # Asociar la validación al evento de escritura
    entry_widget.bind("<KeyPress>", validar_entrada)

def limitar_caracteres2(entry_widget):
    def validar_entrada(event):
        #Extraer largo del widget, dependiendo del tipo
        if isinstance(entry_widget,Entry):
            largo = entry_widget.get()
        else:
            largo = entry_widget.get("1.0", tk.END)
        
        # Permitir solo letras como primer carácter
        if not event.char.isalpha() and event.char not in ("\b", "\x7f","-") and len(largo)<=2:
            return "break"
    entry_widget.bind("<KeyPress>",validar_entrada)

def Instancias_Disponibles():
    if datetime.now().month >= 10:
        Inst = ["Emergente","Contingencia","Adelanto"]
    else:
        Inst = ["Emergente","Contingencia"]
    return Inst

# Función para formatear el monto cuando se pierde el enfoque
def FormatearNumero(entry_widget,Frames=None):

    global Contador2
    # Función para formatear el monto como moneda (con separación de miles y 2 decimales)
    def format_money(value):
        # Elimina cualquier caracter que no sea un dígito o punto
        value = re.sub(r'[^\d]', '', value)
        if value:
            # Convierte el valor a un número entero y luego lo formatea
            value = int(value)
            # Aplica el formato de moneda con separación de miles
            return f"{value:,}".replace(",", ".")
        return ""  # Devuelve vacío si no hay valor
    
    def validar_out_focus2(event):
        if Frames != None:
            widget_insert = Frames.grid_slaves()[len(Frames.grid_slaves())-3]
            formatted_value = format_money(widget_insert.get())
            widget_insert.delete(0, 'end')
            widget_insert.insert(0, formatted_value)
    
    def validar_out_focus(event):
       global Contador2
       monto_value = entry_widget.get()
       Contador2=1
       if monto_value.strip():
            formatted_value = format_money(monto_value)
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, formatted_value)

    def validar_focusout_final(event):
        validar_out_focus(event)
        validar_out_focus2(event)
   
    def validar_entrada(event):
        global Contador2
        if Contador2 == 1:  # Verifica que Contador2 sea 1 para no ejecutar la función
            return
        elif not event.char.isdigit() and event.char not in ("\b", "\x7f","."):
            return
        elif len(entry_widget.get())==0 and event.char=="0":
            return
        
        widget_insert = Frames.grid_slaves()[len(Frames.grid_slaves())-3]

        if event.keysym in ("BackSpace", "Delete"):
            widget_insert.delete(len(widget_insert.get()) - 1, tk.END)
        else:
            widget_insert.insert(len(widget_insert.get()),event.char)
        


    entry_widget.bind("<KeyPress>", validar_entrada if Frames != None else None)
    entry_widget.bind('<FocusOut>', validar_focusout_final)

def format_money(value):
    if isinstance(value,int):
        return f"{value:,}".replace(",", ".")
    else:
        return

def eliminar_fila(Frame, boton):
    fila_actual = boton.grid_info()["row"]
    columna_actual = boton.grid_info()["column"]
    
    # Eliminar todos los widgets de la fila especificada
    for widget in Frame.grid_slaves():
        try:
            # Verificar si el widget pertenece a la fila actual y a la columna correspondiente
            if widget.grid_info()["row"] == fila_actual and widget.grid_info()["column"] >= columna_actual:
                widget.destroy()
        except tk.TclError:
            # Manejar el caso donde el widget ya ha sido destruido
            continue

    # Reorganizar las filas restantes después de la fila eliminada
    for widget in Frame.grid_slaves():
        try:
            fila_widget = widget.grid_info()["row"]
            columna_widget = widget.grid_info()["column"]
            if fila_widget > fila_actual and columna_widget >= columna_actual:
                widget.grid(row=fila_widget - 1)
            
            if widget.grid_info()["row"]==1 and widget.grid_info()["column"]==3:
                widget.set(widget['values'][datetime.now().month-1])
        except tk.TclError:
            # Manejar el caso donde el widget ya ha sido destruido
            continue

def agregar_fila(Frame,Lista,boton,label,Montoaprobado):
    # Obtener la posición actual del botón
    fila_actual = boton.grid_info()["row"]
    for widget in Frame.grid_slaves():
        if widget.grid_info()["row"] > fila_actual:
            widget.grid(row=fila_actual+2)
    Monto = Entry(Frame,width=22,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10)); Monto.grid(row=fila_actual+1, column=1,sticky="w", padx=(0,5)); FormatearNumero(Monto)
    Monto.bind("<KeyRelease>", lambda e: actualizar_total(Frame, label,Montoaprobado))
    Mes = ttk.Combobox(Frame, values=Lista,width=15,state="readonly"); Mes.grid(row=fila_actual+1,column=2,sticky="ew"); Mes.set(Mes["values"][datetime.now().month -1])
    eliminar = ttk.Button(Frame,text="-",width=3,command=lambda: eliminar_fila(Frame,eliminar)); eliminar.grid(row=fila_actual,column=0,sticky="e")
    boton.grid(row=fila_actual+1)    

def eliminar_item(marco, listamarcos):
    
    #Extrae el título del Item #
    marconuevo = marco.grid_slaves()[::-1];    marcohijo = marconuevo[0];    marcohijonuevo = marcohijo.grid_slaves()[::-1];    Label = marcohijonuevo[1].cget("text")
    
    #Extrae el N° del Item dentro del título y se destruye el Item, actualizando la lista #
    Numero = int(Label[len(Label)-1:])-1
    
    Modificar_marcos = listamarcos.copy(); del Modificar_marcos[0]
    
    #if len(listamarcos)==1:
    #    marco.destroy()
    if marco == listamarcos[-1]:
        marco.destroy()
    else:
        for Frame in Modificar_marcos:
            if Frame.grid_info()['row'] > Numero:

                for Frame2 in Frame.grid_slaves():
                    for widget in Frame2.grid_slaves():
                        try:
                            # Verificar si el widget pertenece a la fila actual y a la columna correspondiente
                            if isinstance(widget,tk.Label) and widget.master.winfo_name() == "!frame":
                                textoLabel = widget.cget("text")
                                NumeroLabel = int(textoLabel[len(textoLabel)-1:])
                                widget.config(text=f"Item {NumeroLabel-1}")
                                marco.destroy()
                        except tk.TclError:
                            # Manejar el caso donde el widget ya ha sido destruido
                            print("Error")
                            continue
                Frame.grid(row=Frame.grid_info()['row']-1)

    del listamarcos[Numero]

def SumaMonto(Frame):
    """Calcula la suma de todos los valores en la columna 2 del Frame dado."""
    suma_monto = 0
    for widget in Frame.grid_slaves():
        try:
            if widget.grid_info()["column"] == 1 and isinstance(widget,Entry):  # Verificar columna 2
                valor = widget.get()
                if valor:  # Verificar que no esté vacío
                    valor_sin_puntos = int(valor.replace('.',''))  # Eliminar puntos y convertir a entero
                    suma_monto += valor_sin_puntos
        except ValueError:
            continue  # Ignorar entradas no válidas
    return f"Total: {suma_monto:,}".replace(",", ".") # Formatear con puntos como separadores

def actualizar_total(Frame, Label_Total, Montoaprobado):
    """
    Actualiza el texto del Label con el total sumado.
    """
    Label_Total.config(text=SumaMonto(Frame))
    if (Montoaprobado.get() == "" and int(Label_Total.cget("text").replace("Total: ","").replace(".","")) != 0) or (Montoaprobado.get() != "" and int(Label_Total.cget("text").replace("Total: ","").replace(".","")) == 0):
        Label_Total.config(fg="red")

    elif Montoaprobado.get() != "" and int(Montoaprobado.get().replace(".","")) != int(Label_Total.cget("text").replace("Total: ","").replace(".","")):
        Label_Total.config(fg="red")
        
    elif int(Label_Total.cget("text").replace("Total: ","").replace(".","")) ==0  and Montoaprobado.get()=="":
        Label_Total.config(fg="black")
    else:
        Label_Total.config(fg="dark green")

def actualizar_Division_ID(entry_widget1,entry_widget2,checkbox):
    
    def validar_click(event):
        if checkbox.get():
            codigo = entry_widget2.get()
            partes = codigo.split("-")
            partes[1] = str(Divisiones[entry_widget1.get()]).zfill(4)
            nuevo_codigo = "-".join(partes)
            entry_widget2.delete(0,tk.END)
            entry_widget2.insert(0,nuevo_codigo)
    entry_widget1.bind("<<ComboboxSelected>>", validar_click)

def limpiar_widgets(Frames,FramesInternos):

    Marcos = Frames.copy(); del Marcos[len(Marcos)-1]
    OCOS = [300,5000,4000,4500,12100]

    for Frame in Marcos:
        for widget in Frame.grid_slaves():
            try:
                if isinstance(widget,Entry):
                        widget.delete(0,tk.END)
                elif isinstance(widget,Text):
                    widget.delete('1.0',tk.END)         
            except:
                continue
    
    MarcoItem = FramesInternos[0]
    
    for Frame in FramesInternos[1:]:
            Frame.destroy()

    # Mantener solo el primer elemento modificando la lista original
    while len(FramesInternos) > 1:
        FramesInternos.pop()
    
    for Frame in MarcoItem.grid_slaves():
        for widget in Frame.grid_slaves():
            try:
                if isinstance(widget,Entry):
                    if widget.grid_info()["row"] == 0:
                        for OCO in OCOS:  # Recorre la lista con índice
                            if str(OCO) in widget.get():  # Verifica si el valor está como subsección
                                widget.delete(0,tk.END)
                                widget.insert(0,OCO)
                    else:
                        widget.delete(0,tk.END)
                elif isinstance(widget,ttk.Combobox) and widget.master.winfo_name() == "!frame4":
                    widget.set(widget['values'][datetime.now().month -1])
                elif isinstance(widget,Label) and "Total: " in widget.cget("text"):
                    widget.config(text="Total: 0",fg="black")

            except:
                continue


    return print("Campos limpiados.")

def obtener_variables(Frames):

    Datos=[]
    Campos_Vacios=False
    p=0

    # Extrae todos los valores de las celdas/objetos visibles (Excepto CheckBox) y los registra en la lista Datos
    for Frame in Frames:
        DarVuelta = []
        for widget in Frame.grid_slaves():
            if isinstance(widget,ttk.Combobox):
                if widget.get()!="":
                    DarVuelta.append(widget.get())                    
                else:
                    Campos_Vacios=True
            elif isinstance(widget, Text):  # Caso específico para Text
                DarVuelta.append(widget.get("1.0", tk.END).strip())  # Obtener todo el texto
            else:
                try:
                    if widget.get()=="": 
                        Campos_Vacios=True
                    else:
                        DarVuelta.append(widget.get())  # Para otros widgets que soportan .get()
                except AttributeError:
                    pass  # Si el widget no tiene .get(), simplemente no lo agregamos
        Datos += DarVuelta[::-1]

    # Mensaje de error por si encuentra campos vacios
    if Campos_Vacios==True:
        return messagebox.showerror("Error",f"Tiene campos sin completar.\nFavor llenar el formulario con todos los campos obligatorios.")
    
    for i in range(len(Datos)):
        texto = Datos[i]
        if texto.isdigit() or texto.replace(".","").isdigit():
            nuevo = int(texto.replace(".",""))
            Datos[i]=nuevo

    if str(datetime.now().year) in Datos[1]:
        p=1
        Division = Datos[2]
    else:
        Division = Datos[1]
        p=0

    return Datos,Division,p

def Registrar_Valores(Frames,FramesInternos,Check_var,Col1):

    # --------------------------------------------------------------------------------------------------------------------------------------------- #

    # Info preeliminar #

    MesesNumero = {
        'Enero': 0,
        'Febrero': 1,
        'Marzo': 2,
        'Abril': 3,
        'Mayo': 4,
        'Junio': 5,
        'Julio': 6,
        'Agosto': 7,
        'Septiembre': 8,
        'Octubre': 9,
        'Noviembre': 10,
        'Diciembre': 11,
    }
    FrameCheckBox = Frames[1]

    github_url = "https://raw.githubusercontent.com/FMorety/SDP-App/refs/heads/main/SQL-Querys/ID_Max.sql"
    response = requests.get(github_url)

    if response.status_code == 200:
        SQL_Select = response.text.strip()
    else:
        raise Exception("Error al obtener el archivo SQL desde GitHub")
    
        #Lista con los datos ingresados en el formulario

    DatosGenerales, Division, p = obtener_variables(Frames)

        #Se extrae el ID Solicitud maximo 
    ID_Solicitud_Max = SQL(SQL_Select)

    # --------------------------------------------------------------------------------------------------------------------------------------------- #


    #Extrae los datos del Item, y distribuye los montos en la Matriz_Planificacion
    for Frame in FramesInternos:

        Matriz_Planificacion = [0,0,0,0,0,0,0,0,0,0,0,0]
        DatosItem, *_ = obtener_variables(Frame.grid_slaves())

        # Restricción de montos ingresados iguales #
        Frame_de_Label = Frame.grid_slaves()[0].grid_slaves()
        Label_Monto = int(Frame_de_Label[len(Frame_de_Label)-1].cget("text").replace("Total: ","").replace(".",""))
        Monto_Aprobado = DatosItem[len(DatosItem)-1]

        if Label_Monto != Monto_Aprobado:
            return (messagebox.showerror(
            "Error: Revisar montos ingresados",
            f"""Por favor, asegurarse de que la casilla 'Total Aprobado' se igual al monto del total acumulado que se indica en la etiqueta de color rojo.
            
        Monto Total Aprobado: {format_money(Monto_Aprobado)}
                   Total Acumulado: {format_money(Label_Monto)}"""), print("No se ejecutó la acción."))   
                    
        # --------------------------------------------------------------------------------------------------------------------------------------------- #

        #Extrae la planificación del monto aprobado y lo distribuye en la Matriz_Planificacion
        for i in range(len(DatosItem)):
            NumeroM = None
            n = (2*i)+1
            if DatosItem[n] in MesesNumero:
                Matriz_Planificacion[MesesNumero[DatosItem[n]]] += DatosItem[n-1]
            else:
                DatosItem.append(   (   next(   (k for k, v in MesesNumero.items() if v == ( datetime.now().month -1 ) ), None )  ).upper()   )
                del DatosItem[:n-1]
                break

        # Unifica los datos y reordena la información para que esté en el orden que sale en la matriz

        DatosItem[len(DatosItem)-2:len(DatosItem)-2] = [1]
        DatosItem[len(DatosItem)-2:len(DatosItem)-2] = DatosItem[:3];       del DatosItem[:3]
        Datos = DatosGenerales+DatosItem

        Datos[len(Datos)-1:len(Datos)-1] = [Datos[2+p]]; del Datos[2+p]
        Datos[len(Datos)-1:len(Datos)-1] = [Datos[2+p]]; del Datos[2+p]
        Datos[len(Datos)-1:len(Datos)-1] = [Datos[0]]; del Datos[0]

        Datos += Matriz_Planificacion

        if p == 0:
            cod_Div = Divisiones[Division]
            Codigo_ID_Solicitud_Nuevo = ["2025-"+str(cod_Div).zfill(4)+"-"+str(ID_Solicitud_Max+1).zfill(4)]
            Datos[0:0]=Codigo_ID_Solicitud_Nuevo
            
        elif p == 1:
            if len(Datos[0]) != 14:
                return (messagebox.showerror("Error: Revisar ID Solicitud ingresada manualmente.",f"Por favor, completar el ID Solicitud con el formato solicitado en la casilla.\n\nFormato del ID Solicitud: {datetime.now().year}-XXXX-XXXX"), print("No se ejecutó la acción."))
            
            elif str(datetime.now().year) in Datos[0] and str(Divisiones[Division]) in Datos[0]:
                Codigo_ID_Solicitud_Nuevo = Datos[0]
                


        # Advertencia de monto ingresado e impresión #
        if Monto_Aprobado > 150000000:
            result = messagebox.askokcancel(
                "Advertencia: Monto elevado",
                "Se ha asignado un 'Monto Total' a la solicitud que supera los $150.000.000 CLP.\n\n¿Desea registrar la solicitud de todas formas?"
            )
            if not result:
                print("Operación cancelada por el usuario.")  # Mensaje en caso de "Cancelar"
                return
            elif result:
                print(Datos)
                
        else:
            print(Datos)
    
    limpiar_widgets(Frames,FramesInternos)


def Sabana_2025(Division,Escuela,Carrera,Subcartera):
    
    github_url = "https://raw.githubusercontent.com/FMorety/SDP-App/refs/heads/main/SQL-Querys/Consulta_Codigos.sql"
    response = requests.get(github_url)

    if response.status_code == 200:
        SQL_Select = response.text.strip()
    else:
        raise Exception("Error al obtener el archivo SQL desde GitHub")
    
    Sabana = SQL(SQL_Select,pandas=True)

    # --------------------------------------------------------------------------------------------------------------------------------------------#

        #Lista de Sedes y diccionario de Sedes

    Sedes = {
        clave: (valor.zfill(2), clave) for clave, valor in Sabana[['Sede', 'Cod_Sede']].drop_duplicates().values
        }
    Sedes['Casa Central'] = ('00','Casa Central'); Sedes['Ed. Continua'] = ('98','Ed. Continua'); Sedes['Liceo Renca'] = ('99','Liceo Renca')

    Lista_Sedes = [Sede[1] for Sede in Sedes.values()];       Lista_Sedes += [Lista_Sedes[17]];      del Lista_Sedes[17]
    Lista_Sedes = sorted(Lista_Sedes[:20]) + Lista_Sedes[20:]

        # Diccionario de escuelas
    
    Escuelas = {
        f"Escuela de {clave}": (valor.zfill(2), f"Escuela de {clave}") 
        for clave, valor in Sabana[['Escuela', 'Cod_Escuela']].drop_duplicates().values
    }
    
        #   Diccionario de carreras

    Carreras = [
        (valor, clave) for clave, valor in Sabana[['Carrera', 'Programa']].drop_duplicates().values
        ]
    
        # Lista de Direcciones

    Direcciones = ["Dirección de Administración, Finanzas, y Financiamiento Estudiantil","Dirección de Desarrollo Online","Dirección de Estudios y Progresión Estudiantil","Dirección de Gestión y Proyectos","Dirección de Investigación Aplicada, Innovación y Transferencia","Dirección de Pastoral y Cultura Cristiana","Dirección de Procesos y Servicios Digitales","Dirección de Servicios de Infraestructura","Dirección de Contraloria","Dirección de Cumplimiento","Dirección de Calidad","Dirección de Tecnología","Dirección de Gobierno de Datos","Dirección General de Admisión, Comunicaciones y Extensión","Dirección General de Desarrollo Estudiantil, Educación Continua y Titulados","Dirección General de Personas","Dirección General de Servicios Digitales","Dirección Juridica","Secretaría General","Subdirección de Procesos Académicos","Subdirección de Sistemas de Desarrollo de Programas","Vicerrectoría Académica"]; Direcciones.sort

    Division.config(values=Lista_Sedes)

    def validar_click_Division(event):

        if Division.get() == "Casa Central":
            Direcciones.append("Operación Sede"); Escuela.config(values=Direcciones); Escuela.set(Escuela['values'][0]) if Escuela.get() in ["Operación Sede","Infraestructura Sede"] else None
            Subcartera.config(values="Corporativo"); Subcartera.set(Subcartera['values'][0])
            Carrera.config(values=Direcciones,state="Enable");  Carrera.set(Escuela.get())
            return
        else:
            Lista_Subcartera = ["Operacional","Disciplinar","Corporativo"]
            Subcartera.config(values=Lista_Subcartera); Subcartera.set(Subcartera['values'][0]) if Subcartera.get() == "Corporativo" else None
            
        
        if event == None:
            Lista_Subcartera = ["Operacional","Disciplinar","Corporativo"]
            Subcartera.config(values=Lista_Subcartera); Subcartera.set(Subcartera['values'][0])
            Carrera.config(state=DISABLED); Carrera.set("Operación Sede")


        if Subcartera.get() != "Disciplinar":
            Escuela.config(values=["Operación Sede","Infraestructura Sede"]); Escuela.set(Escuela['values'][0])
            Carrera.set(str(Escuela.get())); Carrera.config(state=DISABLED)

        
        elif Subcartera.get() == "Disciplinar":

            Lista_Escuelas = set()
            Lista_Carreras = set()

            Cod_Division = Sedes[Division.get() if event != None else 'Alameda'][0]

            for codigo in Carreras:

                if Cod_Division == str(codigo[0][0:2]):
                    Cod_Escuela = str(codigo[0][3:5])
                    Nombre_Escuela = next((escuela[1] for escuela in Escuelas.values() if escuela[0] == Cod_Escuela), None)

                    if Nombre_Escuela:
                        Lista_Escuelas.add(Nombre_Escuela)


            Lista_Escuelas = list(Lista_Escuelas)
            Escuela.config(values=Lista_Escuelas) ;     Escuela.set(Escuela['values'][0]) if Escuela.get() not in Lista_Escuelas else None
            
            Cod_Escuela = next((escuela[0] for escuela in Escuelas.values() if escuela[1] == Escuela.get()),None)

            for codigo in Carreras:
                if Cod_Division == str(codigo[0][0:2]) and Cod_Escuela == str(codigo[0][3:5]):
                        Lista_Carreras.add(codigo[1])

            Lista_Carreras = list(Lista_Carreras);  Lista_Carreras2 = [" ".join([palabra.capitalize() if (len(palabra) > 3 and '/' not in palabra) else palabra.lower() for palabra in s.split()]) for s in Lista_Carreras];     Lista_Carreras2[0:0] = ["Todas"]
            Carrera.config(state="readonly",values=Lista_Carreras2); Carrera.set(Carrera['values'][0]) if Carrera.get() not in Carreras else None

    Division.bind("<<ComboboxSelected>>", validar_click_Division)
    Subcartera.bind("<<ComboboxSelected>>", validar_click_Division)
    Escuela.bind("<<ComboboxSelected>>", validar_click_Division)

    validar_click_Division(event=None)

def Ejecutor_Auto(Ejecutor, MacroAgr, FramesInternos):
    
    EjeOCO = {
        "SEDE": 300,
        "DSI": 500,
        "DGSD": 400,
        "BIB": 450,
        "CC": 1210,
    }
    
    TipodeItems = ["Equipamiento", "Mobiliario", "Tecnología", "Infraestructura"]

    def validar_entrada(event):

        for Frames in FramesInternos:
            OCO = Frames.grid_slaves()[1].grid_slaves()[4]
            Cuenta = Frames.grid_slaves()[1].grid_slaves()[0]
            TipoItem = Frames.grid_slaves()[2].grid_slaves()[4]

            if event == None:
                Ejecutor.set(Ejecutor['values'][0])
                TipoItem.set(TipoItem['values'][0])
                Cuenta.config(state=DISABLED); Cuenta.set("61070000")

            Cod_OCO = str(EjeOCO[Ejecutor.get()])
            OCO.delete(0,tk.END)
            OCO.insert(0,Cod_OCO)

            if Ejecutor.get() == "DSI":
                Cuenta.set(Cuenta['values'][2])
                TipoItem.config(values=["Infraestructura","Mobiliario"]); TipoItem.set(TipoItem['values'][0]) if TipoItem.get() not in TipoItem['values'] else None
            else:
                Cuenta.set(Cuenta['values'][0])
                TipoItem.config(values= TipodeItems if Ejecutor.get() != "DGSD" else ["Tecnología"]); TipoItem.set(TipoItem['values'][0]) if TipoItem.get() not in TipoItem['values'] else None
            
            Cruce_TipoItem_Cuenta(TipoItem,Cuenta,["61070000","61075000","61080000"])
    
    validar_entrada(event=None)
    Ejecutor.bind("<<ComboboxSelected>>",validar_entrada)
    
def Formato_OCO(widget,Ejecutor,event):
    
    EjeOCO = {
        "SEDE": 300,
        "DSI": 500,
        "DGSD": 400,
        "BIB": 450,
        "CC": 1210,
    }

    OCO = widget
    
    Cod_OCO = str(EjeOCO[Ejecutor.get()])


    # Obtener el largo máximo permitido según la condición
    limite = 9 if Ejecutor.get() == "CC" else 8

    # Manejo de teclas de borrado
    if event.keysym in ("BackSpace", "Delete"):
        if len(OCO.get()) <= len(Cod_OCO):
            return "break"  # Bloquear si intenta borrar antes del prefijo
        else:
            return  # Permitir borrar

    # Bloquear caracteres no numéricos
    if not event.char.isdigit():
        return "break"

    # Bloquear si excede el límite de caracteres
    if len(OCO.get()) >= limite:
        return "break"
    
def Cruce_TipoItem_Cuenta(TipoItem_Entry,Cuenta_Entry,lista):

    if TipoItem_Entry.get() in ["Equipamiento","Mobiliario"]:
        Cuenta_Entry.config(state=DISABLED); Cuenta_Entry.set("61070000")
    elif TipoItem_Entry.get() == "Infraestructura":
        Cuenta_Entry.config(state=DISABLED); Cuenta_Entry.set("61080000")
    elif TipoItem_Entry.get() == "Tecnología":
        Cuenta_Entry.config(state="readonly",values=lista); Cuenta_Entry.set(Cuenta_Entry['values'][0])
        