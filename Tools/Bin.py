    # Mensaje de error por si no se cumplen las restricciones
    LabelMonto = int(Frames[len(Frames)-1].grid_slaves()[1].cget("text").replace("Total: ","").replace(".",""))
    MontoTotal = Datos[13+p]
    if LabelMonto != MontoTotal:
        return (messagebox.showerror(
            "Error: Revisar montos ingresados",
            f"""Por favor, asegurarse de que la casilla 'Monto Total Aprobado' tenga el mismo monto que el total acumulado que se indica en la etiqueta de color rojo.
            
        Monto Total Aprobado: {format_money(MontoTotal)}
                   Total Acumulado: {format_money(LabelMonto)}"""), print("No se ejecutó la acción."))   
    if MontoTotal>150000000:
        result = messagebox.askyesno("Advertencia: Monto elevado","Se ha asignado un 'Monto Total' a la solicitud que supera los $150.000.000 CLP.\n\n¿Desea registrar la solicitud de todas formas?")
        if not result:
            return