# INF-8239 · Unidad 03 · Algoritmos y características generativas

**Autor académico:** Edwin Ramón José Nolasco

Proyecto base para LAB08–LAB09. No sustituya la comprensión por ejecución mecánica.

## Estudiante

**Laudys Jerusi Zapata**

**Programa:** Maestría en Ciencia de Datos e Inteligencia Artificial

**Universidad:** Universidad Autónoma de Santo Domingo (UASD)

**Asignatura:** Ciencia de Datos II

## 1. Objetivo

Este proyecto implementa un flujo reproducible de recomendación sobre **MovieLens Latest Small**.

El laboratorio desarrolla y compara cuatro estrategias:

1. Popularidad suavizada.
2. Recomendación por contenido.
3. Factorización colaborativa.
4. Recomendación híbrida.

LAB09 incorpora además una división temporal, evaluación de ratings y ranking, análisis de cobertura, cold start, comparación de configuraciones y costo computacional.

El sistema tiene finalidad académica y experimental. Una recomendación no representa una predicción universal de satisfacción individual.

## 2. Estructura del proyecto

```text
data/raw/              Dataset MovieLens descargado
docs/                   Dataset Card y System Card
reports/                Resultados reproducibles
scripts/                Descarga, auditoría y experimentos
src/inf8239_u03/        Código reutilizable
tests/                  Pruebas automatizadas
app/                    Aplicación Streamlit
```

## 3. Requisitos

* Python 3.12
* `uv`
* Dependencias definidas en `pyproject.toml`

Instalación:

```bash
uv python install 3.12
uv sync
```

No se crea un segundo entorno para LAB09 y no se descarga una segunda copia de MovieLens.

## 4. Pruebas

La suite completa se ejecuta con:

```bash
uv run pytest -q
```

Resultado verificado antes de LAB09:

```text
7 passed
```

Para LAB09 también se verificaron específicamente los componentes de factorización y métricas:

```bash
uv run pytest tests/test_matrix_factorization.py tests/test_metrics.py -q
```

Resultado verificado:

```text
3 passed
```

## 5. Dataset MovieLens

Se utiliza **MovieLens Latest Small (`ml-latest-small`)** de GroupLens.

Descarga:

```bash
uv run python scripts/download_data.py
```

Auditoría:

```bash
uv run python scripts/audit_data.py
```

SHA-256 de la descarga utilizada:

```text
696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436
```

La versión auditada contiene:

* 610 usuarios.
* 9,742 películas en el catálogo.
* 9,724 películas con al menos una valoración.
* 100,836 valoraciones.
* Rango de valoración: 0.5–5.0.
* Media: 3.501557.
* Mediana: 3.5.
* Desviación estándar: 1.042529.
* Densidad usuario-película: 0.016968, aproximadamente 1.70%.

Los datos originales se descargan mediante el script y no se editan manualmente.

La información detallada del dataset se encuentra en:

```text
docs/DATASET_CARD.md
```

## 6. Baseline de popularidad

La popularidad se calcula mediante una media suavizada que combina la media de cada película con la media global y considera la cantidad de valoraciones.

El umbral mínimo se obtiene mediante el percentil 80 del número de valoraciones.

Ejecutar:

```bash
uv run python scripts/lab08_content.py
```

El resultado se guarda en:

```text
reports/popular_top10.csv
```

El Top-10 obtenido fue encabezado por:

1. *Shawshank Redemption, The (1994)* — weighted_score 4.395194.
2. *Godfather, The (1972)* — weighted_score 4.242739.
3. *Fight Club (1999)* — weighted_score 4.232690.

La suavización evita que una película con pocas valoraciones domine únicamente por presentar una media alta.

## 7. Recomendador por contenido

El recomendador utiliza los géneros de las películas como señal de contenido.

Proceso:

1. Los géneros separados por `|` se transforman en texto.
2. Se construye una representación TF-IDF.
3. Se calcula similitud coseno.
4. Se excluye la película consultada.
5. Se devuelve el Top-10.

El resultado reproducible se guarda en:

```text
reports/content_recommendations.csv
```

### Consultas verificadas

**Toy Story (1995)**

Las 10 recomendaciones obtuvieron similitud 1.0 y compartieron:

```text
Adventure|Animation|Children|Comedy|Fantasy
```

**Pulp Fiction (1994)**

Nueve recomendaciones compartieron exactamente:

```text
Comedy|Crime|Drama|Thriller
```

con similitud 1.0. Una recomendación obtuvo 0.928515 al compartir tres de esos cuatro géneros.

**Titanic (1997)**

