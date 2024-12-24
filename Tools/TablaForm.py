# Archivo separado: treeview_module.py

import tkinter as tk
from tkinter import ttk

def configurar_treeview(tabla_padre, columnas, encabezados, dimensiones):
    # Crear frame contenedor para el TreeView
    frame = ttk.Frame(tabla_padre)
    frame.pack(fill=tk.BOTH, expand=True)

    # Scrollbars
    x_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
    y_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    
    tree = ttk.Treeview(
        frame,
        columns=columnas,
        show="headings",
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set,
    )
    
    x_scroll.config(command=tree.xview)
    y_scroll.config(command=tree.yview)

    x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)

    # Configuración de columnas
    for col, ancho in zip(columnas, dimensiones.get("widths", [])):
        tree.heading(col, text=encabezados[col])
        tree.column(col, width=ancho, anchor=tk.CENTER, stretch=False)  # stretch=False fija el ancho inicial

    return tree

def insertar_datos(tree, datos):
    for item in datos:
        tree.insert("", tk.END, values=item)

def limpiar_treeview(tree):
    for row in tree.get_children():
        tree.delete(row)