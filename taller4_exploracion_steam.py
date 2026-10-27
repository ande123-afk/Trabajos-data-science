"""
Taller - Aprendizaje No Supervisado (Steam Video Games)
Etapa 1: Exploracion de datos
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "steam-200k.csv")
IMG_DIR = os.path.join(BASE_DIR, "img_taller4")
os.makedirs(IMG_DIR, exist_ok=True)

# -----------------------------
# 1. Carga
# -----------------------------
# El CSV no trae encabezado, se asignan los nombres manualmente.
# La 5ta columna no tiene informacion util (siempre vale 0), se descarta.
df = pd.read_csv(
    DATA_PATH,
    header=None,
    names=["user_id", "game", "behavior", "value", "unused"],
)
df = df.drop(columns=["unused"])

print("=" * 60)
print("1. DIMENSIONES")
print("=" * 60)
print("Filas:", df.shape[0], "| Columnas:", df.shape[1])

print("\n" + "=" * 60)
print("2. TIPOS DE VARIABLES")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("3. VALORES NULOS")
print("=" * 60)
print(df.isnull().sum())

print("\n" + "=" * 60)
print("4. REGISTROS DUPLICADOS")
print("=" * 60)
n_dup = df.duplicated().sum()
print(f"Duplicados exactos: {n_dup}")
# Se eliminan aqui: son el mismo evento (usuario+juego+accion+valor) repetido,
# no aportan informacion nueva y pueden sesgar los conteos por usuario.
df = df.drop_duplicates().reset_index(drop=True)
print(f"Filas despues de quitar duplicados: {df.shape[0]}")

print("\n" + "=" * 60)
print("5. ESTADISTICOS DESCRIPTIVOS")
print("=" * 60)
print("\nValores unicos de 'behavior':", df["behavior"].unique())
print("\nUsuarios unicos:", df["user_id"].nunique())
print("Juegos unicos:", df["game"].nunique())

print("\nDescriptivos de 'value' segun tipo de accion:")
print(df.groupby("behavior")["value"].describe())

# purchase siempre deberia valer 1 (es una bandera de compra, no una cantidad)
print("\nValores unicos de 'value' cuando behavior=purchase:")
print(df.loc[df["behavior"] == "purchase", "value"].unique())

# -----------------------------
# 6. Visualizaciones
# -----------------------------
sns.set_style("whitegrid")

# 6.1 Cantidad de eventos por tipo de accion
plt.figure(figsize=(5, 4))
sns.countplot(data=df, x="behavior")
plt.title("Cantidad de registros por tipo de accion")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "eda_conteo_behavior.png"), dpi=120)
plt.close()

# 6.2 Distribucion de horas jugadas (muy sesgada, se usa escala log)
horas = df.loc[df["behavior"] == "play", "value"]
plt.figure(figsize=(6, 4))
sns.histplot(horas, bins=50, log_scale=True)
plt.title("Distribucion de horas jugadas por registro (escala log)")
plt.xlabel("Horas jugadas (log)")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "eda_distribucion_horas.png"), dpi=120)
plt.close()

# 6.3 Top 15 juegos con mas jugadores distintos
top_juegos = (
    df[df["behavior"] == "purchase"]
    .groupby("game")["user_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(15)
)
plt.figure(figsize=(7, 6))
sns.barplot(x=top_juegos.values, y=top_juegos.index, orient="h")
plt.title("Top 15 juegos con mas compradores")
plt.xlabel("Numero de usuarios")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "eda_top_juegos.png"), dpi=120)
plt.close()

# 6.4 Distribucion de juegos comprados por usuario
juegos_por_usuario = (
    df[df["behavior"] == "purchase"].groupby("user_id")["game"].nunique()
)
plt.figure(figsize=(6, 4))
sns.histplot(juegos_por_usuario, bins=50)
plt.title("Numero de juegos comprados por usuario")
plt.xlabel("Juegos comprados")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "eda_juegos_por_usuario.png"), dpi=120)
plt.close()

print(f"\nGraficas guardadas en: {IMG_DIR}")

# -----------------------------
# 7. Guardar version limpia (sin duplicados) para la siguiente etapa
# -----------------------------
OUT_PATH = os.path.join(BASE_DIR, "data", "steam4_sin_duplicados.csv")
df.to_csv(OUT_PATH, index=False)
print(f"\nDataset sin duplicados guardado en: {OUT_PATH}")
