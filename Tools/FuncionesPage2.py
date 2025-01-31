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
    columna = 0

    print(info) if not info.empty else print("No se encontró información")

    if not info.empty:
        info_dict = info.to_dict('records')[0]
        for key, value in info_dict.items():
            columna += 1
            
            if key == 'ID_Activo':
                continue
            elif key == 'OCO':
                value = int(value)
            elif key == 'Post_Resolucion':
                value = "${:,.0f}".format(float(value))

            for widget in parent.grid_slaves():
                fila_actual = ID.grid_info()["row"]
                if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual and widget.grid_info()["column"] == columna:
                    widget.config(text=value)

                    break
    else:
        for widget in parent.grid_slaves():
                fila_actual = ID.grid_info()["row"]
                if widget.winfo_class() == "Label" and widget.grid_info()["row"] == fila_actual:
                    widget.config(text="-")


    
    