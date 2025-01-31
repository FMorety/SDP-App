import re
import requests
from SQLConnect import SQLConsulta as SQL

def Data_Bitacora():
    
    github_url = "https://raw.githubusercontent.com/FMorety/SDP-App/refs/heads/Original/SQL-Querys/Consulta_Codigos.sql"
    response = requests.get(github_url)

    if response.status_code == 200:
        SQL_Select = response.text.strip()
    else:
        raise Exception("Error al obtener el archivo SQL desde GitHub")
    
    Data = SQL(SQL_Select,pandas=True)

    print(Data)