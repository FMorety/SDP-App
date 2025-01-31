SELECT 
    ID_Activo, ID_Solicitud, OCO,  Nombre_Solicitud, Item,
    (Enero + Febrero + Marzo + Abril + Mayo + Junio + Julio + Agosto + Septiembre + Octubre + Noviembre + Diciembre)
    AS Total_Anual

FROM [Subdireccion de Proyectos BBDD].[dbo].[Matriz_CAPEX_Regular]