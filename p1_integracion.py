import pandas as pd
import numpy as np


# 1. Leer archivos

ventas = pd.read_csv("ventas.csv")
clientes = pd.read_csv("clientes.csv")
productos = pd.read_csv("productos.csv")

# Asegurar columnas limpias
ventas.columns = ventas.columns.str.strip()
clientes.columns = clientes.columns.str.strip()
productos.columns = productos.columns.str.strip()


# 2. Eliminar ventas cuyo Producto no existe en productos.csv

productos_validos = set(productos["Producto"].unique())
clientes_validos = set(clientes["Cliente"].unique())

rechazadas_producto = ventas[~ventas["Producto"].isin(productos_validos)]
ventas = ventas[ventas["Producto"].isin(productos_validos)]


# 3. Eliminar ventas cuyo Cliente no existe en clientes.csv

rechazadas_cliente = ventas[~ventas["Cliente"].isin(clientes_validos)]
ventas = ventas[ventas["Cliente"].isin(clientes_validos)]


# 4. Corrección de tipos (Cantidad, PrecioUnitario, Total)

def corregir_columna(df, col):
    # Convertir a numérico, errores → NaN
    df[col] = pd.to_numeric(df[col], errors="coerce")
    # Calcular promedio sin NaN
    promedio = df[col].mean()
    # Reemplazar valores inválidos con promedio
    df[col].fillna(promedio, inplace=True)

corregir_columna(ventas, "Cantidad")
corregir_columna(ventas, "PrecioUnitario")
corregir_columna(ventas, "Total")


# 5. Integración (merge)

df_final = ventas.merge(clientes, on="Cliente", how="left")
df_final = df_final.merge(productos, on="Producto", how="left")


# 6. Reportes de filas

total_rechazadas = len(rechazadas_producto) + len(rechazadas_cliente)
total_finales = len(df_final)

print("---------------------------------------------------")
print("PROBLEMA 1 – INTEGRACIÓN DE DATOS")
print("---------------------------------------------------")
print(f"Filas rechazadas por producto inexistente: {len(rechazadas_producto)}")
print(f"Filas rechazadas por cliente inexistente : {len(rechazadas_cliente)}")
print(f"Total de filas rechazadas                : {total_rechazadas}")
print(f"Total de filas finales en el DataFrame  : {total_finales}")
print("---------------------------------------------------")


# 7. Mostrar primeras 10 filas

print("\nPrimeras 10 filas del DataFrame final:")
print(df_final.head(10))
