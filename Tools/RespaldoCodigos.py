# Para usarlos en Formulario para crear los campos con una def distinta
def crear_campos():
    entry_nombre = crear_entry(frame1, "Nombre:", 0, 0)
    combobox_categoria = crear_combobox(frame1, "Categoría:", ["A", "B", "C"], 1, 0)
    button_guardar = crear_button(frame1, "Guardar", 2, 0, command=guardar_datos)
    
    # Crear un CheckButton
    var_check = tk.BooleanVar()
    checkbutton_aceptar = crear_checkbutton(frame1, "Aceptar términos", 3, 0, var_check)
    
    # Crear un Text
    text_descripcion = crear_text(frame1, 4, 0)


### ---------- Tabla (TreeView) ---------- ###   

        columnas = ("col1", "col2", "col3", "col4", "col5", "col6","col7", "col8", "col9", "col10",
                    "col11", "col12", "col13", "col14", "col15", "col16", "col17", "col18", "col19", "col20",
                    "col21", "col22", "col23", "col24", "col25", "col26", "col27", "col28", "col29", "col30")
        encabezados = {"col1": "ID", "col2": "ID Solicitud", "col3": "Division", "col4": "Unidad o Escuela", "col5": "Carrera Destino", "col6": "Nombre Solicitud",
                    "col7": "Desc. Solicitud", "col8": "Justif. Solicitud", "col9": "Tipo Ítem", "col10": "Ítem", "col11": "Cantidad Aprobada", "col12": "Tipo de Inversión",
                    "col13": "OCO", "col14": "CECO", "col15": "Cuenta", "col16": "Monto Aprobado", "col17": "Ejecutor", "col18": "Instancia de Apr.",
                    "col19": "Ene", "col20": "Febrero", "col21": "Mar", "col22": "Abr", "col23": "May", "col24": "Jun", "col25": "Jul", "col26": "Ago",
                    "col27": "Sep", "col28": "Oct", "col29": "Nov", "col30": "Dic"}
        dimensiones = {"height": 15, "widths": [100, 150, 200]}

        TablaFormulario = configurar_treeview(self.Page1,columnas,encabezados,dimensiones)

        insertar_datos(TablaFormulario, results)

        # Empaquetar el Treeview
        TablaFormulario.pack(fill="both", expand=True)
    

# Función de validación para aceptar solo números
"""def validar_entrada(P):
    if P == "" or P.isdigit():  # Permitir vacío o solo números
        return True
    else:
        return False"""

