# a chambear fabian, dijiste que no comentarios entonces suerte
# att: el diseñador del backend (Erick)
import tkinter as tk
from backend import *
from tkinter import ttk, messagebox

def registro_front():
    resultado = registrar_venta(ventas,producto.get(),cantidad.get(),precio.get())
    mensaje_registro.set(resultado["mensaje"])
def ventas_dia():
    resultado = ver_ventas_dia(ventas)
    tabla_dia.delete(*tabla_dia.get_children())
    for venta in resultado["ventas"]:
        tabla_dia.insert("", "end", values=(venta["id"], venta["producto"], venta["cantidad"], venta["subtotal"]))
    total_dia.set("Total: " + str(resultado["total"]))
    resultado_mas_vendido = producto_mas_vendido(ventas)
    if resultado_mas_vendido["ok"] == True:
        mensaje_mas_vendido.set(f" el producto mas vendido fue {(resultado_mas_vendido["producto"])} y se vendio {str(resultado_mas_vendido["cantidad"])}")
    else:
        mensaje_mas_vendido.set(resultado_mas_vendido["mensaje"])
def ventas_semana():
    resultado = resumen_semanal(ventas)
    tabla_semanal.delete(*tabla_semanal.get_children())
    for venta in resultado["ventas"]:
        tabla_semanal.insert("", "end", values=(venta["fecha"], venta["producto"], venta["cantidad"], venta["subtotal"]))
    total_semanal.set("Total: " + str(resultado["total"]))
def eliminar_id():
    resultado = eliminar_venta(ventas, int(id_eliminar.get()))
    mensaje_eliminar.set(resultado["mensaje"])
def editar_id():
    resultado = editar_venta(ventas, int(id_editar.get()), campo.get(), nuevo_valor.get())
    mensaje_editar.set(resultado["mensaje"])
def limpiar_todo():
    confirmar = messagebox.askyesno("confirmacion", "¿estás seguro?")
    if confirmar == True:
        resultado = limpiar_todo(ventas)
        mensaje_formateo.set(resultado["mensaje"])
root = tk.Tk()
root.title("Sistema de ventas")
root.state("zoomed")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

frame_registrar = tk.Frame(notebook)
notebook.add(frame_registrar, text="Registrar venta")
producto_label = tk.Label(frame_registrar, text="producto")
producto_label.grid(row=0, column=0)
producto = tk.Entry(frame_registrar)
producto.grid(row=0, column=1)
cantidad_label = tk.Label(frame_registrar, text="cantidad")
cantidad_label.grid(row=1, column=0)
cantidad = tk.Entry(frame_registrar)
cantidad.grid(row=1, column=1)
precio_label = tk.Label(frame_registrar, text="precio")
precio_label.grid(row=2, column=0)
precio = tk.Entry(frame_registrar)
precio.grid(row=2, column=1)
registrarbtn = tk.Button(frame_registrar, text="Registrar", command=registro_front)
registrarbtn.grid(row=3, column=1)
mensaje_registro = tk.StringVar()
tk.Label(frame_registrar, textvariable=mensaje_registro).grid(row=4, column=1)

frame_ventas_dia = tk.Frame(notebook)
notebook.add(frame_ventas_dia, text="Ver ventas del día")
tabla_dia = ttk.Treeview(frame_ventas_dia, columns=("id", "producto", "cantidad", "subtotal"), show="headings")
tabla_dia.heading("id", text="ID")
tabla_dia.heading("producto", text="PRODUCTO")
tabla_dia.heading("cantidad", text="CANTIDAD")
tabla_dia.heading("subtotal", text="SUBTOTAL")
tabla_dia.pack()
mensaje_mas_vendido = tk.StringVar()
tk.Label(frame_ventas_dia, textvariable=mensaje_mas_vendido).pack()
total_dia = tk.StringVar()
tk.Label(frame_ventas_dia, textvariable=total_dia).pack()
tk.Button(frame_ventas_dia, text="actualizar", command=ventas_dia).pack()

frame_semanal = tk.Frame(notebook)
notebook.add(frame_semanal, text="Resumen semanal")
tabla_semanal = ttk.Treeview(frame_semanal, columns=("fecha", "producto", "cantidad", "subtotal"), show="headings")
tabla_semanal.heading("fecha", text="FECHA")
tabla_semanal.heading("producto", text="PRODUCTO")
tabla_semanal.heading("cantidad", text="CANTIDAD")
tabla_semanal.heading("subtotal", text="SUBTOTAL")
tabla_semanal.pack()
total_semanal = tk.StringVar()
tk.Label(frame_semanal, textvariable=total_semanal).pack()
tk.Button(frame_semanal, text="actualizar", command=ventas_semana).pack()

frame_editar = tk.Frame(notebook)
notebook.add(frame_editar, text="Editar / Eliminar")
tk.Label(frame_editar, text="ID a eliminar").grid(row=0, column=0)
id_eliminar = tk.Entry(frame_editar)
id_eliminar.grid(row=0, column=1)
mensaje_eliminar = tk.StringVar()
tk.Label(frame_editar, textvariable=mensaje_eliminar).grid(row=1, column=1)
tk.Button(frame_editar, text="eliminar", command=eliminar_id).grid(row=2, column=1)
tk.Label(frame_editar, text="ID a editar").grid(row=3, column=0)
id_editar = tk.Entry(frame_editar)
id_editar.grid(row=3, column=1)
tk.Label(frame_editar, text="campo que desea editar").grid(row=4, column=0)
campo = ttk.Combobox(frame_editar, values=["producto", "cantidad", "precio"], state="readonly")
campo.grid(row=4, column=1)
tk.Label(frame_editar, text="ingrese el nuevo valor").grid(row=5, column=0)
nuevo_valor = tk.Entry(frame_editar)
nuevo_valor.grid(row=5, column=1)
tk.Button(frame_editar, text="editar", command=editar_id).grid(row=6, column=1)
mensaje_editar = tk.StringVar()
tk.Label(frame_editar, textvariable=mensaje_editar).grid(row=7, column=1)

frame_config = tk.Frame(notebook)
notebook.add(frame_config, text="Configuración")
mensaje_formateo = tk.StringVar()
tk.Label(frame_config, textvariable=mensaje_formateo).grid(row=0)
tk.Button(frame_config, text="Borrar todo", command=limpiar_todo).grid(row=1)

root.mainloop()
