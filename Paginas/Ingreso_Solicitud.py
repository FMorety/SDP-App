from Tools.CrearObj import *
from Tools.FuncionesPage1 import * 


def Form_Ingreso_Solicitud(parent,window):
        
    MesActual = (datetime.now().month)-1
    Marcos=[]
    global Checkbox_var

    # Registrar la función de validación de valor numerico para ciertas celdas #
    Lista_Instancia = Instancias_Disponibles()
            
    ### ---------- Marco1 ---------- ###
    marco1 = LabelFrame(parent,text="Información general",font=("Arial",10,"bold")); marco1.grid(padx=12,pady=(5,5) ,ipady=5, ipadx=5,column=0,row=0,sticky="n") 

    ### ---------- Frames Marco1 ---------- ###   

    Frame_Instancia = crear_Frame(marco1,0); Frame_Instancia.grid(sticky="n",padx=20)
    Frame_Linea = crear_Frame(marco1,1,(15,10))
    Frame_Top = crear_Frame(marco1,2); Frame_Top.grid(sticky="n",padx=20)
    Frame_Mid = crear_Frame(marco1,3); Frame_Mid.grid(sticky="n",padx=20)
    Frame_Bottom = crear_Frame(marco1,4); Frame_Bottom.grid(sticky="n",pady=5,padx=20)

    Marcos += [Frame_Instancia,Frame_Top,Frame_Mid,Frame_Bottom]

    ### ---------- Campos ---------- ###

        #Instancia#
    Instancia = crear_combobox(Frame_Instancia,"Instancia de aprobación:",Lista_Instancia,0,0,12).set(Lista_Instancia[0])  
    linea = agregar_linea(Frame_Linea,10,0,400,0,"gray",2)

        #CheckBox ID Solicitud#
    Checkbox_var = tk.BooleanVar()
    CheckBox = crear_checkbox(Frame_Top,"Ingreso manual de ID Solicitud",0,Checkbox_var)
    CheckBox.config(command=lambda: MostrarID(Checkbox_var, ID_Solicitud,2,Marcos))

        #ID Solicitud si CheckBox = True#
    ID_Solicitud = crear_entry2(Frame_Top,14)
    limitar_caracteres(ID_Solicitud, 14,1)

        #División#
    Division = crear_combobox(Frame_Mid,"División:",[],0,0,15)
    actualizar_Division_ID(Division,ID_Solicitud,Checkbox_var)

        #Ejecutor#
    Lista_Ejecutor = ["SEDE","CC","DSI","DGSD","BIB"]
    Ejecutor = crear_combobox(Frame_Mid,"Ejecutor:",Lista_Ejecutor,0,2,7)

        #Subcartera
    Subcartera = crear_combobox(Frame_Mid,"Subcartera:",[],0,4,12)
    
        #Unidad o Escuela#
    
    UnidadEscuela = crear_combobox(Frame_Bottom,"Unidad o Escuela:",[],0,0)

        #Carrera de Destino#
    Carrera = crear_combobox(Frame_Bottom,"Carrera de destino:",[],1,0)

        #Nombre Solicitud#
    NomSol = crear_entry(Frame_Bottom,"Nombre Solicitud:",2,0); limitar_caracteres2(NomSol)

        #Descripción Solicitud#
    DesSol = crear_text(Frame_Bottom,"*Descripción Solicitud:",3,0); limitar_caracteres2(DesSol)

        #Justificación Solicitud#
    Lista_MacroAgr = ["Accesibilidad Universal","Biblioteca","Desarrollo Informático","DIAITT","Infraestructura Crítica","Renovación Tecnológica 2020","Sala de Lactancia","Seguridad Integral"]
    MacroAgrupacion = crear_combobox(Frame_Bottom, "Macroagrupación:",Lista_MacroAgr,4,0)

    # --------------------------------------------------------------------------------------------------------------------------------------------#
        
        # ---------- Listados provenientes de SQL ---------- #    
    
    Sabana_2025(Division,UnidadEscuela,Carrera,Subcartera);    Division.set(Division['values'][0]);       UnidadEscuela.set(UnidadEscuela['values'][0])

    # --------------------------------------------------------------------------------------------------------------------------------------------#


    ### ---------- Marco2 ---------- ###
    marco2 = LabelFrame(parent,text="Información ítem",font=("Arial",10,"bold")); marco2.grid(padx=0,pady=(5,5) ,ipady=5, ipadx=5, column=1,row=0,sticky="n") 

    canvas = Canvas(marco2)
    scrollbar = Scrollbar(marco2, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Configuración del canvas y scrollbar
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set,height=305)

    canvas.pack(side="left", fill="both", expand=True,padx=(0,15))
    scrollbar.pack(side="right", fill="y")

    # Agrega el scrollable_frame con todo lo que va dentro.     Y aparte agrega una nueva lista de Marcos, util para crear multiples lineas en la BBDD con los multiples items#
    MarcosInternos = []

    ### ---------- Frames ---------- ###

    MarcoItem1 = crear_Frame(scrollable_frame,0,0); MarcoItem1.grid(row=0,sticky="n")
    Frame_Titulo = crear_Frame(MarcoItem1,0,0); Frame_Titulo.grid(row=0,column=0,columnspan=2,sticky="n")
    Frame_Right = crear_Frame(MarcoItem1,1,5); Frame_Right.grid(column=1,padx=(0,15),sticky="ew")
    Frame_Left = crear_Frame(MarcoItem1,1,5); Frame_Left.grid(column=0,padx=(15,10),sticky="ew")
    Frame_MontoMes = crear_Frame(MarcoItem1,2,15); Frame_MontoMes.grid(column=0,columnspan=2,padx=(20,0),sticky="n")

    MarcosInternos += [MarcoItem1]


    ### ---------- Campos ---------- ###

        #Título Item#
    Label_Item = Label(Frame_Titulo,text="Item 1",anchor="center",font=("Times New Roman",11,"bold")); Label_Item.grid(row=0,column=0,sticky="n")

        #OCO#
    OCO = crear_entry(Frame_Left, "*OCO:",0,0,15)
    OCO.bind("<KeyPress>",lambda event: Formato_OCO(OCO,Ejecutor,event))
    
        #CECO#
    CECO = crear_entry(Frame_Left, "CECO:",1,0,15)
    limitar_caracteres(CECO,15,1)
    
        #Cuenta#
    Lista_Cuenta = [61070000,61075000,61080000]
    Cuenta = crear_combobox(Frame_Left, "Cuenta:", Lista_Cuenta,2,0,12); Cuenta.set(Cuenta['values'][0])

        #Tipo ítem#
    Lista_TipoItem = ["Equipamiento", "Mobiliario", "Tecnología", "Infraestructura"]
    TipoItem = crear_combobox(Frame_Right, "Tipo de ítem:",Lista_TipoItem,0,0,14)
    TipoItem.bind("<<ComboboxSelected>>",lambda event: Cruce_TipoItem_Cuenta(TipoItem,Cuenta,Lista_Cuenta))
        
        #Ítem#
    Item = crear_entry(Frame_Right, "Ítem Solicitud:",1,0,17)
    Item.grid(padx=(0,7)); limitar_caracteres2(Item)

        #Monto Total Aprobado#
    Label_MontoTotal = Label(Frame_Right,text="Total Aprobado:",font=("Arial",9,"bold")); Label_MontoTotal.grid(row=2,column=0,sticky="ew",padx=(0,2),pady=(10,0))
    MontoTotal = Entry(Frame_Right,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10),width=14); MontoTotal.grid(row=2, column=1,sticky="ew",padx=(0,7),pady=(10,0))
    FormatearNumero(MontoTotal,Frame_MontoMes);     MontoTotal.bind("<KeyRelease>", lambda e: actualizar_total(Frame_MontoMes, Label_Total, MontoTotal))

        #Etiqueta para visualizar el total de lo que corresponde a cada mes
    Label_Total= Label(Frame_MontoMes, text="Total: 0", anchor="w", font=("Arial", 9, "bold")); Label_Total.grid(row=2,column=1,pady=(0,0))
    
        #Monto Aprobado#
    Label_Monto = Label(Frame_MontoMes,text="Monto",anchor="center",font=("Arial",9,"bold")).grid(row=0,column=1,sticky='ew')  
    Monto = Entry(Frame_MontoMes,width=22,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10)); Monto.grid(row=1, column=1,sticky="w", padx=(0,5))
    FormatearNumero(Monto);    Monto.bind("<KeyRelease>", lambda e: actualizar_total(Frame_MontoMes, Label_Total,MontoTotal))

        #Mes#
    Lista_Mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    Label_Mes = Label(Frame_MontoMes,text="Mes",anchor="center",font=("Arial",9,"bold")).grid(row=0,column=2,sticky="ew")
    Mes = ttk.Combobox(Frame_MontoMes, values=Lista_Mes,width=15,state="readonly") ; Mes.grid(row=1,column=2,sticky="ew")
    Mes.set(Lista_Mes[MesActual])

        
        #Botón para agregar mes de imputación
    AgregarMonto = ttk.Button(Frame_MontoMes,text="+",width=3,command=lambda: agregar_fila(Frame_MontoMes,Lista_Mes,AgregarMonto,Label_Total,MontoTotal)); AgregarMonto.grid(row=1,column=0,sticky="e",padx=(0,0))

    # --------------------------------------------------------------------------------------------------------------------------------------------#

    # ---------- Botones ---------- #

    Frame_Botones = Frame(parent); Frame_Botones.grid(row=1,column=0,columnspan=2,sticky="n",pady=5)

    Limpiar = Button(Frame_Botones,text="Limpiar",command=lambda: limpiar_widgets(Marcos,MarcosInternos),width=10)
    Limpiar.grid(row=0,column=0,sticky="n",padx=(0,20))

    Registrar = Button(Frame_Botones,text="Registrar",command=lambda: Registrar_Valores(Marcos,MarcosInternos,Checkbox_var,ID_Solicitud),width=10)
    Registrar.grid(row=0,column=1,sticky="n",padx=(20,20))

    Nuevo_Item = Button(Frame_Botones,text="Nuevo Item",command=lambda: Frame_de_Item(scrollable_frame,MarcosInternos,Ejecutor),width=10)
    Nuevo_Item.grid(row=0,column=2,sticky="n",padx=(20,0))

        # ---------- Automatización OCO/Cuenta/Equipamiento ---------- #    

    Ejecutor_Auto(Ejecutor, MacroAgrupacion, MarcosInternos)
    
    # --------------------------------------------------------------------------------------------------------------------------------------------#
