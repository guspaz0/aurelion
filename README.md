# Tienda Aurelion

Proyecto para guayerd, fundamentos de inteligencia artificial.

## Introduccion

Aurelion es una tienda/despensa/supermercado que vende productos de limpieza y alimentos al por menor y mayor. Desarrolla sus actividades principales dentro de la provincia de cordoba, Argentina.

## Observaciones

la base de datos presenta inconsistencias en los campos de las tablas siguintes: 
- `productos`:
    - `categorias`: el nombre de la categoria es inconsistente con la descripcion del producto. Se le pidio a GPT-5 mini que lo corrija. lo corrijio pero aun asi se encontraron 2 articulos mal categorizados.


## Resumen del proyecto (tema / problema / solución)

- Tema: análisis y limpieza de ventas y catálogos de una pequeña tienda local para soportar consultas, reportes y análisis simples (clientes, productos, ventas y detalle de ventas).
- Problema: la base de datos provista (CSV en `src/bd/`) contiene inconsistencias y redundancias (por ejemplo, categorías mal asignadas en `productos`, campos duplicados en `ventas` y posibles errores de integridad entre `ventas` y `detalle_ventas`). Estas inconsistencias dificultan el análisis y pueden causar errores en agregaciones o reportes.
- Solución propuesta: implementar un pequeño flujo ETL en Python que:
    1. cargue y valide los archivos CSV,
    2. limpie y normalice columnas problemáticas (p. ej. categorías de productos),
    3. detecte y reporte discrepancias (ventas sin detalle, productos sin categoría válida),
    4. genere tablas/archivos limpios listos para análisis y para ser consumidos por los módulos del proyecto (`modules/*`).

La solución está pensada para integrarse con la estructura del repositorio (módulos `clientes`, `productos`, `ventas`) y proveer servicios de acceso y limpieza reutilizables.

## Fuente de datos y definición

Los datos provienen de archivos CSV incluidos en `src/bd/`. A continuación se describen las tablas, sus columnas y los tipos estimados (según una inspección inicial de los archivos):

- `clientes.csv`
    - Columnas: `id_cliente` (entero), `nombre_cliente` (texto), `email` (texto), `ciudad` (texto), `fecha_alta` (fecha, AAAA-MM-DD)
    - Observaciones: emails y nombres repetidos posibles; `id_cliente` debería ser único.

- `productos.csv`
    - Columnas: `id_producto` (entero), `nombre_producto` (texto), `categoria` (texto), `precio_unitario` (numérico entero, moneda en centavos ó unidades locales)
    - Observaciones: categorías inconsistentes con el nombre/Descripción del producto (se detectaron casos que requieren recategorización manual o heurística).

- `ventas.csv`
    - Columnas: `id_venta` (entero), `fecha` (fecha), `id_cliente` (entero), `nombre_cliente` (texto), `email` (texto), `medio_pago` (texto)
    - Observaciones: contiene datos redundantes del cliente (`nombre_cliente`, `email`) además del `id_cliente`. Esto facilita lectura rápida, pero rompe la normalización y puede causar inconsistencias.

- `detalle_ventas.csv`
    - Columnas: `id_venta` (entero), `id_producto` (entero), `nombre_producto` (texto), `cantidad` (entero), `precio_unitario` (numérico), `importe` (numérico)
    - Observaciones: `importe` suele ser `cantidad * precio_unitario`, pero conviene validar y recomputar para detectar errores.

## Estructura, tipos y escala de los datos (inspección rápida)

Conteo de líneas (incluye encabezado) en los CSV provistos en `src/bd/`:

- `clientes.csv`: 100 líneas (99 registros aproximadamente)
- `productos.csv`: 101 líneas (100 registros aproximadamente)
- `ventas.csv`: 120 líneas (119 registros aproximadamente)
- `detalle_ventas.csv`: 343 líneas (342 registros aproximadamente)

Total aproximado de registros (sin contar encabezados): 660 filas.

Nota sobre escala: es un dataset pequeño, adecuado para prácticas y demostraciones. El flujo diseñado prioriza claridad, validación y trazabilidad más que optimizaciones de rendimiento a gran escala.
