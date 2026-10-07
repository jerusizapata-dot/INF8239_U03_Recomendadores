# System Card — Recomendador

## Usuarios y propósito

El sistema tiene propósito académico y experimental: evaluar un pipeline reproducible de recomendación sobre MovieLens Latest Small, comparando popularidad, contenido, factorización colaborativa y una combinación híbrida.

El sistema no predice de forma directa si una persona disfrutará una película. Las recomendaciones son resultados de evaluación offline y no predicciones universales de preferencias.

## Catálogo y candidatos

El catálogo contiene **9,742 películas**, de las cuales **9,724** presentan al menos una valoración observada.

El recomendador por contenido utiliza el catálogo como conjunto de candidatos y excluye la película consultada. El modelo colaborativo excluye películas ya valoradas durante el entrenamiento. El híbrido combina las señales colaborativa y de contenido sobre los candidatos colaborativos.

## Señales utilizadas

- **Valoraciones:** `userId`, `movieId`, `rating` y `timestamp`.
- **Contenido:** géneros de `movies.csv`, transformados a texto y representados mediante TF-IDF.
- **Popularidad:** cantidad y media de valoraciones para el baseline y el fallback de cold start.

No se utilizan atributos demográficos ni información sensible.

## División temporal

La evaluación colaborativa utiliza **leave-one-out temporal por usuario**. Para cada usuario, las valoraciones se ordenan por `timestamp` y la última se reserva como prueba; las restantes se utilizan para entrenamiento.

## Modelos

### Popularidad suavizada

Combina la media de cada película con la media global y pondera la cantidad de observaciones. El umbral mínimo se obtiene mediante el percentil 80 del número de valoraciones.

### Recomendación por contenido

Utiliza TF-IDF sobre los géneros y similitud coseno. El Top-10 excluye la película consultada.

### Factorización colaborativa

Se implementa factorización matricial mediante descenso de gradiente estocástico.

Configuración base:

- Factores: **20**.
- Épocas: **12**.
- Semilla: **42**.
- Learning rate: `0.01`.
- Regularización: `0.05`.

La predicción utiliza la media global más el producto punto entre los factores latentes del usuario y de la película.

### Modelo híbrido

Combina señal colaborativa normalizada y similitud de contenido normalizada:

`hybrid_score = alpha * collaborative_score + (1 - alpha) * content_score`

Se evaluaron `alpha = 0.25` y `alpha = 0.75`, manteniendo constantes factores, épocas, split y semilla.

Se seleccionó **alpha = 0.75** porque obtuvo mayor `HitRate@10` bajo la misma semilla:

- alpha 0.75: **HitRate@10 = 0.03748**, cobertura = **7.72%**.
- alpha 0.25: **HitRate@10 = 0.03237**, cobertura = **10.60%**.

La decisión prioriza el desempeño de ranking observado, aceptando menor cobertura.

## Métricas offline

Para valoración se utiliza **RMSE**. Para ranking se utiliza **HitRate@10**. La cobertura es la proporción de películas del catálogo completo de **9,742 películas** que aparecen en las recomendaciones.

Configuración colaborativa base:

- RMSE: **1.026418**.
- HitRate@10: **0.037479**.
- Cobertura: **7.43%**.

Configuración híbrida seleccionada, alpha 0.75, seed 42:

- RMSE: **1.026418**.
- HitRate@10: **0.037479**.
- Cobertura: **7.72%**.

El RMSE permanece igual porque el híbrido modifica el ranking, pero no las predicciones de valoración.

## Robustez por semillas

| Seed | Alpha | RMSE | HitRate@10 | Cobertura |
|---:|---:|---:|---:|---:|
| 42 | 0.75 | 1.026418 | 0.037479 | 7.72% |
| 123 | 0.75 | 1.026084 | 0.028961 | 6.96% |
| 2024 | 0.75 | 1.026561 | 0.035775 | 7.46% |

Los resultados muestran variación en el ranking entre semillas, mientras el RMSE permanece alrededor de 1.026.

## Cold start

Para un usuario nuevo sin historial se utiliza un fallback basado en popularidad y se marca la salida como **no personalizada**. Para usuarios con historial se generan recomendaciones híbridas.

## Cobertura y diversidad

La configuración híbrida seleccionada alcanzó **7.72%** de cobertura, mientras alpha 0.25 alcanzó **10.60%**.

Una cobertura mayor no implica mejores recomendaciones; debe analizarse junto con HitRate@10.

El modelo de contenido presenta riesgo de sobre-especialización porque películas con los mismos géneros pueden obtener similitud coseno de **1.0**.

## Costo computacional y Green AI

La configuración seleccionada utiliza 20 factores y 12 épocas.

Para seed 42:

- Tiempo de entrenamiento: aproximadamente **11.35 segundos**.
- Tamaño de los factores almacenados: aproximadamente **1.57 MiB**.

Las tres semillas con alpha 0.75 presentaron tiempos entre aproximadamente **11.19 y 11.35 segundos**.

La selección no utiliza automáticamente el mayor modelo; se mantiene una configuración moderada y se compara desempeño, cobertura y costo.

## Riesgos y mitigación

- **Dominancia de popularidad:** el fallback puede concentrar recomendaciones en películas muy activas. Se declara explícitamente cuándo la salida no es personalizada.
- **Filtro burbuja y sobre-especialización:** el contenido puede producir listas homogéneas. Se evalúa cobertura junto con HitRate@10 y se combina con colaboración.
- **Sesgo de selección:** MovieLens representa usuarios e interacciones observadas, no a la población general. Los resultados se interpretan como evidencia experimental.
- **Ausencia de información demográfica:** limita el análisis de representatividad por subgrupos.
- **Bucle de retroalimentación:** un sistema desplegado podría reforzar preferencias observadas. En este laboratorio la evaluación es offline y no se presenta como decisión autónoma.

## Limitaciones

- La matriz usuario-película es altamente dispersa.
- El modelo colaborativo depende del historial disponible.
- El modelo de contenido depende de la calidad de los géneros.
- El híbrido utiliza candidatos generados por el componente colaborativo.
- RMSE y HitRate@10 son métricas offline y no sustituyen una evaluación con usuarios reales.
- MovieLens Latest Small es un dataset de desarrollo y los resultados dependen de su versión.

## Archivos de evidencia

- `reports/popular_top10.csv`
- `reports/content_recommendations.csv`
- `reports/collaborative_metrics.json`
- `reports/hybrid_metrics.json`
- `reports/pareto_comparison.csv`
- `reports/cold_start_fallback.csv`

## Conclusión

El laboratorio muestra una arquitectura reproducible que combina popularidad, contenido y colaboración.

La configuración seleccionada utiliza **20 factores, 12 épocas y alpha 0.75**, priorizando HitRate@10 frente a alpha 0.25 bajo el mismo experimento.

El resultado es una evaluación offline sobre MovieLens Latest Small, con limitaciones derivadas de dispersión, sesgo de selección, sobre-especialización y ausencia de interacción real con usuarios.