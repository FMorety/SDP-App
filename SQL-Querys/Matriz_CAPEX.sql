SELECT 
    ID_Activo, ID_Solicitud, OCO,  Nombre_Solicitud, Item,
    (Enero + Febrero + Marzo + Abril + Mayo + Junio + Julio + Agosto + Septiembre + Octubre + Noviembre + Diciembre)
    AS Post_Resolucion,
    (Enero + Febrero + Marzo + Abril + Mayo + Junio + Julio + Agosto + Septiembre + Octubre + Noviembre + Diciembre)
    AS Post_Resolucion2

FROM [Subdireccion de Proyectos BBDD].[dbo].[Matriz_CAPEX_Regular]