Las 10 recomendaciones compartieron:

```text
Drama|Romance
```

con similitud 1.0.

En las tres consultas la película utilizada como referencia no apareció en su propio Top-10.

## 8. Factorización colaborativa

LAB09 incorpora una factorización matricial mediante factores latentes entrenados con descenso de gradiente estocástico.

La configuración base es:

* Factores: **20**.
* Épocas: **12**.
* Seed: **42**.
* Learning rate: `0.01`.
* Regularización: `0.05`.

La división de evaluación es temporal:

1. Se ordenan las valoraciones por usuario y timestamp.
2. La última valoración de cada usuario se reserva como prueba.
3. Las restantes se utilizan para entrenamiento.

El experimento colaborativo se ejecuta con:

```bash
uv run python scripts/lab09_collaborative.py
```

El resultado se guarda en:

```text
reports/collaborative_metrics.json
```

Resultado obtenido:

* RMSE: **1.026418**.
* HitRate@10: **0.037479**.
* Cobertura del catálogo: **7.43%**.
* Tiempo de entrenamiento: aproximadamente **11.34 segundos**.
* Tamaño de factores: aproximadamente **1.57 MiB**.

## 9. Recomendación híbrida

El modelo híbrido combina la señal colaborativa con la similitud de contenido.

La puntuación utilizada es:

```text
hybrid_score = alpha * collaborative_score + (1 - alpha) * content_score
```

Se evaluaron dos valores de `alpha` manteniendo constantes:

* split temporal;
* factores;
* épocas;
* seed.

Configuraciones evaluadas:

```bash
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.25
uv run python scripts/lab09_hybrid.py --factors 20 --epochs 12 --alpha 0.75
```

### Comparación

| Alpha |     RMSE | HitRate@10 | Cobertura |
| ----: | -------: | ---------: | --------: |
|  0.25 | 1.026418 |   0.032368 |    10.60% |
|  0.75 | 1.026418 |   0.037479 |     7.72% |

Se selecciona **alpha = 0.75** porque obtiene mayor HitRate@10 bajo la misma semilla.

La configuración alpha 0.25 presenta mayor cobertura, por lo que existe un intercambio entre desempeño de ranking y cobertura.

El RMSE permanece igual porque alpha modifica el ranking híbrido, no las predicciones de valoración del modelo colaborativo.

El resultado principal se guarda en:

```text
reports/hybrid_metrics.json
```

## 10. Robustez por semillas

Para analizar la variabilidad se ejecutaron tres semillas con `alpha = 0.75`:

| Seed | Alpha |     RMSE | HitRate@10 | Cobertura | Tiempo aprox. |
| ---: | ----: | -------: | ---------: | --------: | ------------: |
|   42 |  0.75 | 1.026418 |   0.037479 |     7.72% |       11.35 s |
|  123 |  0.75 | 1.026084 |   0.028961 |     6.96% |       11.19 s |
| 2024 |  0.75 | 1.026561 |   0.035775 |     7.46% |       11.29 s |

Los resultados muestran variación en HitRate@10 entre semillas, mientras que el RMSE permanece alrededor de 1.026.

La comparación reproducible se almacena en:

```text
reports/pareto_comparison.csv
```

La tabla permite analizar conjuntamente desempeño de ranking, cobertura, tiempo y tamaño del modelo.

## 11. Tres perfiles y cold start

Se evaluaron tres perfiles:

* **Historial pequeño:** usuario 595.
* **Historial amplio:** usuario 414.
* **Usuario nuevo:** usuario 611.

Los usuarios con historial reciben recomendaciones híbridas.

Para el usuario nuevo no existe historial disponible, por lo que el sistema utiliza un fallback de popularidad.

La salida del usuario nuevo se marca explícitamente como:

```text
personalized = false
method = popularidad
```

Esto evita presentar una lista de popularidad como si fuera una recomendación personalizada.

El fallback se conserva en:

```text
reports/cold_start_fallback.csv
```

## 12. Cobertura, diversidad y riesgos

La cobertura se calcula sobre el catálogo completo de **9,742 películas**.

La configuración híbrida seleccionada alcanza **7.72%** de cobertura.

Alpha 0.25 alcanza **10.60%**, pero presenta menor HitRate@10.

La cobertura no debe interpretarse aisladamente: una mayor cobertura no implica necesariamente mejores recomendaciones.

El modelo de contenido presenta riesgo de sobre-especialización. Por ejemplo, Toy Story y Titanic generaron listas completas con similitud 1.0 debido a que muchas películas comparten exactamente los mismos géneros.

## 13. Costo computacional y Green AI

