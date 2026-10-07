# Dataset Card — MovieLens

## Fuente, fecha, versión y hash

**Fuente:** GroupLens — MovieLens Latest Small (`ml-latest-small`).

**Dataset descargado:** 7 de octubre de 2026.

**Archivo de descarga:** `https://files.grouplens.org/datasets/movielens/ml-latest-small.zip`

**SHA-256 de la descarga:** `696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436`

El conjunto descargado contiene las actividades de valoración y etiquetado de usuarios de MovieLens. La versión utilizada contiene 100,836 valoraciones y 9,742 películas.

## Licencia y cita

MovieLens se distribuye bajo las condiciones de uso indicadas por GroupLens. El dataset está destinado a fines de investigación y desarrollo; no debe utilizarse con fines comerciales o generadores de ingresos sin autorización. Las redistribuciones deben mantener las condiciones establecidas por GroupLens.

**Cita:**

Harper, F. M., & Konstan, J. A. (2015). *The MovieLens Datasets: History and Context*. ACM Transactions on Interactive Intelligent Systems, 5(4), 19:1–19:19. DOI: 10.1145/2827872.

## Archivos y diccionario

El conjunto `ml-latest-small` contiene:

- `ratings.csv`: `userId`, `movieId`, `rating`, `timestamp`.
- `movies.csv`: `movieId`, `title`, `genres`.
- `tags.csv`: `userId`, `movieId`, `tag`, `timestamp`.
- `links.csv`: `movieId`, `imdbId`, `tmdbId`.
- `README.txt`: documentación oficial del dataset.

Las valoraciones están en una escala de **0.5 a 5.0**, en incrementos de media estrella. Los timestamps están expresados como segundos desde el epoch UTC. Los géneros de las películas están separados por `|`.

## Procedimiento de descarga

La descarga se realiza mediante:

```text
uv run python scripts/download_data.py
```

El script descarga el archivo desde la URL configurada en `.env.example`, lo almacena en `data/raw` y calcula su SHA-256. Los datos originales no se editan manualmente.

## Población observada y exclusiones

El dataset contiene:

- **610 usuarios**.
- **9,742 películas** en el catálogo.
- **9,724 películas** con al menos una valoración observada.
- **100,836 valoraciones**.
- Rango de valoración: **0.5–5.0**.
- Media de valoración: **3.501557**.
- Mediana: **3.5**.
- Desviación estándar: **1.042529**.
- Densidad de la matriz usuario-película: **0.016968**, aproximadamente **1.70%**.

Los usuarios fueron seleccionados aleatoriamente y cada usuario incluido había valorado al menos 20 películas. No se proporcionan datos demográficos de los usuarios y los identificadores son anonimizados.

Hay 18 películas del catálogo que no presentan valoraciones observadas. No se eliminan como parte de la auditoría, porque forman parte del catálogo original.

## Calidad, sesgos y usos prohibidos

La matriz de valoraciones es altamente dispersa: aproximadamente el 98.3% de las combinaciones usuario-película no tienen una valoración observada. Esta dispersión limita la capacidad de inferir preferencias para usuarios o películas con poca información.

El dataset presenta sesgos de selección y actividad: representa a los usuarios seleccionados por MovieLens y sus interacciones registradas, no a la población general de espectadores. Además, no contiene información demográfica que permita evaluar representatividad por grupos.

MovieLens Latest Small es un **dataset de desarrollo** y su contenido puede cambiar. Por ello, no debe utilizarse como base para resultados de investigación compartidos sin considerar la versión concreta y las condiciones indicadas por GroupLens.

En este laboratorio no se utilizan datos personales identificables ni se intenta inferir atributos sensibles de los usuarios. El dataset no debe emplearse para decisiones de alto impacto sobre personas.
