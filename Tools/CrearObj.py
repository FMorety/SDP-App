import tkinter as tk
from tkinter import ttk

def crear_entry(parent, label_text, row, column,width1=45):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"bold"))
    label.grid(row=row, column=column, sticky='e', padx=(0,2), pady=(10,0))
    entry = tk.Entry(parent,bd=1, highlightthickness=1, highlightbackground="gray",width=width1)
    entry.grid(row=row, column=column+1, sticky="w",padx=(0,0), pady=(10,0))
    return entry

def crear_entry2(parent, width):
    entry = tk.Entry(parent ,width=width,bd=1, highlightthickness=1, highlightbackground="gray")
    return entry

def crear_combobox(parent, label_text, options, row, column,width1=42,estado="readonly"):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"bold"))
    label.grid(row=row, column=column, sticky='e', padx=(0,2), pady=(10,0))
    combobox = ttk.Combobox(parent, values=options,width=width1,state=estado)
    combobox.grid(row=row, column=column+1, padx=(0,7), pady=(10,0))
    return combobox

def crear_checkbox(parent, label_text, columns, variable):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"italic")).grid(row=1,column=columns,sticky="e",padx=0,pady=0)
    checkbutton = tk.Checkbutton(parent,
                                 variable=variable)
    checkbutton.grid(row=1,column=columns+1, padx=0, pady=0)
    return checkbutton

def crear_text(parent, label_text, row, column, height=2, width=45):
    label = tk.Label(parent, text=label_text,font=("Arial",9,"bold"))
    label.grid(row=row, column=column, sticky='ne', padx=(0,2), pady=(10,0))
    text = tk.Text(parent, height=height, width=width,bd=1, highlightthickness=1, highlightbackground="gray",font=("Segoe UI",8))
    text.grid(row=row, column=column+1, sticky="w",padx=0, pady=(10,0), ipady=10)
    return text

def crear_Frame(parent,rows,pad=0):
    frame = tk.Frame(parent)
    frame.grid(row=rows,column=0,sticky="ew",pady=pad)
    return frame

def agregar_linea(parent, x1, y1, x2, y2, color="black", grosor=1):

    canvas = tk.Canvas(parent, height=abs(y2 - y1), width=abs(x2 - x1), bg=parent["bg"], highlightthickness=0)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor)
    canvas.grid(sticky="n")
    return canvas