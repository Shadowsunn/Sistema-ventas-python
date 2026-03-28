import json
from datetime import datetime, timedelta

def cargar_datos():
    try:
        with open("memoria.json", "r") as file:
            ventas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
    for i, venta in enumerate(ventas):
        if "id" not in venta:
            venta["id"] = i+1
    guardar_datos(ventas)
    return ventas

def guardar_datos(ventas):
    with open("memoria.json", "w") as file:
        json.dump(ventas, file)

ventas = cargar_datos()

def registrar_venta(ventas, producto, cantidad, precio):
    producto = producto.strip().lower()
    cantidad = int(str(cantidad).split()[0])
    precio = int(str(precio).replace(".", "").replace(",", ""))

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
    guardar_datos(ventas)
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
    
def formatear_programa():
    # notas del diseñador backend para fabian (ya se que dijiste no notas, pero es necesario)
    # Que el diseñador del frontend se encargue de pedir la confirmacion al usuario antes de llamar a esta funcion
    # Fabian, ademas acuerdate de poner el ventas.clear() en el frontend para que se borren las ventas de la memoria del programa tambien, no solo del archivo json
    # sino eso quedara guardado en memoria y se volvera a escribir en el json la proxima vez que se registre una venta
    with open("memoria.json", "w") as file:
        json.dump([], file)
    return {"ok": True, "mensaje": "Todas las ventas han sido borradas."}

def eliminar_venta(ventas, id_eliminar):    
    venta_encontrada = None

    for venta in ventas:
        if venta["id"] == id_eliminar:
            venta_encontrada = venta
            break

    if venta_encontrada:
        ventas.remove(venta_encontrada)
        guardar_datos(ventas)
        return {"ok": True, "mensaje": "Venta eliminada exitosamente."}
    else:
        return {"ok": False, "mensaje": "No se encontró una venta con ese ID. Intente de nuevo."}

def editar_venta(ventas, id_editar, campo, nuevo_valor):
    venta_encontrada = None
    for venta in ventas:
        if venta["id"] == id_editar:
            venta_encontrada = venta
            break
        
    if not venta_encontrada:
        return{"ok": False, "mensaje": "No se encontró una venta con ese ID. Intente de nuevo."}
    
    if campo == "producto":
        venta_encontrada["producto"] = str(nuevo_valor).strip().lower()
    elif campo == "cantidad":
        venta_encontrada["cantidad"] = int(str(nuevo_valor).split()[0])
    elif campo == "precio":
        venta_encontrada["precio"] = int(str(nuevo_valor).replace(".", "").replace(",", ""))
    else:
        return {"ok": False, "mensaje": "Campo no válido. Los campos editables son: producto, cantidad, precio."}
    guardar_datos(ventas)
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