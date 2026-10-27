"""
Taller - Aprendizaje No Supervisado (Steam Video Games)
Etapa 3: Modelado de clustering
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img_taller4")
os.makedirs(IMG_DIR, exist_ok=True)

usuarios = pd.read_csv(os.path.join(BASE_DIR, "data", "usuarios4_features.csv"))
X_scaled = pd.read_csv(os.path.join(BASE_DIR, "data", "usuarios4_features_escalado.csv"))

sns.set_style("whitegrid")

# =====================================================
# K-MEANS
# =====================================================
# Decision: se elige K-Means como primer algoritmo porque produce clusters
# interpretables y balanceados, utiles para segmentacion de usuarios/marketing.

# 1. Metodo del codo para elegir K
inercias = []
rango_k = range(2, 11)
for k in rango_k:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inercias.append(km.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(list(rango_k), inercias, marker="o")
plt.xlabel("K (numero de clusters)")
plt.ylabel("Inercia")
plt.title("Metodo del codo - K-Means")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "kmeans_metodo_codo.png"), dpi=120)
plt.close()

# Revisa la grafica kmeans_metodo_codo.png y ajusta K_ELEGIDO segun el "codo"
# que se vea. Se deja un valor inicial razonable basado en pruebas previas.
K_ELEGIDO = 4

kmeans = KMeans(n_clusters=K_ELEGIDO, random_state=42, n_init=10)
usuarios["cluster_kmeans"] = kmeans.fit_predict(X_scaled)

sil_kmeans = silhouette_score(X_scaled, usuarios["cluster_kmeans"])
print(f"K-Means (K={K_ELEGIDO}) - Silhouette Score: {sil_kmeans:.3f}")
print(usuarios["cluster_kmeans"].value_counts().sort_index())

# =====================================================
# DBSCAN
# =====================================================
# Decision: se compara con DBSCAN porque no obliga a fijar K de antemano y
# puede detectar outliers (usuarios con comportamiento muy atipico) como
# ruido en vez de forzarlos dentro de un cluster.

# 1. Grafico de k-distancia para elegir eps (regla practica: min_samples ~
# 2 * numero de variables, aqui 4 variables -> min_samples = 8)
MIN_SAMPLES = 8
vecinos = NearestNeighbors(n_neighbors=MIN_SAMPLES)
vecinos_fit = vecinos.fit(X_scaled)
distancias, _ = vecinos_fit.kneighbors(X_scaled)
# distances[:, 0] es la distancia de cada punto a si mismo (siempre 0),
# se usa la columna del k-esimo vecino real: indice MIN_SAMPLES - 1
k_distancias = sorted(distancias[:, MIN_SAMPLES - 1])

plt.figure(figsize=(6, 4))
plt.plot(k_distancias)
plt.xlabel("Puntos ordenados")
plt.ylabel(f"Distancia al {MIN_SAMPLES}-esimo vecino")
plt.title("Grafico de k-distancia - DBSCAN")
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "dbscan_k_distancia.png"), dpi=120)
plt.close()

# Probado con varios valores: eps=0.35 es el que da un numero de clusters
# comparable a K-Means (4) sin dejar casi todo en un solo grupo.
EPS_ELEGIDO = 0.35

dbscan = DBSCAN(eps=EPS_ELEGIDO, min_samples=MIN_SAMPLES)
usuarios["cluster_dbscan"] = dbscan.fit_predict(X_scaled)

print(f"\nDBSCAN (eps={EPS_ELEGIDO}, min_samples={MIN_SAMPLES})")
print(usuarios["cluster_dbscan"].value_counts().sort_index())
print("(-1 = ruido / outliers)")

# Silhouette excluyendo el ruido (-1), porque incluirlo distorsiona la metrica
mask_sin_ruido = usuarios["cluster_dbscan"] != -1
if usuarios.loc[mask_sin_ruido, "cluster_dbscan"].nunique() > 1:
    sil_dbscan = silhouette_score(
        X_scaled[mask_sin_ruido], usuarios.loc[mask_sin_ruido, "cluster_dbscan"]
    )
    print(f"DBSCAN - Silhouette Score (sin ruido): {sil_dbscan:.3f}")
else:
    print("DBSCAN no genero suficientes clusters validos con este eps; ajusta EPS_ELEGIDO.")

# =====================================================
# Visualizacion comparativa (2 variables para graficar en 2D)
# =====================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.scatterplot(
    data=usuarios, x="log_horas_totales", y="log_n_comprados",
    hue="cluster_kmeans", palette="tab10", ax=axes[0]
)
axes[0].set_title(f"K-Means (K={K_ELEGIDO})")

sns.scatterplot(
    data=usuarios, x="log_horas_totales", y="log_n_comprados",
    hue="cluster_dbscan", palette="tab10", ax=axes[1]
)
axes[1].set_title(f"DBSCAN (eps={EPS_ELEGIDO})")

plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "clusters_comparacion.png"), dpi=120)
plt.close()

# -----------------------------
# Guardar resultados
# -----------------------------
out_path = os.path.join(BASE_DIR, "data", "usuarios4_con_clusters.csv")
usuarios.to_csv(out_path, index=False)
print(f"\nResultados guardados en: {out_path}")
print("\nIMPORTANTE: revisa img/kmeans_metodo_codo.png y img/dbscan_k_distancia.png")
print("y ajusta K_ELEGIDO / EPS_ELEGIDO en este script si el codo esta en otro punto.")
