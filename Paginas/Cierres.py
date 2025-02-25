import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from datetime import datetime

from Tools.FuncionesPage2 import Data_Bitacora,Divisiones
from SQLConnect import SQLActualizar, SQLConsulta as SQL, funcion_subida_bitacora

def Form_Cierres(parent,responsable):

    Matriz_CAPEX = Data_Bitacora()

    marco = tk.LabelFrame(parent,text="Seguimiento Cierre OCOS",font=("Arial",9,"bold")); marco.pack(side="top",padx=12,pady=8 ,ipady=5, ipadx=5, fill="both", expand="yes")

    Label_OCO = tk.Label(marco, text="OCO",font=("Arial",9,"bold")); Label_OCO.grid(row=0,column=0,pady=(13,7),padx=5)
    OCO = tk.Entry(marco,bd=1, highlightthickness=1, highlightbackground="gray",width=15,justify="center",font=("Open Sans",10)); OCO.grid(row=1,column=0,pady=2,padx=(20,10))
    OCO.bind("<KeyPress>",lambda event: FormatoOCO(OCO,event))

    Label_Estado = tk.Label(marco, text="Estado Cierre",font=("Arial",9,"bold")); Label_Estado.grid(row=0,column=1,pady=(13,7),padx=10)
    Estado = ttk.Combobox(marco, values=["Por Solicitar","Solicitado","Cerrado"], state="readonly",width=10); Estado.grid(row=1,column=1,pady=2,padx=5); Estado.set("Por Solicitar")

    Registrar = tk.Button(marco,text="Registrar",width=8, command= lambda : Registrar_Cierres(responsable,OCO,Estado,Matriz_CAPEX));Registrar.grid(row=1,column=2,pady=2,padx=10)

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
        
def Registrar_Cierres(responsable,oco,estado,matriz):

    # Información para registro de cierres en bitacora
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
    ID_Correlativo_Max = SQL(SQL_Select2)+1

    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Obtener el menor ID_Activo
    OCO = oco.get()
       
    # --------------------------------------------------------------------------------------------------------- #

    if OCO[0] == "1" and len(OCO) != 9:
        return messagebox.showerror("Error: OCO","Ingrese un código de OCO válido. La OCO debe tener 9 digitos.")
    elif OCO[0] != "1" and len(OCO) != 8:
        return messagebox.showerror("Error: OCO","Ingrese un código de OCO válido. La OCO debe tener 8 digitos.")
    
    Validacion_Cierre = SQL(f"SELECT [OCO] FROM [Subdireccion de Proyectos BBDD].[dbo].[Cierres] WHERE [OCO] = {OCO}")
    Validacion_Matriz = matriz[matriz['OCO'] == int(OCO)].empty
    Validacion_Estado = SQL(f"SELECT [Estado_Cierre] FROM [Subdireccion de Proyectos BBDD].[dbo].[Cierres] WHERE [OCO] = {OCO}")
    print(Validacion_Estado)

    if Validacion_Estado == estado.get():
        return messagebox.showerror("Error: Estado","El estado de cierre seleccionado ya se encuentra registrado en la base de datos.")

    if not Validacion_Cierre and Validacion_Matriz:
        return messagebox.showerror("Error: OCO","La OCO señalada no se encuentra registrada en la Matriz CAPEX.")
    elif not Validacion_Cierre and not Validacion_Matriz:
        menor_id_activo = int(matriz.loc[matriz['OCO'] == int(OCO), 'ID_Activo'].min())
        Datos = [ID_Correlativo_Max, Evento_Max, menor_id_activo, int(OCO), responsable, fecha_hora_actual, 0, f"Estado: {estado.get()}", f"{responsable} ha actualizado el estado de cierre de la OCO {OCO}"]
        cierre_nuevo = messagebox.askyesno("OCO no encontrada.","La OCO señalada no se encontró en el listado de OCOs en proceso de cierre. ¿Desea incluir esta nueva OCO al listado?")
        if cierre_nuevo:
            try:
                Nombre_Solicitud = matriz.loc[matriz['OCO'] == int(OCO), 'Nombre_Solicitud'].values[0]
                ID_Division = matriz.loc[matriz['OCO'] == int(OCO), 'ID_Solicitud'].values[0][5:9]
                Division = next(   (Nombre for Nombre, id in Divisiones.items() if id == -int(ID_Division)), None ) if ID_Division.isdigit() else messagebox.showerror("Error.", "Error.")

            except IndexError:
                return messagebox.showerror("Error: OCO","La OCO señalada no se encuentra registrada en la Matriz CAPEX. Favor de registrar la OCO registrada en la matriz.")
    
            SQLActualizar(f"INSERT INTO [Subdireccion de Proyectos BBDD].[dbo].[Cierres] ([OCO],[Division],[Nombre_Solicitud],[Estado_Cierre]) VALUES ({OCO},'{Division}','{Nombre_Solicitud}','{estado.get()}')")
            funcion_subida_bitacora(Datos)
            return messagebox.showinfo("Cierre Registrado","La OCO ha sido registrada en el listado de cierres.")
        else:
            return
    else:
        SQL_Update = f"UPDATE [Subdireccion de Proyectos BBDD].[dbo].[Cierres] SET [Estado_Cierre] = '{estado.get()}' WHERE [OCO] = {int(OCO)}"
        SQLActualizar(SQL_Update)
        funcion_subida_bitacora(Datos)
        print(SQL_Update)
        return messagebox.showinfo("Cierre Registrado","El estado de cierre ha sido registrada en el listado.")