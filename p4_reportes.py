import pandas as pd

# Cargar archivos
ventas = pd.read_csv("ventas.csv")
clientes = pd.read_csv("clientes.csv")
productos = pd.read_csv("productos.csv")

# Limpiar nombres de columnas
ventas.columns = ventas.columns.str.strip()
clientes.columns = clientes.columns.str.strip()
productos.columns = productos.columns.str.strip()

# ---- Corrección necesaria: asegurar que las llaves tengan el mismo tipo ----
ventas["Cliente"] = ventas["Cliente"].astype(str)
clientes["Cliente"] = clientes["Cliente"].astype(str)

ventas["Producto"] = ventas["Producto"].astype(str)
productos["Producto"] = productos["Producto"].astype(str)
# ---------------------------------------------------------------------------

# Merge para unir toda la información
df = ventas.merge(clientes, on="Cliente", how="left")
df = df.merge(productos, on="Producto", how="left")

# MÉTRICAS SOLICITADAS
reporte = df.groupby(
    ["Cliente", "Producto", "Ciudad", "Categoria_Cliente"]
).agg(
    Total_Sum=("Total", "sum"),
    Precio_Promedio=("PrecioUnitario", "mean"),
    Compras_Count=("Producto", "count")
).reset_index()

# Ordenar según lo solicitado
reporte = reporte.sort_values(by=["Ciudad", "Total_Sum"], ascending=[True, False])

# Exportar reporte final
reporte.to_csv("reporte_multinivel.csv", index=False)

# Indicadores adicionales
volumen_ciudad = df.groupby("Ciudad")["Total"].sum()
ciudad_top = volumen_ciudad.idxmax()

variedad = df.groupby("Cliente")["Producto"].nunique()
cliente_top_variedad = variedad.idxmax()

# Mostrar resultados
print("------- REPORTE MULTINIVEL GENERADO -------")
print("Archivo: reporte_multinivel.csv\n")
print("Ciudad con mayor volumen total:", ciudad_top)
print("Cliente con mayor variedad de productos:", cliente_top_variedad)
print("-------------------------------------------")
