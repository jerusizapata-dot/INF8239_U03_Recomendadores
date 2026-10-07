# INF-8239 — Unidad 03 — Sistemas recomendadores

**Asignatura:** INF-8239 Ciencia de Datos II  
**Laboratorio:** U03.LAB08 — MovieLens, popularidad y recomendación por contenido  
**Autor académico:** Edwin Ramón José Nolasco

## 1. Objetivo

Este proyecto implementa un flujo reproducible de recomendación sobre el conjunto MovieLens Latest Small. Se construyen y auditan los datos, se calcula un baseline de popularidad suavizada y se desarrolla un recomendador por contenido basado en los géneros de las películas.

El sistema tiene finalidad académica y experimental. Una recomendación por similitud de contenido no representa una predicción de preferencia individual.

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

- Python 3.12
- `uv`
- Dependencias definidas en `pyproject.toml`

Instalación:

```bash
uv python install 3.12
uv sync
```

## 4. Pruebas

La suite completa se ejecuta con:

```bash
uv run pytest -q
```

Resultado verificado:

```text
7 passed
```

También se verificaron específicamente los contratos de datos y contenido:

```bash
uv run pytest tests/test_data.py tests/test_content.py -q
```

Resultado verificado:

```text
4 passed
```

## 5. Dataset MovieLens

Se utiliza **MovieLens Latest Small** de GroupLens.

Descarga:

```bash
uv run python scripts/download_data.py
```

Auditoría:

```bash
uv run python scripts/audit_data.py
```

La descarga utilizada presentó el siguiente SHA-256:

```text
696d65a3dfceac7c45750ad32df2c259311949efec81f0f144fdfb91ebc9e436
```

La versión auditada contiene:

- 610 usuarios.
- 9,742 películas en el catálogo.
- 9,724 películas con al menos una valoración.
- 100,836 valoraciones.
- Rango de valoración: 0.5–5.0.
- Media: 3.501557.
- Mediana: 3.5.
- Desviación estándar: 1.042529.
- Densidad usuario-película: 0.016968, aproximadamente 1.70%.

Los datos originales se descargan mediante el script y no se editan manualmente.

## 6. Baseline de popularidad

La popularidad se calcula mediante una media suavizada que combina la media de cada película con la media global y considera la cantidad de valoraciones. El umbral mínimo se obtiene mediante el percentil 80 del número de valoraciones.

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
3. Se calcula similitud coseno entre la película consultada y el catálogo.
4. Se excluye la propia película consultada.
5. Se devuelve el Top-10.

El resultado reproducible de la consulta principal se guarda en:

```text
reports/content_recommendations.csv
```

### Consultas verificadas

**Toy Story (1995)**

Las 10 recomendaciones obtuvieron una similitud de 1.0 y compartieron los géneros `Adventure|Animation|Children|Comedy|Fantasy`.

**Pulp Fiction (1994)**

Las recomendaciones incluyeron *Confessions of a Dangerous Mind (2002)*, *Fargo (1996)* e *In Bruges (2008)*. Nueve recomendaciones compartieron exactamente `Comedy|Crime|Drama|Thriller` y una obtuvo 0.928515 al compartir tres de esos cuatro géneros.

**Titanic (1997)**

Las 10 recomendaciones compartieron `Drama|Romance` y obtuvieron una similitud de 1.0.

En las tres consultas la película utilizada como referencia no apareció en su propio Top-10.

## 8. Aplicación Streamlit

Ejecutar:

```bash
uv run streamlit run app/streamlit_app.py
```

La interfaz permite seleccionar una película y obtener diez recomendaciones basadas en similitud de géneros.

La aplicación informa explícitamente que el método utilizado es TF-IDF de géneros con similitud coseno y advierte sobre el riesgo de sobre-especialización.

## 9. Cold start, cobertura y diversidad

El modelo de contenido no necesita historial de valoraciones para calcular similitud si la película tiene géneros registrados. Por ello puede representar una película nueva con información de contenido disponible.

Sin embargo, una película sin características de género informativas tendrá una representación limitada. Además, el recomendador no personaliza las recomendaciones para un usuario individual.

El catálogo contiene 9,742 películas y 18 no presentan valoraciones observadas. La matriz usuario-película tiene una densidad aproximada de 1.70%, lo que evidencia una alta dispersión.

Las consultas realizadas muestran riesgo de **sobre-especialización**: cuando varias películas comparten exactamente los mismos géneros, pueden aparecer numerosos empates con similitud 1.0. Esto reduce la diversidad del Top-k.

## 10. Limitaciones y riesgos

- La similitud de géneros no predice satisfacción individual.
- Las recomendaciones pueden ser muy homogéneas.
- La representación utiliza únicamente información de género.
- La matriz de valoraciones es altamente dispersa.
- MovieLens Latest Small es un dataset de desarrollo y sus contenidos pueden cambiar.
- Los resultados deben interpretarse según la versión concreta del dataset utilizada.
- No se realizan inferencias sobre atributos sensibles de los usuarios.

## 11. Documentación

La descripción del dataset se encuentra en:

```text
docs/DATASET_CARD.md
```

La descripción del sistema y sus riesgos se encuentra en:

```text
docs/SYSTEM_CARD.md
```

## 12. Requisitos para publicación

Las dependencias exportadas para entornos de publicación se encuentran en:

```text
requirements-cloud.txt
```

El dataset descargado no se versiona en Git. Se reproduce mediante el script de descarga.

## 13. Uso académico del dataset

MovieLens se utiliza bajo las condiciones establecidas por GroupLens. El dataset está destinado a investigación y desarrollo según sus condiciones de uso y no debe tratarse como un conjunto de datos representativo de toda la población de espectadores.

La cita correspondiente es:

Harper, F. M., & Konstan, J. A. (2015). *The MovieLens Datasets: History and Context*. ACM Transactions on Interactive Intelligent Systems, 5(4), 19:1–19:19. DOI: 10.1145/2827872.

## 14. Conclusión del laboratorio

**Resultado principal:** se implementó un pipeline reproducible de popularidad y recomendación por contenido sobre MovieLens.

**Evidencia utilizada:** auditoría del dataset, hash SHA-256, Top-10 de popularidad, tres consultas de contenido, aplicación Streamlit y siete pruebas automatizadas.

**Qué representa la similitud:** cercanía entre los géneros registrados de dos películas; no representa una predicción de gusto individual.

**Problema de cold start observado:** el modelo de contenido puede utilizar información de géneros sin historial de valoraciones, pero depende de disponer de características de contenido.

**Riesgo de sobre-especialización:** las recomendaciones pueden concentrarse en películas con exactamente los mismos géneros y producir empates con similitud 1.0.

**Siguiente experimento:** incorporar señales adicionales y evaluar estrategias que aumenten diversidad y personalización sin perder reproducibilidad.
