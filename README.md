# 🛒 Sistema de Registro de Ventas
> **Backend desarrollado por:** Erick\
> **Frontend a cargo de:** Fabian Alejandro\
> Ingeniería de Software — Proyecto personal colaborativo

-----
## 📋 Descripción
Sistema de gestión de ventas desarrollado en Python. Permite registrar, consultar, editar y eliminar ventas de forma local. Todos los datos se persisten automáticamente en un archivo `memoria.json`, lo que significa que sobreviven al cierre del programa.

Este repositorio contiene el **backend completo y listo**. El frontend en tkinter está siendo desarrollado por Fabian Alejandro por separado.

-----
## 🗂️ Estructura del proyecto
~~~
sistema-ventas/
├── backend.py       # Lógica de negocio — toda la lógica interna del sistema
├── main.py          # Interfaz de usuario — trabajo de Fabian Alejandro (tkinter)
├── memoria.json     # Base de datos local (se genera automáticamente)
└── README.md        # Este archivo
~~~

-----
## ⚙️ Requisitos
- Python 3.x
- No requiere instalación de librerías externas. Todas las dependencias (`json`, `datetime`, `timedelta`) vienen incluidas con Python.
- Para el frontend: `tkinter` (incluido con Python en Windows y Mac. En Linux: `sudo apt-get install python3-tk`)
-----
## 🚀 Cómo ejecutar
~~~ bash
python main.py
~~~
> ⚠️ `main.py` es responsabilidad del frontend. Mientras no esté implementado, el backend puede probarse importando las funciones directamente desde `backend.py`.

-----
## 🧠 API del backend
Todas las funciones están en `backend.py`. Fabian las importa así:
~~~ python
from backend import *
~~~

O de forma explícita:
~~~ python
from backend import ventas, registrar_venta, ver_ventas_dia, eliminar_venta, editar_venta, producto_mas_vendido, resumen_semanal, formatear_programa
~~~

-----
### `cargar_datos()`
Carga las ventas desde `memoria.json` al iniciar. Se llama automáticamente al importar `backend.py`.
~~~ python
# Se ejecuta solo al importar, no necesita llamarse manualmente
ventas = cargar_datos()
~~~

-----
### `registrar_venta(ventas, producto, cantidad, precio)`
Registra una nueva venta y la guarda en `memoria.json`.
~~~ python
resultado = registrar_venta(ventas, "pan integral", "3 paquetes", "5.000")
# → {"ok": True, "mensaje": "Venta registrada exitosamente."}
~~~

|Parámetro|Tipo|Ejemplo|
| :-: | :-: | :-: |
|`ventas`|`list`|La lista global de ventas|
|`producto`|`str`|`"pan integral"`|
|`cantidad`|`str` o `int`|`"3 paquetes"` o `3`|
|`precio`|`str` o `int`|`"5.000"` o `5000`|
> ✅ `cantidad` acepta texto como `"3 paquetes"` — extrae el número automáticamente.\
> ✅ `precio` acepta separadores de miles como `"5.000"` o `"5,000"`.

-----
### `ver_ventas_dia(ventas)`
Retorna todas las ventas del día actual con sus subtotales y el total acumulado.
~~~ python
resultado = ver_ventas_dia(ventas)
# → {
#     "ventas": [
#         {"id": 1, "producto": "pan", "cantidad": 3, "subtotal": 15000},
#         {"id": 2, "producto": "leche", "cantidad": 2, "subtotal": 8000}
#     ],
#     "total": 23000
# }
~~~

-----
### `eliminar_venta(ventas, id_eliminar)`
Elimina una venta por su ID.
~~~ python
resultado = eliminar_venta(ventas, 3)
# → {"ok": True,  "mensaje": "Venta eliminada exitosamente."}
# → {"ok": False, "mensaje": "No se encontró una venta con ese ID."}
~~~
> ⚠️ **Fabian:** Mostrar confirmación visual antes de llamar esta función.

-----
### `editar_venta(ventas, id_editar, campo, nuevo_valor)`
Edita un campo específico de una venta existente.
~~~ python
resultado = editar_venta(ventas, 1, "producto", "pan tajado")
resultado = editar_venta(ventas, 1, "cantidad", "5 paquetes")
resultado = editar_venta(ventas, 1, "precio", "4.500")
# → {"ok": True,  "mensaje": "Venta editada exitosamente."}
# → {"ok": False, "mensaje": "No se encontró una venta con ese ID."}
# → {"ok": False, "mensaje": "Campo no válido."}
~~~

