SELECT 
	MAX(
        CAST(
            SUBSTRING([ID_Solicitud], CHARINDEX('-', [ID_Solicitud], CHARINDEX('-', [ID_Solicitud]) + 1) + 1, 4) AS INT
            )
        ) AS Num_Solicitud
FROM [SDPrueba].[dbo].[Matriz]