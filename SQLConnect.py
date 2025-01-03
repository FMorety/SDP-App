import pyodbc
import pandas as pd
from tkinter import messagebox

def SQLConsulta(Query,lista=[],pandas=False):


    server = 'CCDNBA12021461\SQLEXPRESS'  # Ejemplo: 'localhost' o '192.168.1.100'
    database = 'SDPrueba'  # Ejemplo: 'mi_base_de_datos'
    username = 'Admin'  # Tu nombre de usuario
    password = 'duoc2025.'  # Tu contraseña

    # Crear la cadena de conexión
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 18 for SQL Server}};'
                        f'SERVER={server};'
                        f'DATABASE={database};'
                        f'UID={username};'
                        f'PWD={password};'
                        f'TrustServerCertificate=yes')

   #Query como la consulta SQL predefinida.
   
    if pandas==True:
        Sabana = pd.read_sql(Query,conn)
        conn.close()
        return Sabana
    else:
        cursor = conn.cursor()

    try:
    
        # Ejecutar la consulta SQL

        # Confirmar cambios en caso de inserción, actualización o eliminación
        if Query.strip().lower().startswith(('insert')):
            for i in range(len(lista)):
                item = str(lista[i])
                if i==0:
                    Query += f"'{item}'"
                else:
                    if isinstance(lista[i],int):
                        Query += f", {item}"
                    elif isinstance(lista[i],str):
                        Query += f", '{item}'"
            Query += ")"
            print(Query)
            cursor.execute(Query)
            conn.commit()
            messagebox.showinfo("Resultado","La información fue subida con éxito.")

        # Recuperar resultados en caso de consultas SELECT
        elif Query.strip().lower().startswith('select'):
            cursor.execute(Query)
            results = cursor.fetchall()
            messagebox.showinfo("Resultado","La consulta fue realizada con éxito.")
            return int(results[0][0])
                     
    except pyodbc.Error as e:
        messagebox.showinfo("Resultado",f"Error al ejecutar la consulta. Revisar código. {e}")

    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conn.close()



