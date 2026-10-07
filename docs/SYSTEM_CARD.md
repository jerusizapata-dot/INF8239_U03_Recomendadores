# System Card — Recomendador

## Usuarios y propósito

El sistema tiene como propósito experimental recomendar películas similares a una película seleccionada y generar un ranking de popularidad. El laboratorio está orientado a evaluar modelos reproducibles de recomendación sobre MovieLens Latest Small.

El sistema no predice de forma directa si una persona disfrutará una película. En el recomendador por contenido, la similitud representa únicamente la cercanía entre las características de género registradas para las películas.

## Catálogo y candidatos

El catálogo contiene **9,742 películas**, de las cuales **9,724** presentan al menos una valoración observada. Las películas se cargan desde `data/raw/ml-latest-small/movies.csv`.

El recomendador por contenido considera las películas del catálogo como candidatas y excluye explícitamente la película utilizada como consulta del Top-k resultante.

## Señales utilizadas

El modelo de contenido utiliza únicamente los géneros registrados en `movies.csv`. Los géneros separados por `|` se transforman en texto y se representan mediante TF-IDF.

Las valoraciones (`rating`) y sus cantidades se utilizan para el baseline de popularidad suavizada, pero no forman parte de la similitud de contenido.

## Modelos y fallback

Se implementan dos componentes principales en este laboratorio:

1. **Popularidad suavizada:** combina la media de valoración de cada película con la media global y pondera la cantidad de observaciones. Se utiliza un umbral basado en el percentil 80 del número de valoraciones.
2. **Recomendación por contenido:** utiliza TF-IDF sobre los géneros y similitud coseno. El Top-10 excluye la película consultada.

El laboratorio no implementa todavía un fallback híbrido entre ambos modelos. La popularidad funciona como baseline independiente.

## Métricas offline

Para la popularidad se conserva `reports/popular_top10.csv`, con `count`, `mean` y `weighted_score`.

El Top-10 de popularidad obtenido fue encabezado por *Shawshank Redemption, The (1994)* con un `weighted_score` de **4.395194**, seguido por *Godfather, The (1972)* con **4.242739** y *Fight Club (1999)* con **4.232690**.

Para el modelo de contenido se utiliza `content_score`, basado en similitud coseno. Las consultas realizadas fueron:

- **Toy Story (1995):** las 10 recomendaciones obtuvieron `1.0` y compartieron `Adventure|Animation|Children|Comedy|Fantasy`.
- **Pulp Fiction (1994):** 9 recomendaciones obtuvieron `1.0` al compartir `Comedy|Crime|Drama|Thriller`; una obtuvo **0.928515** al compartir tres de esos cuatro géneros.
- **Titanic (1997):** las 10 recomendaciones obtuvieron `1.0` y compartieron `Drama|Romance`.

La película consultada no apareció en ninguno de los tres Top-10.

## Cold start, cobertura y diversidad

**Cold start:** el recomendador por contenido puede representar una película nueva si dispone de sus géneros, porque no necesita valoraciones históricas para calcular la similitud. Sin embargo, una película sin géneros informativos tendrá una representación limitada.

**Cobertura:** el catálogo contiene 9,742 películas y 9,724 tienen valoraciones observadas. Hay 18 películas sin valoraciones observadas. La matriz usuario-película tiene una densidad de **1.70%**, por lo que aproximadamente el **98.3%** de las combinaciones posibles no tienen valoración observada.

**Diversidad:** las consultas muestran un riesgo de baja diversidad cuando muchas películas comparten exactamente los mismos géneros. En Toy Story y Titanic se observan listas completas con `content_score = 1.0`, lo que evidencia recomendaciones muy homogéneas.

## Riesgos y monitoreo

El principal riesgo observado es la **sobre-especialización**: el modelo puede concentrar el Top-k en películas con exactamente los mismos géneros que la consulta.

También existen empates frecuentes porque el modelo utiliza un conjunto reducido de características. Un `content_score` de `1.0` no implica igualdad de películas ni predice satisfacción del usuario; indica máxima similitud dentro de las características de género utilizadas.

El dataset presenta además una matriz de valoraciones muy dispersa y sesgos derivados de los usuarios e interacciones observadas en MovieLens. Por estas razones, los resultados deben interpretarse como evidencia experimental y no como predicciones universales de preferencias.
