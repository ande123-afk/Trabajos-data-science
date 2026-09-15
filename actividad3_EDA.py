"""
Actividad 3: Taller EDA
Dataset: Netflix Movies and TV Shows (Kaggle)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('netflix_titles.csv')

# ============================================================
# 2. EXPLORACION INICIAL
# ============================================================
print("=== Forma del dataset (filas, columnas) ===")
print(df.shape)

print("\n=== Columnas ===")
print(df.columns.tolist())

print("\n=== Tipos de datos ===")
print(df.dtypes)

print("\n=== Primeras filas ===")
print(df.head())

print("\n=== Nulos por columna ===")
print(df.isnull().sum())

print("\n=== Cantidad de filas duplicadas ===")
print(df.duplicated().sum())

# ============================================================
# 3. LIMPIEZA DE DATOS
# ============================================================

# director, cast y country tienen muchos nulos.
# En vez de borrar esas filas, las rellenamos con "Desconocido"
# para no perder informacion de las demas columnas.
df['director'] = df['director'].fillna('Desconocido')
df['cast'] = df['cast'].fillna('Desconocido')
df['country'] = df['country'].fillna('Desconocido')

# date_added, rating y duration tienen muy pocos nulos,
# asi que esas filas si las eliminamos.
df = df.dropna(subset=['date_added', 'rating', 'duration'])

# quitamos filas duplicadas
df = df.drop_duplicates()

print("\n=== Forma despues de limpieza ===")
print(df.shape)

print("\n=== Nulos despues de limpieza ===")
print(df.isnull().sum())

# ============================================================
# 4. FILTRADO Y SELECCION DE DATOS RELEVANTES
# ============================================================

columnas_relevantes = ['type', 'title', 'country', 'date_added',
                        'release_year', 'rating', 'duration', 'listed_in']
df_analisis = df[columnas_relevantes].copy()

# Filtro de peliculas
peliculas = df_analisis[df_analisis['type'] == 'Movie']

# Filtro de series
series = df_analisis[df_analisis['type'] == 'TV Show']

print("\n=== Cantidad de peliculas vs series ===")
print(f"Peliculas: {len(peliculas)}")
print(f"Series: {len(series)}")

# ============================================================
# 5. TRANSFORMACION DE COLUMNAS Y VARIABLES NUEVAS
# ============================================================

# 5.1 duration viene mezclada: "90 min" para peliculas
#     y "2 Seasons" para series. La separamos en dos columnas
#     nuevas, recorriendo el DataFrame fila por fila con un for.

lista_minutos = []
lista_temporadas = []

for indice, fila in df_analisis.iterrows():
    if fila['type'] == 'Movie':
        # la duracion viene como "90 min", quitamos " min" y convertimos a numero
        texto_duracion = fila['duration'].replace(' min', '')
        minutos = int(texto_duracion)
        lista_minutos.append(minutos)
        lista_temporadas.append(np.nan)
    else:
        # la duracion viene como "2 Seasons" o "1 Season"
        texto_duracion = fila['duration'].split(' ')[0]
        temporadas = int(texto_duracion)
        lista_temporadas.append(temporadas)
        lista_minutos.append(np.nan)

df_analisis['duration_minutos'] = lista_minutos
df_analisis['duration_temporadas'] = lista_temporadas

# 5.2 convertimos date_added a fecha real y sacamos el anio
df_analisis['date_added'] = pd.to_datetime(df_analisis['date_added'].str.strip())
df_analisis['anio_agregado'] = df_analisis['date_added'].dt.year

# 5.3 country y listed_in a veces traen varios valores separados por coma
#     (ej: "United States, Ghana"). Nos quedamos solo con el primero.

lista_paises = []
for valor in df_analisis['country']:
    primer_pais = valor.split(',')[0].strip()
    lista_paises.append(primer_pais)
df_analisis['pais_principal'] = lista_paises

lista_generos = []
for valor in df_analisis['listed_in']:
    primer_genero = valor.split(',')[0].strip()
    lista_generos.append(primer_genero)
df_analisis['genero_principal'] = lista_generos

print("\n=== Vista de las columnas nuevas ===")
print(df_analisis[['type', 'duration', 'duration_minutos',
                    'duration_temporadas', 'anio_agregado',
                    'pais_principal', 'genero_principal']].head())

# ============================================================
# 6. AGRUPACIONES Y RESUMENES (groupby)
# ============================================================

print("\n=== Cantidad de titulos por tipo ===")
print(df_analisis.groupby('type').size())

print("\n=== Top 10 paises con mas titulos ===")
# quitamos "Desconocido" para que no distorsione el ranking real de paises
df_con_pais = df_analisis[df_analisis['pais_principal'] != 'Desconocido']
top_paises = df_con_pais.groupby('pais_principal').size().sort_values(ascending=False).head(10)
print(top_paises)

print("\n=== Duracion promedio de peliculas por genero (top 10) ===")
duracion_por_genero = df_analisis.groupby('genero_principal')['duration_minutos'].mean().sort_values(ascending=False).head(10)
print(duracion_por_genero)

print("\n=== Titulos agregados por anio ===")
titulos_por_anio = df_analisis.groupby('anio_agregado').size()
print(titulos_por_anio)

# ============================================================
# 7. PREGUNTAS DE ANALISIS
# ============================================================

# ------------------------------------------------------------
# Pregunta 1: Como ha evolucionado la cantidad de titulos
# agregados a Netflix por anio?
# ------------------------------------------------------------
plt.figure(figsize=(10, 5))
titulos_por_anio.plot(kind='line', marker='o', color='#E50914')
plt.title('Titulos agregados a Netflix por anio')
plt.xlabel('Anio')
plt.ylabel('Cantidad de titulos')
plt.grid(True)
plt.tight_layout()
plt.savefig('pregunta1_titulos_por_anio.png')
plt.show()

# Interpretacion:
# El catalogo crece fuerte desde 2016 y llega a su punto mas alto
# alrededor de 2019, para luego bajar. Coincide con la epoca de
# mayor inversion de Netflix en contenido antes de la pandemia.

# ------------------------------------------------------------
# Pregunta 2: Que paises producen mas contenido en el catalogo?
# ------------------------------------------------------------
plt.figure(figsize=(10, 6))
sns.barplot(x=top_paises.values, y=top_paises.index, hue=top_paises.index,
            palette='Reds_r', legend=False)
plt.title('Top 10 paises con mas titulos en Netflix')
plt.xlabel('Cantidad de titulos')
plt.ylabel('Pais')
plt.tight_layout()
plt.savefig('pregunta2_top_paises.png')
plt.show()

# Interpretacion:
# Estados Unidos domina claramente el catalogo, seguido de India.
# Refleja donde Netflix concentra su produccion original y sus
# acuerdos de licencia de contenido.

# ------------------------------------------------------------
# Pregunta 3: Predomina Movie o TV Show, y como varia eso
# entre los paises con mas contenido?
# ------------------------------------------------------------
top5_paises = top_paises.head(5).index.tolist()
subset_top5 = df_analisis[df_analisis['pais_principal'].isin(top5_paises)]

plt.figure(figsize=(10, 6))
sns.countplot(data=subset_top5, x='pais_principal', hue='type', order=top5_paises)
plt.title('Peliculas vs Series en los 5 paises con mas contenido')
plt.xlabel('Pais')
plt.ylabel('Cantidad de titulos')
plt.legend(title='Tipo')
plt.tight_layout()
plt.savefig('pregunta3_movie_vs_tv_por_pais.png')
plt.show()

# Interpretacion:
# Las peliculas predominan sobre las series en casi todos los
# paises principales, aunque la proporcion de series es mas alta
# en paises como Corea del Sur o Reino Unido que en Estados Unidos.

# ------------------------------------------------------------
# Pregunta 4: Cuales son los generos mas comunes en el catalogo?
# ------------------------------------------------------------
top_generos = df_analisis.groupby('genero_principal').size().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_generos.values, y=top_generos.index, hue=top_generos.index,
            palette='mako', legend=False)
plt.title('Top 10 generos principales en Netflix')
plt.xlabel('Cantidad de titulos')
plt.ylabel('Genero')
plt.tight_layout()
plt.savefig('pregunta4_top_generos.png')
plt.show()

# Interpretacion:
# Los dramas internacionales y las comedias dominan el catalogo,
# lo que muestra la apuesta de Netflix por contenido internacional
# mas alla de las producciones estadounidenses tradicionales.

# ------------------------------------------------------------
# Pregunta 5: Como se distribuyen las clasificaciones (rating)?
# Hay mas contenido para adultos o para audiencia familiar?
# ------------------------------------------------------------
plt.figure(figsize=(10, 5))
sns.countplot(data=df_analisis, x='rating',
              order=df_analisis['rating'].value_counts().index)
plt.title('Distribucion de clasificaciones (rating) en Netflix')
plt.xlabel('Clasificacion')
plt.ylabel('Cantidad de titulos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('pregunta5_distribucion_rating.png')
plt.show()

# Interpretacion:
# La clasificacion mas comun es TV-MA (contenido para adultos),
# seguida de TV-14. El catalogo esta orientado principalmente a
# audiencia adulta/adolescente, no infantil.

# ============================================================
# 8. CONCLUSIONES
# ============================================================
print("""
CONCLUSIONES:

1. El catalogo de Netflix crecio de forma acelerada entre 2016 y 2019,
   con una caida notoria despues de 2020, probablemente relacionada
   con cambios en la estrategia de contenido y la pandemia.

2. Estados Unidos e India concentran la mayor parte del catalogo,
   mostrando que Netflix combina produccion propia en EE.UU. con
   fuerte presencia de contenido de Bollywood/India.

3. El catalogo esta compuesto mayoritariamente por peliculas (Movies)
   sobre series (TV Shows), en una proporcion de aproximadamente 70/30.

4. La clasificacion TV-MA es la mas frecuente, lo que confirma que
   el catalogo esta pensado mas para publico adulto que infantil,
   a diferencia de lo que muchos asumirian de una plataforma familiar.
""")