import json
from datetime import datetime, timedelta
import os

def cargar_datos():
    for archivo in ["memoria.json", "memoria.tmp"]:
        try:
            with open(archivo, "r") as file:
                ventas = json.load(file)
                if isinstance(ventas, list):
                    hubo_cambios = False
                    for i, venta in enumerate(ventas):
                        if "id" not in venta:
                            venta["id"] = i+1
                            hubo_cambios = True
                    if hubo_cambios:
                        guardar_datos(ventas)
                    return ventas
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    return []

def guardar_datos(ventas):
    try: 
        with open("memoria.tmp", "w") as file:
            json.dump(ventas, file)

        os.replace("memoria.tmp", "memoria.json")
    except Exception as e:
        if os.path.exists("memoria.tmp"):
            os.remove("memoria.tmp")
        return {"ok": False, "mensaje": f"Error al guardar los datos: {e}"}
    return {"ok": True}

ventas = cargar_datos()

def buscar_venta_id(ventas, id_buscar):
    for venta in ventas:
        if venta["id"] == id_buscar:
            return venta
    return None

def registrar_venta(ventas, producto, cantidad, precio):
    producto = producto.strip().lower()
    if not producto: 
        return {"ok": False, "mensaje": "El nombre del producto no puede estar vacío."}

    try:
        cantidad = int(str(cantidad).split()[0])
    except (ValueError, IndexError): 
        return {"ok": False, "mensaje": "La cantidad debe ser un número válido."}
    try:
        precio = int(str(precio).replace(".", "").replace(",", ""))
    except (ValueError, IndexError):
        return {"ok": False, "mensaje": "El precio debe ser un número válido."}

    if cantidad <= 0:
        return {"ok": False, "mensaje": "La cantidad debe ser mayor que cero."}
    if precio <= 0:
        return {"ok": False, "mensaje": "El precio debe ser mayor que cero."}
    
    if ventas:
        nuevo_id = max(venta["id"] for venta in ventas)+1
    else:
        nuevo_id = 1

    venta = {
        "id": nuevo_id,
        "producto": producto,
        "cantidad": cantidad,
        "precio": precio,
        "fecha": datetime.now().strftime("%Y-%m-%d")
    }
    ventas.append(venta)
    resultado = guardar_datos(ventas)
    if not resultado["ok"]:
        ventas.pop()
        return resultado    
    return {"ok": True, "mensaje": "Venta registrada exitosamente."}

def ver_ventas_dia(ventas):
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    total = 0
    ventas_hoy = []

    for venta in ventas:
        if venta["fecha"] == fecha_hoy:
            subtotal = venta["cantidad"] * venta["precio"]
            total += subtotal
            ventas_hoy.append({
                "id": venta["id"],
                "producto": venta["producto"],
                "cantidad": venta["cantidad"],
                "subtotal": subtotal
            })

    return {"ventas": ventas_hoy, "total": total}
    
def limpiar_todo(ventas):
    resultado = guardar_datos([])
    if not resultado["ok"]:
        return resultado
    ventas.clear()
    return {"ok": True, "mensaje": "Todas las ventas han sido borradas."}

def eliminar_venta(ventas, id_eliminar):    
    venta_encontrada = buscar_venta_id(ventas, id_eliminar)

    if venta_encontrada:
        ventas.remove(venta_encontrada)
        resultado = guardar_datos(ventas)
        if not resultado["ok"]:
            ventas.append(venta_encontrada)
            return resultado
        return {"ok": True, "mensaje": "Venta eliminada exitosamente."}
    else:
        return {"ok": False, "mensaje": "No se encontró una venta con ese ID. Intente de nuevo."}

def editar_venta(ventas, id_editar, campo, nuevo_valor):
    venta_encontrada = buscar_venta_id(ventas, id_editar)
        
    if not venta_encontrada:
        return{"ok": False, "mensaje": "No se encontró una venta con ese ID. Intente de nuevo."}
    
    if campo == "producto":
        nuevo_producto = str(nuevo_valor).strip().lower()
        if not nuevo_producto:
            return {"ok": False, "mensaje": "El nombre del producto no puede estar vacío."}
        venta_encontrada["producto"] = nuevo_producto
    elif campo == "cantidad":
        try:
            nueva_cantidad = int(str(nuevo_valor).split()[0])
        except (ValueError, IndexError): 
            return {"ok": False, "mensaje": "La cantidad debe ser un número válido."}
        if nueva_cantidad <= 0:
            return {"ok": False, "mensaje": "La cantidad debe ser mayor que cero."}
        venta_encontrada["cantidad"] = nueva_cantidad 
    elif campo == "precio":
        try:
            nuevo_precio = int(str(nuevo_valor).replace(".", "").replace(",", ""))
        except ValueError:
            return {"ok": False, "mensaje": "El precio debe ser un número válido."}
        if nuevo_precio <= 0:
            return {"ok": False, "mensaje": "El precio debe ser mayor que 0."}
        venta_encontrada["precio"] = nuevo_precio
    else:
        return {"ok": False, "mensaje": "Campo no válido. Los campos editables son: producto, cantidad, precio."}
    resultado = guardar_datos(ventas)
    if not resultado["ok"]:
        return resultado
    return {"ok": True, "mensaje": "Venta editada exitosamente."}

def resumen_semanal(ventas):
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    total = 0
    cantidad_ventas = 0
    ventas_semana = []

    for venta in ventas:
        fecha_venta = datetime.strptime(venta["fecha"], "%Y-%m-%d")
        if fecha_venta >= hace_7_dias:
            subtotal = venta["cantidad"] * venta["precio"]
            total += subtotal
            cantidad_ventas += 1
            ventas_semana.append({
                "fecha": venta["fecha"],
                "producto": venta["producto"],
                "cantidad": venta["cantidad"],
                "subtotal": subtotal
            })

    return {"ventas": ventas_semana,
            "total": total,
            "cantidad_ventas": cantidad_ventas}

def producto_mas_vendido(ventas):
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    conteo = {}
    
    for venta in ventas:
        if venta["fecha"] == fecha_hoy:
            producto = venta["producto"]
            cantidad = venta["cantidad"]
            if producto in conteo:
                conteo[producto] += cantidad
            else:
                conteo[producto] = cantidad
                
    if not conteo:
        return {"ok": False, "mensaje": "No se han registrado ventas hoy."}

    max_producto = None
    max_cantidad = 0

    for producto, cantidad in conteo.items():
        if cantidad > max_cantidad:
            max_cantidad = cantidad
            max_producto = producto
    return {"ok": True, "producto": max_producto, "cantidad": max_cantidad}
