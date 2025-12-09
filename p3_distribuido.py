import pandas as pd


# Diccionario para sumar ventas por producto
ventas_por_producto = {}

# Acumulador del total final global
total_global = 0

# Para identificar el chunk que más vendió
mejor_chunk_venta = 0
mayor_venta_chunk = 0

# Leer por chunks de 1000 filas
chunk_num = 0
for chunk in pd.read_csv("ventas.csv", chunksize=1000):

    chunk_num += 1  # contar chunks

    # Asegurar columnas limpias
    chunk.columns = chunk.columns.str.strip()

    # Subtotal = Cantidad * PrecioUnitario
    chunk["Subtotal"] = chunk["Cantidad"] * chunk["PrecioUnitario"]

    # Impuesto según Total
    def calcular_impuesto(total):
        if total < 5000:
            return total * 0.10
        elif 5000 <= total <= 20000:
            return total * 0.15
        else:
            return total * 0.18

    chunk["Impuesto"] = chunk["Total"].apply(calcular_impuesto)

    # Total Final del chunk
    chunk["Total_Final"] = chunk["Total"] + chunk["Impuesto"]

    # Acumular al total global
    suma_chunk = chunk["Total_Final"].sum()
    total_global += suma_chunk

    # Ver si este chunk es el de mayor contribución
    if suma_chunk > mayor_venta_chunk:
        mayor_venta_chunk = suma_chunk
        mejor_chunk_venta = chunk_num

    # Acumular ventas por producto
    for prod, monto in zip(chunk["Producto"], chunk["Total_Final"]):
        if prod not in ventas_por_producto:
            ventas_por_producto[prod] = 0
        ventas_por_producto[prod] += monto


# Obtener el top 5 productos más vendidos
top5 = sorted(ventas_por_producto.items(), key=lambda x: x[1], reverse=True)[:5]

# Mostrar resultados
print("---------- RESULTADOS PROCESAMIENTO DISTRIBUIDO -----------")
print("Total Final Global:", round(total_global, 2))
print("\nTop 5 productos más vendidos:")
for prod, monto in top5:
    print(f"{prod}: {round(monto, 2)}")

print("\nChunk con mayor contribución en ventas:", mejor_chunk_venta)
print("------------------------------------------------------------")
