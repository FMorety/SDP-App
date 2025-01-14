
    """
    
    if len(Datos)==16:
        cod_Div = Divisiones[Division]
        Codigo_ID_Solicitud_Nuevo = ["2025-"+str(cod_Div).zfill(4)+"-"+str(ID_Solicitud_Max+1).zfill(4)]
        Datos[0:0]=Codigo_ID_Solicitud_Nuevo
        limpiar_widgets(Frames)
                
    elif len(Datos)==17:
        if isinstance(Datos[0],str):
            if len(Datos[0]) != 14:
                return (messagebox.showerror("Error: Revisar ID Solicitud ingresada manualmente.",f"Por favor, completar el ID Solicitud con el formato solicitado en la casilla.\n\nFormato del ID Solicitud: {datetime.now().year}-XXXX-XXXX"), print("No se ejecutó la acción."))
            
            elif str(datetime.now().year) in Datos[0] and str(Divisiones[Division]) in Datos[0]:
                Codigo_ID_Solicitud_Nuevo = Datos[0]
                limpiar_widgets2(Frames)
            else:
                return (messagebox.showerror("Error",f"Revisar ID Solicitud ingresada manualmente.\nFavor de revisar que el año o el código de la división sean los correctos."), print("No se ejecutó la acción."))

        elif isinstance(Datos[0],int):
            if Contador==0 and Datos[0]>1:
                cod_Div = Divisiones[Datos[1]]
                Codigo_ID_Solicitud_Nuevo = "2025-"+str(cod_Div).zfill(4)+"-"+str(ID_Solicitud_Max+1).zfill(4)
                for widget in FrameCheckBox.grid_slaves():
                    if isinstance(widget,Entry):
                        widget.delete(0,tk.END); widget.insert(0,Datos[0]-1)
                Datos[0] = Codigo_ID_Solicitud_Nuevo
                limpiar_widgets2(Frames)
                Contador=1
                
            elif Contador!=0 and Datos[0]>1:
                cod_Div = Divisiones[Datos[1]]
                Codigo_ID_Solicitud_Nuevo = "2025-"+str(cod_Div).zfill(4)+"-"+str(ID_Solicitud_Max).zfill(4)
                for widget in FrameCheckBox.grid_slaves():
                    if isinstance(widget,Entry):
                        widget.delete(0,tk.END); widget.insert(0,Datos[0]-1)
                Datos[0] = Codigo_ID_Solicitud_Nuevo
                limpiar_widgets2(Frames)

            elif Datos[0]==1:
                cod_Div = Divisiones[Datos[1]]
                Codigo_ID_Solicitud_Nuevo = "2025-"+str(cod_Div).zfill(4)+"-"+str(ID_Solicitud_Max).zfill(4)
                Datos[0] = Codigo_ID_Solicitud_Nuevo
                Check_var.set(0)
                MostrarID(Check_var, Col1,5)
                limpiar_widgets2(Frames)

    elif len(Datos)==18:
            if len(Datos[0]) != 14:
                return (messagebox.showerror("Error: Revisar ID Solicitud ingresada manualmente.",f"Por favor, completar el ID Solicitud con el formato solicitado en la casilla.\n\nFormato del ID Solicitud: {datetime.now().year}-XXXX-XXXX"), print("No se ejecutó la acción."))
            elif str(datetime.now().year) in Datos[0] and str(Divisiones[Division]) in Datos[0]:
                if Datos[1]>1:
                    for widget in FrameCheckBox.grid_slaves():
                        if isinstance(widget,Entry) and widget.grid_info()["column"]>2:
                            widget.delete(0,tk.END); widget.insert(0,Datos[1]-1)
                if Datos[1]==1:
                    Check_var.set(0); Check_var2.set(0)
                    MostrarID(Check_var, Col1,5,Frames); MostrarID(Check_var2, Col2,5,Frames)
                del Datos[1]
                limpiar_widgets2(Frames)
            else:
                return (messagebox.showerror("Error",f"Revisar ID Solicitud ingresada manualmente.\nFavor de revisar que el año o el código de la división sean los correctos."), print("No se ejecutó la acción."))"""

    # Crear la consulta SQL sin especificar columnas
       
    Lista_a_subir=Datos+Matriz_Planificacion
    
    placeholders = ", ".join("?" for _ in range(len(Lista_a_subir)))
    SQL_Insert = f"INSERT INTO [SDPrueba].[dbo].[Matriz] VALUES ("
    
    SQL(SQL_Insert,lista=Lista_a_subir)