La configuración seleccionada utiliza:

* 20 factores.
* 12 épocas.
* aproximadamente 11.35 segundos de entrenamiento para seed 42.
* aproximadamente 1.57 MiB de factores almacenados.

Las tres semillas con alpha 0.75 tuvieron tiempos aproximados entre 11.19 y 11.35 segundos.

No se selecciona automáticamente el modelo más grande. La configuración se mantiene moderada y se compara considerando:

* desempeño;
* cobertura;
* tiempo;
* tamaño del modelo.

Esto permite documentar una decisión compatible con el principio de Green AI.

## 14. Riesgos principales y mitigaciones

### Dominancia de popularidad

El fallback puede concentrar las recomendaciones en películas con alta actividad.

**Mitigación:** declarar explícitamente cuándo la salida es no personalizada.

### Filtro burbuja y sobre-especialización

El contenido puede producir listas muy homogéneas.

**Mitigación:** combinar señales y evaluar cobertura además de HitRate@10.

### Sesgo de selección

MovieLens representa las interacciones observadas y no a la población general de espectadores.

**Mitigación:** interpretar los resultados como evidencia experimental.

### Ausencia de información demográfica

No se utilizan datos demográficos y, por tanto, no se realizan afirmaciones sobre representatividad por subgrupos.

### Bucle de retroalimentación

Un sistema desplegado podría reforzar las preferencias ya observadas.

**Mitigación:** este laboratorio utiliza evaluación offline y no presenta el sistema como mecanismo autónomo de decisión.

## 15. Aplicación Streamlit

Ejecutar:

```bash
uv run streamlit run app/streamlit_app.py
```

La interfaz permite seleccionar una película y obtener recomendaciones basadas en contenido.

La aplicación informa que el método de contenido utiliza TF-IDF de géneros con similitud coseno.

## 16. Limitaciones

* La matriz usuario-película es altamente dispersa.
* El modelo colaborativo depende del historial disponible.
* El modelo de contenido depende de la calidad de los géneros.
* El híbrido utiliza candidatos generados por el componente colaborativo.
* RMSE y HitRate@10 son métricas offline.
* Las métricas offline no sustituyen una evaluación con usuarios reales.
* MovieLens Latest Small es un dataset de desarrollo.
* Los resultados dependen de la versión concreta del dataset.
* No se utilizan atributos demográficos ni información sensible.

## 17. Evidencia reproducible

Los principales resultados se encuentran en:

```text
reports/popular_top10.csv
reports/content_recommendations.csv
reports/collaborative_metrics.json
reports/hybrid_metrics.json
reports/pareto_comparison.csv
reports/cold_start_fallback.csv
```

La documentación del sistema se encuentra en:

```text
docs/SYSTEM_CARD.md
```

La documentación del dataset se encuentra en:

```text
docs/DATASET_CARD.md
```

## 18. Requisitos para publicación

Las dependencias exportadas para entornos de publicación se encuentran en:

```text
requirements-cloud.txt
```

El dataset descargado no se versiona en Git. Se reproduce mediante el script de descarga.

## 19. Uso académico del dataset

MovieLens se utiliza bajo las condiciones establecidas por GroupLens. El dataset está destinado a investigación y desarrollo según sus condiciones de uso.

La cita correspondiente es:

Harper, F. M., & Konstan, J. A. (2015). *The MovieLens Datasets: History and Context*. ACM Transactions on Interactive Intelligent Systems, 5(4), 19:1–19:19. DOI: 10.1145/2827872.

## 20. Conclusión

El proyecto implementa un pipeline reproducible que parte de un baseline de popularidad y un recomendador por contenido y posteriormente incorpora factorización colaborativa y una estrategia híbrida.

La configuración seleccionada para LAB09 utiliza:

* **20 factores**.
* **12 épocas**.
* **alpha = 0.75**.
* **seed = 42**.

La selección se basa en la comparación offline con alpha 0.25 y en la evaluación de tres semillas.

El resultado híbrido seleccionado obtiene:

* RMSE: **1.026418**.
* HitRate@10: **0.037479**.
* Cobertura: **7.72%**.
* Tiempo de entrenamiento: aproximadamente **11.35 segundos**.
* Tamaño de factores: aproximadamente **1.57 MiB**.

La evidencia muestra un intercambio entre desempeño de ranking y cobertura. También se documentan explícitamente cold start, sobre-especialización, sesgo de selección, popularidad dominante y costo computacional.

El sistema debe interpretarse como un experimento reproducible de recomendación sobre MovieLens Latest Small y no como un predictor universal de preferencias.
