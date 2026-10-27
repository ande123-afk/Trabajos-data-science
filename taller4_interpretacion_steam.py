"""
Taller - Aprendizaje No Supervisado (Steam Video Games)
Etapa 4: Interpretacion de clusters
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img_taller4")

usuarios = pd.read_csv(os.path.join(BASE_DIR, "data", "usuarios4_con_clusters.csv"))

sns.set_style("whitegrid")

# -----------------------------
# Se interpreta el resultado de K-Means (mejor Silhouette Score que DBSCAN,
# ver etapa 3). DBSCAN dejo 170 usuarios como ruido/outliers, utiles para
# revisar aparte como "usuarios atipicos" pero no para la segmentacion
# principal.
# -----------------------------

print("=" * 60)
print("PERFIL PROMEDIO POR CLUSTER (K-Means)")
print("=" * 60)
perfil = usuarios.groupby("cluster_kmeans")[
    ["n_juegos_comprados", "n_juegos_jugados", "horas_totales",
     "horas_promedio_por_juego", "pct_juegos_nunca_jugados"]
].mean().round(2)
perfil["n_usuarios"] = usuarios["cluster_kmeans"].value_counts().sort_index()
print(perfil)

# -----------------------------
# Visualizacion de cada variable por cluster
# -----------------------------
variables = ["n_juegos_comprados", "horas_totales", "pct_juegos_nunca_jugados"]
fig, axes = plt.subplots(1, len(variables), figsize=(15, 4))
for ax, var in zip(axes, variables):
    sns.boxplot(data=usuarios, x="cluster_kmeans", y=var, ax=ax, showfliers=False)
    ax.set_title(var)
plt.tight_layout()
plt.savefig(os.path.join(IMG_DIR, "clusters_perfil_boxplots.png"), dpi=120)
plt.close()

# -----------------------------
# Usuarios atipicos detectados por DBSCAN (ruido)
# -----------------------------
outliers = usuarios[usuarios["cluster_dbscan"] == -1]
print(f"\nUsuarios marcados como outliers por DBSCAN: {len(outliers)}")
print(outliers[["n_juegos_comprados", "horas_totales", "pct_juegos_nunca_jugados"]].describe())


NOMBRES_CLUSTERS = {
    0: "Compradores Activos / Coleccionistas con Uso",
    1: "Jugadores Dedicados (Mono-juego)",
    2: "Coleccionistas Pasivos",
    3: "Jugadores Casuales",
}

print("\nNombres asignados (pendientes de completar):")
for k, v in NOMBRES_CLUSTERS.items():
    print(f"  Cluster {k}: {v}")

print("""
-----------------------------------------------------------
PREGUNTAS A RESPONDER EN EL README / INFORME (con tus datos):
-----------------------------------------------------------
1. Que caracteriza a los usuarios de cada grupo?
2. Son jugadores ocasionales o frecuentes?
3. Presentan comportamientos similares de compra?
4. Que diferencias existen entre los clusters?

-----------------------------------------------------------
RECOMENDACIONES DE NEGOCIO (completar con base en los perfiles):
-----------------------------------------------------------
- Que estrategia de marketing implementarias para cada grupo?
- Que tipo de promociones recibiria cada segmento?
- Que usuarios priorizarias para campanas de fidelizacion?
- Que informacion adicional seria util para mejorar la segmentacion?
  (ej: genero de los juegos, precio, fecha de compra, plataforma)
""")
