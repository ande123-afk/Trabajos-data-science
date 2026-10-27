"""
Taller - Aprendizaje No Supervisado (Steam Video Games)
Etapa 2: Preparacion de datos para clustering
"""

import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "steam4_sin_duplicados.csv")

df = pd.read_csv(DATA_PATH)

# -----------------------------
# 1. Pasar de formato transaccional (1 fila = 1 evento) a formato por usuario
# -----------------------------
# Decision: el clustering debe agrupar USUARIOS, no eventos. Por eso se
# construye una tabla con una fila por user_id y variables agregadas.

compras = df[df["behavior"] == "purchase"]
juegos_jugados = df[df["behavior"] == "play"]

# Variable: numero de juegos comprados por usuario
n_comprados = compras.groupby("user_id")["game"].nunique().rename("n_juegos_comprados")

# Variable: numero de juegos distintos jugados, y horas totales/promedio
n_jugados = juegos_jugados.groupby("user_id")["game"].nunique().rename("n_juegos_jugados")
horas_totales = juegos_jugados.groupby("user_id")["value"].sum().rename("horas_totales")
horas_promedio = juegos_jugados.groupby("user_id")["value"].mean().rename("horas_promedio_por_juego")
horas_max = juegos_jugados.groupby("user_id")["value"].max().rename("horas_max_un_juego")

# -----------------------------
# 2. Unir todo por usuario
# -----------------------------
usuarios = pd.concat(
    [n_comprados, n_jugados, horas_totales, horas_promedio, horas_max], axis=1
)

# Decision: un usuario puede aparecer en 'compras' pero no en 'juegos_jugados'
# (compro y nunca jugo). Para esos casos, las variables de juego quedan NaN
# y se rellenan con 0 porque representan "cero actividad de juego", no un
# dato faltante.
usuarios[["n_juegos_jugados", "horas_totales", "horas_promedio_por_juego", "horas_max_un_juego"]] = (
    usuarios[["n_juegos_jugados", "horas_totales", "horas_promedio_por_juego", "horas_max_un_juego"]].fillna(0)
)

# n_juegos_comprados no deberia tener NaN 
usuarios["n_juegos_comprados"] = usuarios["n_juegos_comprados"].fillna(0)

# -----------------------------
# 3. Variables derivadas
# -----------------------------
# Decision: el % de juegos comprados que nunca se jugaron es un indicador
# util para distinguir "coleccionistas" de "jugadores activos".
usuarios["pct_juegos_nunca_jugados"] = (
    (usuarios["n_juegos_comprados"] - usuarios["n_juegos_jugados"]) / usuarios["n_juegos_comprados"]
).clip(lower=0)

usuarios = usuarios.reset_index()

print("Dimensiones de la tabla por usuario:", usuarios.shape)
print(usuarios.describe())

# -----------------------------
# 4. Transformacion logaritmica
# -----------------------------
# Decision: horas_totales y horas_promedio tienen distribucion muy sesgada
# (confirmado en la etapa de exploracion, escala log fue necesaria para
# visualizarla). K-Means y DBSCAN usan distancias euclidianas, que se
# distorsionan con outliers extremos; log1p (log(1+x)) comprime la cola
# larga sin romper con valores en 0.
usuarios["log_horas_totales"] = np.log1p(usuarios["horas_totales"])
usuarios["log_horas_promedio"] = np.log1p(usuarios["horas_promedio_por_juego"])
usuarios["log_n_comprados"] = np.log1p(usuarios["n_juegos_comprados"])

# -----------------------------
# 5. Seleccion de variables para el modelo
# -----------------------------
# Decision: se usan las versiones log de las variables de volumen/horas
# (reducen el efecto de outliers) junto con el porcentaje de juegos no
# jugados (ya esta en escala 0-1, no necesita transformacion).
features = ["log_n_comprados", "log_horas_totales", "log_horas_promedio", "pct_juegos_nunca_jugados"]

X = usuarios[features].copy()

# -----------------------------
# 6. Escalado
# -----------------------------
# Decision: StandardScaler (media 0, desviacion 1) porque K-Means y DBSCAN
# son sensibles a la escala de las variables; sin esto, horas_totales
# dominaria la distancia euclidiana sobre pct_juegos_nunca_jugados.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=features)

# -----------------------------
# 7. Guardar resultados
# -----------------------------
usuarios_path = os.path.join(BASE_DIR, "data", "usuarios4_features.csv")
scaled_path = os.path.join(BASE_DIR, "data", "usuarios4_features_escalado.csv")

usuarios.to_csv(usuarios_path, index=False)
X_scaled_df.to_csv(scaled_path, index=False)

print(f"\nTabla de usuarios (sin escalar) guardada en: {usuarios_path}")
print(f"Tabla escalada (lista para clustering) guardada en: {scaled_path}")
print(f"\nVariables usadas para el modelo: {features}")