#Respaldo código formulario
    """# Registrar la función de validación de valor numerico para ciertas celdas #
        vcmd = (self.window.register(EsNumero), '%P')
        Lista_Instancia = self.Instancias_Disponibles()

        ### ---------- Título --------------- ###
        titulo = Label(self.Page1, text="Formulario de Emergentes y/o Contingencias",anchor="center",fg="black",font=("Comic Sans",12,"bold"))
        titulo.pack(padx=0,pady=10)
                
        ### ---------- Marco ---------- ###
        marco1 = LabelFrame(self.Page1,text="Información general",font=("Arial",10,"bold")); marco1.pack(side="top",padx=12,pady=5 ,ipady=5, ipadx=5, fill="both", expand="yes") 
        marco2 = LabelFrame(self.Page1, text="Información ítem", font=("Arial", 10, "bold")); marco2.pack(side="bottom",padx=12, pady=5, ipady=5, ipadx=5, fill="both", expand="yes")
        
        ### ---------- Frames Marco1 ---------- ###   

        Frame_Instancia = crear_Frame(marco1,0); Frame_Instancia.grid(padx=130)
        Frame_Linea = crear_Frame(marco1,1,(15,10))
        Frame_Top = crear_Frame(marco1,2); Frame_Top.grid(padx=100)
        Frame_Mid = crear_Frame(marco1,3); Frame_Mid.grid(padx=20)
        Frame_Bottom = crear_Frame(marco1,4); Frame_Bottom.grid(padx=62,pady=5)


        ### ---------- Campos ---------- ###

            #Instancia#
        self.Instancia = crear_combobox(Frame_Instancia,"Instancia de aprobación:",Lista_Instancia,0,0,12)
        self.linea = agregar_linea(Frame_Linea,30,0,530,0,"gray",2)

            #CheckBox ID Solicitud#
        self.checkbox_var = tk.BooleanVar()
        self.CheckBox = crear_checkbox(Frame_Top,"Ingreso manual de ID Solicitud",0,self.checkbox_var)
        self.CheckBox.config(command=lambda: MostrarID(self.checkbox_var, self.ID_Solicitud,2))

            #ID Solicitud si CheckBox = True#
        self.ID_Solicitud = crear_entry2(Frame_Top,14)
        limitar_caracteres(self.ID_Solicitud, 14)

            #CheckBox reiteración de ID Solicitud#
        self.checkbox2_var = tk.BooleanVar()
        self.CheckBox2 = crear_checkbox(Frame_Top,"Repetir ID Solicitud",3,self.checkbox2_var)
        self.CheckBox2.config(command=lambda: MostrarID(self.checkbox2_var, self.Repeticiones,5))

            # Repeticiones # Numero de lineas con el mismo ID Solicitud si CheckBox2 = True #
        self.Repeticiones = crear_entry2(Frame_Top,2)
        self.Repeticiones.config(validate="key",validatecommand=vcmd)

            #División#
        Lista_Division = ["Alameda", "Alonso Ovalle", "Antonio Varas", "Arauco","Concepción","Liceo Renca","Maipú","Melipilla","Nacimiento","Plaza Norte","Plaza Oeste","Plaza Vespucio","Puente Alto","Puerto Montt","San Bernardo","San Carlos","San Joaquin","Valparaíso","Villarrica","Viña del Mar","Casa Central"]
        self.Division = crear_combobox(Frame_Mid,"División:",Lista_Division,0,0,15)

            #Ejecutor#
        Lista_Ejecutor = ["SEDE","CC","DSI","DGSD","BIB","SegInt"]
        self.Ejecutor = crear_combobox(Frame_Mid,"Ejecutor:",Lista_Ejecutor,0,2,7)

            #Subcartera
        Lista_Subcartera = ["Disciplinar","Operacional","Corporativo"]
        self.Subcartera = crear_combobox(Frame_Mid,"Subcartera:",Lista_Subcartera,0,4,12)
        
            #Unidad o Escuela#
        Lista_UnidadEscuela = ["Escuela de Administración y Negocios","Escuela de Comunicación","Escuela de Construcción","Escuela de Diseño","Escuela de Gastronomía","Escuela de Informática y Telecomunicaciones","Escuela de Ingeniería y Recursos Naturales","Escuela de Salud","Escuela de Turismo y Hospitalidad","Operación Sede","Infraestructura Sede","Dirección de Administración, Finanzas, y Financiamiento Estudiantil","Dirección de Desarrollo Online","Dirección de Estudios y Progresión Estudiantil","Dirección de Gestión y Proyectos","Dirección de Investigación Aplicada, Innovación y Transferencia","Dirección de Pastoral y Cultura Cristiana","Dirección de Procesos y Servicios Digitales","Dirección de Servicios de Infraestructura","Dirección de Contraloria","Dirección de Cumplimiento","Dirección de Calidad","Dirección de Tecnología","Dirección de Gobierno de Datos","Dirección General de Admisión, Comunicaciones y Extensión","Dirección General de Desarrollo Estudiantil, Educación Continua y Titulados","Dirección General de Personas","Dirección General de Servicios Digitales","Dirección Juridica","Secretaría General","Subdirección de Procesos Académicos","Subdirección de Sistemas de Desarrollo de Programas","Vicerrectoría Académica"]
        self.UnidadEscuela = crear_combobox(Frame_Bottom,"Unidad o Escuela:",Lista_UnidadEscuela,0,0)

            #Carrera de Destino#
        self.Carrera = crear_combobox(Frame_Bottom,"Carrera de destino:",[],1,0)

            #Nombre Solicitud#
        self.NomSol = crear_entry(Frame_Bottom,"Nombre Solicitud:",2,0)

            #Descripción Solicitud#
        self.DesSol = crear_text(Frame_Bottom,"Descripción Solicitud:",3,0)

            #Justificación Solicitud#
        Lista_JusSol = ["Avance de malla", "Renovación, actualización o mejoramiento", "Reposición por daños o incidentes", "Requerimiento normativa externa"]
        self.JusSol = crear_combobox(Frame_Bottom, "Justificación Solicitud:",Lista_JusSol,4,0).config(state="normal")

            #Tipo ítem#
        #Lista_TipoItem = ["Equipamiento", "Mobiliario", "Tecnología", "Infraestructura"]
        #self.TipoItem = crear_combobox(Frame_Bottom, "Tipo de ítem:",Lista_TipoItem,0,0,14)

            #Ítem#
        #self.Item = crear_entry(Frame_Bottom, "Ítem Solicitud:", 1,0,17)

            #Cantidad Aprobada#
        self.Cantidad = crear_entry(Frame_Bottom, "Cantidad Aprobada:",5,0,3)
        EsNumero(self.Cantidad)
        self.Cantidad.grid(sticky="w")

            #OCO#
        #self.OCO = crear_entry(Frame_Bottom, "*OCO:",0,0,15)
        #limitar_caracteres(self.OCO,9); self.OCO.config(validate="key",validatecommand=vcmd); self.OCO.grid(padx=(2,12))
        
            #CECO#
        #self.CECO = crear_entry(Frame_Bottom, "CECO:",0,2,15)
        #limitar_caracteres(self.CECO,15); self.CECO.config(validate="key",validatecommand=vcmd); self.CECO.grid(padx=(2,12))
        
            #Cuenta#
        #self.Cuenta = crear_combobox(Frame_Bottom, "Cuenta:", [61070000,61075000,61080000],0,4,12)
        #self.Cuenta.grid(padx=(2,0))
        
        
            #Mes#
        #Lista_Mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        #self.Mes = crear_combobox(Frame_Bottom, "Mes:",Lista_Mes, 3, 2, 20)

            #Monto Aprobado#
        #Label_Monto = Label(Frame_Bottom,text="Monto Aprobado: ",font=("Arial",9,"bold")).grid(row=1,column=2,sticky='e',padx=(15,0),pady=(10,0))  
        #self.Monto = Entry(Frame_Bottom,width=22,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10))
        #self.Monto.grid(row=1, column=3, padx=0, pady=(10, 0))
        #self.Monto.bind('<FocusOut>', lambda event: FormatearNumero(event, self.Monto))

    def Instancias_Disponibles(self):
        if datetime.now().month >= 10:
            Inst = ["Emergente","Contingencia","Adelanto"]
        else:
            Inst = ["Emergente","Contingencia"]
        return Inst"""