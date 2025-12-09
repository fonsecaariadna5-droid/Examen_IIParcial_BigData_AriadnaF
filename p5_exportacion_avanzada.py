import pandas as pd
import os
import re


# Cargar archivo principal
ventas = pd.read_csv("ventas.csv")

# Normalizar columnas por si vienen con espacios
ventas.columns = ventas.columns.str.strip()

# Función para limpiar nombres de carpetas y archivos
def limpiar_nombre(nombre):
    nombre = str(nombre)
    nombre = nombre.strip()
    # Remover caracteres no válidos para rutas
    nombre = re.sub(r'[\\/*?:"<>|]', "", nombre)
    # Reemplazar espacios dobles por 1
    nombre = re.sub(r"\s+", "_", nombre)
    return nombre

# Crear carpeta general de salida
base_dir = "salidas"
os.makedirs(base_dir, exist_ok=True)

# Diccionario para el resumen global
resumen_global = []

# Procesar por cada producto
for producto, df_prod in ventas.groupby("Producto"):

    # Limpiar nombre
    nombre_limpio = limpiar_nombre(producto)

    # Ruta de la carpeta del producto
    carpeta = os.path.join(base_dir, f"Producto={nombre_limpio}")
    os.makedirs(carpeta, exist_ok=True)

    # Archivo CSV del producto
    archivo_csv = os.path.join(carpeta, f"{nombre_limpio}.csv")
    df_prod.to_csv(archivo_csv, index=False)

    # Cálculo de métricas
    total_ventas = df_prod["Total"].sum()
    cantidad = len(df_prod)
    precio_promedio = df_prod["PrecioUnitario"].mean()

    # Crear archivo resumen.txt
    resumen_txt = os.path.join(carpeta, "resumen.txt")
    with open(resumen_txt, "w", encoding="utf-8") as f:
        f.write(f"Producto: {producto}\n")
        f.write(f"Total de Ventas: {total_ventas}\n")
        f.write(f"Cantidad de Registros: {cantidad}\n")
        f.write(f"Precio Unitario Promedio: {precio_promedio}\n")

    # Agregar al resumen global
    resumen_global.append({
        "Producto": producto,
        "Total_Ventas": total_ventas,
        "Cantidad_Registros": cantidad,
        "PrecioUnitario_Promedio": precio_promedio
    })

# Crear resumen global CSV
df_global = pd.DataFrame(resumen_global)
df_global.to_csv("resumen_global_productos.csv", index=False)

print("Exportación segmentada completada.")
print("Se generaron carpetas, CSVs y resúmenes por producto.")
print("Resumen global guardado en resumen_global_productos.csv.")
