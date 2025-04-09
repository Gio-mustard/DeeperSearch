# Documentación del Web Scraper Module

## Visión General

Este módulo ofrece una solución de web scraping simple pero potente construida sobre el framework Scrapy. Permite extraer contenido de múltiples páginas web de manera eficiente, contando con funciones integradas para el manejo de grandes lotes de URLs, logging y caching de contenido.

## Arquitectura

El scraper está organizado en los siguientes componentes:

1. **Punto de Entrada Principal** ([`main.py`](./main.py)): Contiene la clase `Scrapper` que orquesta el proceso de scraping.
2. **Spider** ([`scraper/spiders/page.py`](./scraper/spiders/page.py)): Define el `PageSpider` que se encarga del crawling real de las páginas web.
3. **Pipeline** ([`scraper/pipelines.py`](./scraper/pipelines.py)): Procesa y almacena los datos extraídos.
4. **Items** ([`scraper/items.py`](./scraper/items.py)): Define la estructura de datos para el contenido extraído.

## Componentes Principales

### Clase Scrapper {#clase-scrapper}

La clase `Scrapper` en [`main.py`](#clase-scrapper) es el punto de entrada principal para usar el scraper. Se encarga de:

- Inicializar el proceso del crawler de Scrapy con la configuración adecuada.
- Agrupar URLs en lotes manejables para prevenir problemas de memoria.
- Iniciar el proceso de scraping.
- Recuperar resultados desde el cache.

```python
scrapper = Scrapper(show_logs=False)
results = scrapper.start(["https://example.com", "https://example.org"])
```

### PageSpider {#pagespider}

La clase [`PageSpider`](./scraper/spiders/page.py) se encarga del crawling real de las páginas web:

- Procesa cada URL proporcionada.
- Extrae el título y el contenido de la página.
- Valida las respuestas para asegurar la calidad de los datos.
- Genera items estructurados con la información extraída.

### PagePipeline {#pagepipeline}

La clase [`PagePipeline`](./scraper/pipelines.py)  procesa los items extraídos:

- Almacena el contenido en un cache para una rápida recuperación.
- Opcionalmente, guarda logs de los datos extraídos en archivos.
- Maneja errores durante el procesamiento de los datos.

### Items Module {#items-module}

El módulo [`items.py`](./scraper/items.py) define la estructura de datos para el contenido extraído de las páginas web:

- Contiene las clases que representan los items extraídos.
- Define los campos y tipos de datos para cada item.
- Facilita el procesamiento estructurado de la información.

## Ejemplos de Uso

### Uso Básico

```python
from scraper.main import Scrapper  # Importar la clase [`Scrapper`](#clase-scrapper)

# Crear una instancia del scraper (desactivar logs para una operación silenciosa)
scrapper = Scrapper(show_logs=False)

# Definir una lista de URLs para extraer datos
urls = [
    "https://example.com",
    "https://example.org",
    "https://example.net"
]

# Iniciar el scraping y obtener resultados
results = scrapper.start(urls)

# Procesar los resultados
for url, content in zip(urls, results):
    print(f"Contenido de {url}: {content[:100]}...")  # Imprime los primeros 100 caracteres
```

### Con Logging Activado

```python
# Crear un scraper con logging activado
scrapper = Scrapper(show_logs=True)

# El scraper ahora mostrará logs en la consola
# y guardará logs detallados en archivos dentro del directorio 'results'
results = scrapper.start(["https://example.com"])
```

### Manejo de Grandes Cantidades de URLs

El scraper maneja automáticamente grandes lotes de URLs agrupándolas:

```python
# Crear una lista de muchas URLs
many_urls = ["https://example.com/" + str(i) for i in range(5000)]

# El scraper procesará automáticamente estas URLs en grupos de 1000
scrapper = Scrapper()
results = scrapper.start(many_urls)
```

## Detalles Técnicos

### Agrupación de URLs {#agrupacion-de-urls}

Para prevenir problemas de memoria al extraer datos de muchas URLs, el método `__group_links` divide listas grandes en lotes más pequeños (por defecto: 1000 URLs por lote).

### Mecanismo de Caching {#mecanismo-de-caching}

El [`PagePipeline`](./scraper/pipelines.py) mantiene un diccionario estático de cache que mapea URLs a su contenido, lo que permite una rápida recuperación de resultados tras el scraping.

### Logging

Cuando está habilitado, el scraper crea archivos de log con sello de tiempo en el directorio `results`, los cuales contienen:
- La URL que se ha extraído.
- El título de la página.
- El contenido completo de la página.

## Configuración

El scraper utiliza el sistema de settings de Scrapy, con algunos valores por defecto que pueden ser modificados:

- `ROBOTSTXT_OBEY = True`: Respeta las reglas del robots.txt.
- `DOWNLOAD_DELAY = 2`: Espera 2 segundos entre solicitudes al mismo dominio.
- User agent personalizado para simular un navegador Firefox.

## Manejo de Errores {#manejo-de-errores}

El scraper incluye varios mecanismos de manejo de errores:

- Validación de los códigos de estado de las respuestas.
- Verificación de respuestas vacías.
- Manejo de excepciones en el pipeline.
- Logging de solicitudes fallidas.

## Consideraciones de Rendimiento {#consideraciones-de-rendimiento}

- El scraper procesa las URLs en lotes para gestionar el uso de memoria.
- Utiliza la arquitectura asíncrona de Scrapy para un crawling eficiente con [`PageSpider`](./scraper/spiders/page.py).
- El [mecanismo de caching](#mecanismo-de-caching) permite una rápida recuperación de los resultados.

## Cómo Usar Esta Documentación {#como-usar-esta-documentacion}

Este archivo README.md proporciona una visión completa de tu módulo de scraper. Explica:

1. La arquitectura y los componentes del scraper.
2. Cómo utilizar la clase [`Scrapper`](./main.py) desde [`main.py`](./main.py).
3. Ejemplos para diferentes casos de uso.
4. Detalles técnicos sobre el funcionamiento interno del scraper.
