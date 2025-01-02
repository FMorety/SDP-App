from Tools.CrearObj import *
from Tools.FuncionesPage1 import * 
import pandas as pd


def Form_Ingreso_Solicitud(parent):
        
    MesActual = (datetime.now().month)-1
    Marcos=[]
    global Checkbox2_var, Checkbox_var

    # Registrar la función de validación de valor numerico para ciertas celdas #
    Lista_Instancia = Instancias_Disponibles()
            
    ### ---------- Marco1 ---------- ###
    marco1 = LabelFrame(parent,text="Información general",font=("Arial",10,"bold")); marco1.pack(side="top",padx=12,pady=5 ,ipady=5, ipadx=5, fill="x", expand="yes") 

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
    linea = agregar_linea(Frame_Linea,30,0,530,0,"gray",2)

        #CheckBox ID Solicitud#
    Checkbox_var = tk.BooleanVar()
    CheckBox = crear_checkbox(Frame_Top,"Ingreso manual de ID Solicitud",0,Checkbox_var)
    CheckBox.config(command=lambda: MostrarID(Checkbox_var, ID_Solicitud,2,Marcos))

        #ID Solicitud si CheckBox = True#
    ID_Solicitud = crear_entry2(Frame_Top,14)
    limitar_caracteres(ID_Solicitud, 14,1)

        #CheckBox reiteración de ID Solicitud#
    Checkbox2_var = tk.BooleanVar()
    CheckBox2 = crear_checkbox(Frame_Top,"Repetir ID Solicitud",3,Checkbox2_var)
    CheckBox2.config(command=lambda: MostrarID(Checkbox2_var, Repeticiones,5,Marcos))

        # Repeticiones # Numero de lineas con el mismo ID Solicitud si CheckBox2 = True #
    Repeticiones = crear_entry2(Frame_Top,2)
    limitar_caracteres(Repeticiones,1,1)

        #División#
    Division = crear_combobox(Frame_Mid,"División:",[],0,0,15)
    actualizar_Division_ID(Division,ID_Solicitud,Checkbox_var)

        #Ejecutor#
    Lista_Ejecutor = ["SEDE","CC","DSI","DGSD","BIB","SegInt"]
    Ejecutor = crear_combobox(Frame_Mid,"Ejecutor:",Lista_Ejecutor,0,2,7).set(Lista_Ejecutor[0])

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
    Lista_JusSol = ["Avance de malla", "Renovación, actualización o mejoramiento", "Reposición por daños o incidentes", "Requerimiento normativa externa"]
    JusSol = crear_combobox(Frame_Bottom, "Justificación Solicitud:",Lista_JusSol,4,0).set(Lista_JusSol[1])

    # --------------------------------------------------------------------------------------------------------------------------------------------#
        
        # ---------- Listados provenientes de SQL ---------- #    
    
    Sabana_2025(Division,UnidadEscuela,Carrera,Subcartera);    Division.set(Division['values'][0]);       UnidadEscuela.set(UnidadEscuela['values'][0])

    # --------------------------------------------------------------------------------------------------------------------------------------------#


    ### ---------- Marco2 ---------- ###
    marco2 = LabelFrame(parent,text="Información ítem",font=("Arial",10,"bold")); marco2.pack(padx=12,pady=(0,5) ,ipady=5, ipadx=5, fill="x", expand=True) 

    canvas = Canvas(marco2,height=235)
    scrollbar = Scrollbar(marco2, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Configuración del canvas y scrollbar
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


    ### ---------- Frames ---------- ###
    Frame_Right = crear_Frame(scrollable_frame,0,5); Frame_Right.grid(row=0,column=1,padx=(0,0),sticky="ew")
    Frame_Left = crear_Frame(scrollable_frame,0,5); Frame_Left.grid(row=0,column=0,padx=(75,10),sticky="ew")
    Frame_MontoMes = crear_Frame(scrollable_frame,1,15); Frame_MontoMes.grid(column=0,columnspan=2,padx=(10,0),sticky="e")
    Marcos += [Frame_Right,Frame_Left,Frame_MontoMes]

    ### ---------- Campos ---------- ###

        #OCO#
    OCO = crear_entry(Frame_Left, "*OCO:",0,0,15)
    limitar_caracteres(OCO,9,1)
    
        #CECO#
    CECO = crear_entry(Frame_Left, "CECO:",1,0,15)
    limitar_caracteres(CECO,15,1)
    
        #Cuenta#
    Cuenta = crear_combobox(Frame_Left, "Cuenta:", [61070000,61075000,61080000],2,0,12); Cuenta.set(Cuenta['values'][0])

        #Tipo ítem#
    Lista_TipoItem = ["Equipamiento", "Mobiliario", "Tecnología", "Infraestructura"]
    TipoItem = crear_combobox(Frame_Right, "Tipo de ítem:",Lista_TipoItem,0,0,14).set(Lista_TipoItem[0])

        #Ítem#
    Item = crear_entry(Frame_Right, "Ítem Solicitud:",1,0,17)
    Item.grid(padx=(0,7)); limitar_caracteres2(Item)

        #Cantidad Aprobada#
    Cantidad = crear_entry(Frame_Right, "# Aprobada:",2,0,3)
    limitar_caracteres(Cantidad,3,1)

        #Monto Total Aprobado#
    Label_MontoTotal = Label(Frame_MontoMes,text="Monto Total Aprobado",font=("Arial",9,"bold")); Label_MontoTotal.grid(row=0,column=0,sticky="ew",padx=(15,0))
    MontoTotal = Entry(Frame_MontoMes,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10)); MontoTotal.grid(row=1, column=0,sticky="ew",padx=(15,0)); FormatearNumero(MontoTotal,Frame_MontoMes)
    MontoTotal.bind("<KeyRelease>", lambda e: actualizar_total(Frame_MontoMes, Label_Total))
    
        #Monto Aprobado#
    Label_Monto = Label(Frame_MontoMes,text="Monto",anchor="center",font=("Arial",9,"bold")).grid(row=0,column=2,sticky='ew')  
    Monto = Entry(Frame_MontoMes,width=22,bd=1, highlightthickness=1, highlightbackground="gray",font=("Open Sans",10)); Monto.grid(row=1, column=2,sticky="w", padx=(0,5)); FormatearNumero(Monto)
    Monto.bind("<KeyRelease>", lambda e: actualizar_total(Frame_MontoMes, Label_Total))

        #Mes#
    Lista_Mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    Label_Mes = Label(Frame_MontoMes,text="Mes",anchor="center",font=("Arial",9,"bold")).grid(row=0,column=3,sticky="ew")
    Mes = ttk.Combobox(Frame_MontoMes, values=Lista_Mes,width=15,state="readonly") ; Mes.grid(row=1,column=3,sticky="ew")
    Mes.set(Lista_Mes[MesActual])
    
        #Etiqueta para visualizar el total de lo que corresponde a cada mes
    Label_Total= Label(Frame_MontoMes, text="Total: 0", anchor="w", font=("Arial", 9, "bold")); Label_Total.grid(row=2,column=2,pady=(0,0))
        
        #Botón para agregar mes de imputación
    AgregarMonto = ttk.Button(Frame_MontoMes,text="+",width=3,command=lambda: agregar_fila(Frame_MontoMes,Lista_Mes,AgregarMonto,Label_Total)); AgregarMonto.grid(row=1,column=1,sticky="e",padx=(45,0))

    # --------------------------------------------------------------------------------------------------------------------------------------------#

    # ---------- Botones ---------- #
    Frame_Botones = Frame(parent); Frame_Botones.pack(side="bottom")

    Limpiar = Button(Frame_Botones,text="Limpiar",command=lambda: limpiar_widgets(Marcos),width=10)
    Limpiar.grid(row=0,column=0,sticky="n",padx=(0,20))

    Registrar = Button(Frame_Botones,text="Registrar",command=lambda: Registrar_Valores(Marcos,Checkbox_var,ID_Solicitud,Checkbox2_var,Repeticiones),width=10)
    Registrar.grid(row=0,column=1,sticky="n",padx=(20,0))
    
    # --------------------------------------------------------------------------------------------------------------------------------------------#