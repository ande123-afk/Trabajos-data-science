
# Taller Práctico – Aprendizaje No Supervisado (Steam Video Games)

## Objetivo

Segmentar usuarios de Steam según su comportamiento de compra y juego, usando técnicas de clustering, para identificar perfiles de usuario y proponer recomendaciones de negocio.

## Dataset

[Steam Video Games](https://www.kaggle.com/datasets/tamber/steam-video-games) — 199.293 registros (tras quitar duplicados) de interacciones (compra/juego) de 12.393 usuarios sobre 5.155 juegos.

Columnas originales: `user_id`, `game`, `behavior` (purchase/play), `value` (1 para compra, horas para juego).

## Metodología

### 1. Exploración de datos (`taller4_exploracion_steam.py`)

- Dimensiones: 200.000 filas × 4 columnas útiles (se descartó una 5ª columna sin información).
- Sin valores nulos.
- 707 registros duplicados exactos, eliminados.
- `behavior = purchase` siempre vale 1.0 (es una bandera de compra, no una cantidad).
- `behavior = play` tiene distribución de horas muy sesgada: media 48,9h, mediana 4,5h, máximo 11.754h.
- Visualizaciones: conteo por tipo de acción, distribución de horas jugadas (escala log), top 15 juegos más comprados, distribución de juegos comprados por usuario.

### 2. Preparación de datos (`taller4_preparacion_steam.py`)

**Decisión clave**: el dataset es transaccional (una fila por evento), no por usuario. Se transformó a una tabla con una fila por `user_id`, agregando:

- `n_juegos_comprados`, `n_juegos_jugados`
- `horas_totales`, `horas_promedio_por_juego`, `horas_max_un_juego`
- `pct_juegos_nunca_jugados` (compró pero nunca jugó)

**Transformación logarítmica** (`log1p`) sobre las variables de volumen/horas, porque su distribución está muy sesgada y distorsionaría las distancias euclidianas que usan K-Means y DBSCAN.

**Escalado**: `StandardScaler`, necesario porque las variables tienen escalas muy distintas (ej. horas totales vs. porcentaje 0-1); sin esto, horas dominaría la distancia por sobre las demás variables.

**Variables finales usadas en el modelo**: `log_n_comprados`, `log_horas_totales`, `log_horas_promedio`, `pct_juegos_nunca_jugados`.

### 3. Modelado (`taller4_clustering_steam.py`)

| Algoritmo | Parámetros                        | Clusters encontrados     | Silhouette Score         |
| --------- | ---------------------------------- | ------------------------ | ------------------------ |
| K-Means   | K=4 (elegido por método del codo) | 4                        | **0,452**          |
| DBSCAN    | eps=0,35, min_samples=8            | 4 + 170 outliers (ruido) | 0,178 (sin contar ruido) |

**Justificación de la elección**: se usó K-Means como modelo principal porque obtuvo un Silhouette Score muy superior a DBSCAN. Esto es consistente con la naturaleza de los datos: las variables de comportamiento (horas, compras) varían de forma continua entre usuarios, sin zonas de densidad claramente separadas por "vacíos", que es lo que DBSCAN necesita para funcionar bien. DBSCAN sí aportó valor complementario al identificar 170 usuarios atípicos (outliers) con comportamiento extremo, que quedan fuera de los 4 segmentos principales.

### 4. Interpretación de clusters (`taller4_interpretacion_steam.py`)

| Cluster | Usuarios | Juegos comprados | Juegos jugados | Horas totales | Horas/juego | % nunca jugados | Nombre                                                 |
| ------- | -------- | ---------------- | -------------- | ------------- | ----------- | --------------- | ------------------------------------------------------ |
| 0       | 2.336    | 44,74            | 23,74          | 986,55        | 91,57       | 44%             | **Compradores Activos / Coleccionistas con Uso** |
| 1       | 2.930    | 2,71             | 2,19           | 376,89        | 232,21      | 14%             | **Jugadores Dedicados (Mono-juego)**             |
| 2       | 2.343    | 4,02             | 0,87           | 3,56          | 2,64        | 80%             | **Coleccionistas Pasivos**                       |
| 3       | 4.784    | 1,45             | 1,37           | 5,89          | 4,31        | 2%              | **Jugadores Casuales**                           |

**¿Qué caracteriza a cada grupo?**

- **Compradores Activos/Coleccionistas con Uso**: compran mucho catálogo y también juegan bastante, aunque casi la mitad de lo comprado nunca lo tocan. Es el grupo con más horas totales e inversión aparente.
- **Jugadores Dedicados (Mono-juego)**: compran pocos títulos, pero el promedio de horas por juego es el más alto de todos — se concentran intensamente en 1-2 juegos.
- **Coleccionistas Pasivos**: compran, pero el 80% de lo que compran nunca lo juegan. Horas de juego casi nulas.
- **Jugadores Casuales**: el grupo más grande (4.784 usuarios). Compran poco, pero casi todo lo que compran lo prueban (solo 2% sin jugar). Bajo compromiso general en volumen, pero alta "tasa de activación".

**¿Son jugadores ocasionales o frecuentes?** Hay un espectro claro: Cluster 1 es el más frecuente/intenso en relación a lo que compra; Cluster 0 es frecuente en términos absolutos (muchas horas) pero sobre un catálogo más disperso; Clusters 2 y 3 son de bajo compromiso, pero opuestos entre sí: 2 acumula sin jugar, 3 prueba todo lo que compra.

**¿Presentan comportamientos similares de compra?** No — el volumen de compra varía casi 30x entre el cluster más bajo (1,45 juegos) y el más alto (44,74 juegos), y el patrón de "jugar lo comprado" también difiere fuertemente (2% vs 80% sin jugar).

**¿Qué diferencias existen entre los clusters?** La diferencia principal no es solo cuánto compran, sino qué tan bien correlaciona su compra con su consumo real (horas jugadas). Eso separa "compradores" de "jugadores" como dos dimensiones distintas del comportamiento.

## Recomendaciones de negocio

| Cluster                                    | Estrategia de marketing                                               | Tipo de promoción                                                                                         | Prioridad de fidelización                                                              |
| ------------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Compradores Activos/Coleccionistas con Uso | Recomendaciones personalizadas sobre su propio catálogo sin estrenar | Descuentos en DLC/secuelas de lo que ya juegan mucho                                                       | Alta — el segmento más valioso, ya gasta y juega                                      |
| Jugadores Dedicados (Mono-juego)           | Contenido adicional (DLC, expansiones, eventos) del juego que dominan | Ofertas cruzadas hacia títulos similares a su favorito                                                    | Alta — muy comprometidos, riesgo de fuga si se "aburren"                               |
| Coleccionistas Pasivos                     | Campañas de reactivación ("tienes X juegos sin estrenar")           | Evitar más descuentos de compra; priorizar notificaciones/recordatorios para que jueguen lo que ya tienen | Baja — ya gastan sin incentivo extra; el reto es activarlos a jugar, no a comprar más |
| Jugadores Casuales                         | Onboarding y descubrimiento de catálogo                              | Bundles económicos de entrada, ofertas de "primera compra"                                                | Media — el segmento más grande, con potencial de crecimiento si se les engancha       |

**¿Qué información adicional sería útil para mejorar la segmentación?** Género/categoría de los juegos (para saber no solo cuánto sino qué tipo de contenido prefiere cada cluster), precio pagado, fecha de compra (para detectar estacionalidad o antigüedad como usuario), y plataforma de acceso (PC, Steam Deck, etc.).

## Conclusiones

- El dataset transaccional se transformó exitosamente en una tabla por usuario con variables agregadas, necesarias para aplicar clustering.
- K-Means con K=4 fue el modelo con mejor desempeño (Silhouette 0,452) frente a DBSCAN (0,178), por la naturaleza continua (no densamente separada) de los datos de comportamiento.
- Se identificaron 4 segmentos claramente diferenciables por volumen de compra y tasa de activación (juego real vs. compra), más 170 usuarios atípicos detectados por DBSCAN que podrían estudiarse aparte.
- El valor para una organización como Steam está en tratar "comprar" y "jugar" como dos señales separadas: permite dirigir campañas de reactivación de catálogo (Coleccionistas Pasivos) de forma distinta a campañas de expansión de contenido (Jugadores Dedicados), en vez de tratar a todos los usuarios igual.

## Cómo correr el proyecto

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python taller4_exploracion_steam.py
python taller4_preparacion_steam.py
python taller4_clustering_steam.py
python taller4_interpretacion_steam.py
```

## Autor

Andrés Beltrán