|`campo`|Descripción|
| :-: | :-: |
|`"producto"`|Nombre del producto|
|`"cantidad"`|Unidades vendidas|
|`"precio"`|Precio por unidad|

-----
### `producto_mas_vendido(ventas)`
Retorna el producto con más unidades vendidas en el día actual.
~~~ python
resultado = producto_mas_vendido(ventas)
# → {"ok": True,  "producto": "pan integral", "cantidad": 9}
# → {"ok": False, "mensaje": "No se han registrado ventas hoy."}
~~~

-----
### `resumen_semanal(ventas)`
Retorna todas las ventas de los últimos 7 días con el total acumulado.
~~~ python
resultado = resumen_semanal(ventas)
# → {
#     "ventas": [
#         {"fecha": "2026-03-22", "producto": "pan", "cantidad": 3, "subtotal": 15000},
#         {"fecha": "2026-03-25", "producto": "leche", "cantidad": 2, "subtotal": 8000}
#     ],
#     "cantidad_ventas": 2,
#     "total": 23000
# }
~~~

-----
### `formatear_programa()`
Borra todas las ventas del archivo `memoria.json`.
~~~ python
resultado = formatear_programa()
# → {"ok": True, "mensaje": "Todas las ventas han sido borradas."}
~~~
> ⚠️ **Fabian:** ten en mente dos cosas importantes al llamar esta función:
>
> 1. Mostrar confirmación visual antes de llamarla.
> 1. Ejecutar `ventas.clear()` después de llamarla para limpiar la lista en memoria también. Si no, los datos borrados del JSON van a volver a escribirse la próxima vez que se registre una venta.
-----
## 🗃️ Estructura de los datos
Cada venta se almacena en `memoria.json` con el siguiente formato:
~~~ json
{
    "id": 1,
    "producto": "pan integral",
    "cantidad": 3,
    "precio": 5000,
    "fecha": "2026-03-28"
}
~~~

|Campo|Tipo|Descripción|
| :-: | :-: | :-: |
|`id`|`int`|Identificador único autoincremental|
|`producto`|`str`|Nombre del producto en minúsculas|
|`cantidad`|`int`|Unidades vendidas|
|`precio`|`int`|Precio por unidad en pesos colombianos|
|`fecha`|`str`|Fecha en formato `YYYY-MM-DD`|

-----
## 📌 Guía de integración para Fabian Alejandro
### Cómo manejar los retornos `ok: True / False`
Todas las funciones retornan un diccionario con `"ok"` indicando si la operación fue exitosa. Úsalo para mostrar mensajes al usuario:
~~~ python
resultado = eliminar_venta(ventas, id_seleccionado)

if resultado["ok"]:
    mostrar_mensaje_exito(resultado["mensaje"])  # ventana verde
else:
    mostrar_mensaje_error(resultado["mensaje"])  # ventana roja
~~~
### Cómo mostrar las ventas del día en una tabla
~~~ python
resultado = ver_ventas_dia(ventas)

for venta in resultado["ventas"]:
    tabla.insert("", "end", values=(
        venta["id"],
        venta["producto"],
        venta["cantidad"],
        f"{venta['subtotal']:,}"
    ))

total_label.config(text=f"Total: {resultado['total']:,}")
~~~
### Flujo recomendado al iniciar `main.py`
~~~ python
from backend import ventas, registrar_venta, ver_ventas_dia  # etc.

# ventas ya viene cargado desde backend.py
# no necesitas llamar cargar_datos() manualmente
~~~

-----
## 👥 Equipo

|Rol|Nombre|Responsabilidad|
| :-: | :-: | :-: |
|Backend|Erick|Lógica de negocio, persistencia de datos, API interna|
|Frontend|Fabian Alejandro|Interfaz gráfica con tkinter, experiencia de usuario|

-----
## 📚 Tecnologías

|Tecnología|Uso|
| :-: | :-: |
|Python 3|Lenguaje principal|
|`json`|Persistencia de datos local|
|`datetime` / `timedelta`|Manejo y comparación de fechas|
|`tkinter`|Interfaz gráfica (frontend)|

