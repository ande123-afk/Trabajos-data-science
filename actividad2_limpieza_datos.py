import pandas as pd

# Cargo el dataset (separado por punto y coma)
df = pd.read_csv("C:/Users/chato/Downloads/archive/animal_data_dirty1.csv", sep=";")

# ============================
# PARTE 1: DIAGNOSTICO INICIAL
# ============================

print("=== Cantidad de filas y columnas ===")
print(df.shape)

print("\n=== Columnas y tipos de dato ===")
print(df.dtypes)

print("\n=== Valores faltantes por columna ===")
print(df.isnull().sum())

print("\n=== Registros duplicados ===")
print("Duplicados encontrados:", df.duplicated().sum())

print("\n=== Valores unicos en Animal type ===")
print(df["Animal type"].value_counts(dropna=False))

print("\n=== Valores unicos en Country ===")
print(df["Country"].value_counts(dropna=False))

print("\n=== Valores unicos en Gender ===")
print(df["Gender"].value_counts(dropna=False))

# Problemas de calidad encontrados:
# 1. La columna "Animal type" tiene errores de escritura como "red squirrell",
#    "red squirel", "lynx?", "European bisson", "European buster", "ledgehod",
#    "wedgehod", que en realidad son el mismo animal mal escrito.
# 2. La columna "Country" mezcla nombres completos con abreviaturas (PL, HU, CZ, DE)
#    y tiene errores de escritura como "Hungry" y "Czech", ademas de valores
#    que no corresponden a la region de estudio ("Australia", "CC").
# 3. Hay 167 registros completamente duplicados que hay que eliminar.
# 4. La columna "Animal code" esta vacia en el 100% de las filas, no aporta nada.

# ============================
# PARTE 2: LIMPIEZA DE DATOS
# ============================

# 1. Elimino la columna que esta completamente vacia
df = df.drop(columns=["Animal code"])

# 2. Elimino los registros duplicados
print("\nFilas antes de quitar duplicados:", df.shape[0])
df = df.drop_duplicates()
print("Filas despues de quitar duplicados:", df.shape[0])

# 3. Estandarizo la columna Animal type (corrijo errores de escritura)
df["Animal type"] = df["Animal type"].replace({
    "red squirrell": "red squirrel",
    "red squirel": "red squirrel",
    "lynx?": "lynx",
    "European bison™": "European bison",
    "European bisson": "European bison",
    "European buster": "European bison",
    "ledgehod": "hedgehog",
    "wedgehod": "hedgehog"
})

# 4. Estandarizo la columna Country (uno abreviaturas y corrijo errores)
df["Country"] = df["Country"].replace({
    "PL": "Poland",
    "HU": "Hungary",
    "Hungry": "Hungary",
    "CZ": "Czech Republic",
    "Czech": "Czech Republic",
    "DE": "Germany"
})

# Elimino filas con paises que no corresponden a la region de estudio (probable error de captura)
df = df[~df["Country"].isin(["Australia", "CC"])]

# 5. Trato los valores faltantes
# Weight kg y Body Length cm: relleno con la mediana para no afectar el promedio con outliers
df["Weight kg"] = df["Weight kg"].fillna(df["Weight kg"].median())
df["Body Length cm"] = df["Body Length cm"].fillna(df["Body Length cm"].median())

# Gender: relleno los nulos con "unknown" en vez de dejarlos vacios
df["Gender"] = df["Gender"].fillna("unknown")

# Animal type y Country: elimino las filas donde falta esta info, porque son pocas
df = df.dropna(subset=["Animal type", "Country"])

# Latitude y Longitude: los dejo como estan, no se puede inventar una ubicacion
# Animal name: los dejo como estan, es normal que no todos los animales tengan nombre

# ============================
# VERIFICACION FINAL
# ============================

print("\n=== Shape final del DataFrame limpio ===")
print(df.shape)

print("\n=== Nulos restantes por columna ===")
print(df.isnull().sum())

print("\n=== Valores unicos finales en Animal type ===")
print(df["Animal type"].unique())

print("\n=== Valores unicos finales en Country ===")
print(df["Country"].unique())