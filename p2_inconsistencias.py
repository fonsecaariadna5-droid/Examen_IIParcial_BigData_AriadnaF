import pandas as pd
import numpy as np


df = pd.read_csv("ventas.csv")

# Asegurar que los nombres de columnas no tengan espacios raros
df.columns = df.columns.str.strip()

# 1. Subtotal = Cantidad * PrecioUnitario
df["Subtotal"] = df["Cantidad"] * df["PrecioUnitario"]

# 2. Error relativo entre Subtotal y Total
df["Error_Relativo"] = abs(df["Subtotal"] - df["Total"]) / df["Total"]

# 3. Inconsistencias cuando el error es mayor al 5%
inconsistencias = df[df["Error_Relativo"] > 0.05]

# 4. Exportar a CSV
inconsistencias.to_csv("inconsistencias.csv", index=False)

# 5. Métricas pedidas
total_inconsistentes = len(inconsistencias)
promedio_error = inconsistencias["Error_Relativo"].mean()

# Producto con más inconsistencias (si existe alguno)
if total_inconsistentes > 0:
    producto_mas_inconsistente = inconsistencias["Producto"].value_counts().idxmax()
else:
    producto_mas_inconsistente = "Ninguno"

# 6. Mostrar resultados
print("----- RESULTADOS INCONSISTENCIAS -----")
print("Total de registros inconsistentes:", total_inconsistentes)
print("Promedio del error relativo:", round(promedio_error, 4))
print("Producto con más inconsistencias:", producto_mas_inconsistente)
print("--------------------------------------")

# Solo para ver un poco cómo quedaron
print("\nPrimeras filas de inconsistencias:")
print(inconsistencias.head())
