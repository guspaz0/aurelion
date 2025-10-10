## Pasos generales del programa (contrato mínimo)

- Entrada: archivos CSV en `src/bd/` con las estructuras descritas.
- Salida: archivos/objetos limpios y validados (por ejemplo, `clean/clientes.csv`, `clean/productos.csv`, `clean/ventas.csv`, `clean/detalle_ventas.csv`) y reportes de discrepancias (CSV o JSON con filas problemáticas).
- Errores esperados: filas con formatos inválidos, IDs faltantes, importes inconsistentes, categorías mal formateadas.

### Edge cases a cubrir

1. Filas con valores nulos o vacíos en columnas obligatorias.
2. Registros de venta cuyo `id_venta` no aparece en `detalle_ventas` (ventas sin detalle) o viceversa.
3. Productos referenciados en `detalle_ventas` que no existen en `productos.csv`.
4. Precios o cantidades negativos o no numéricos.

## Pasos detallados y pseudocódigo

1. Cargar CSVs en DataFrames (pandas) o listas de diccionarios.
2. Validar esquemas (columnas esperadas y tipos básicos).
3. Normalizar/castenar tipos (fechas -> datetime, números -> numeric).
4. Limpiar texto (trim, case normalization) y recategorizar productos por heurística simple.
5. Recalcular `importe` en `detalle_ventas` y marcar discrepancias.
6. Cruzar `ventas` y `detalle_ventas` para detectar ventas sin detalle y detalles sin venta.
7. Generar archivos limpios y un reporte de inconsistencias.

Pseudocódigo (alto nivel):

```python
# Cargar librerías
import pandas as pd

# 1. Cargar
clientes = pd.read_csv('src/bd/clientes.csv')
productos = pd.read_csv('src/bd/productos.csv')
ventas = pd.read_csv('src/bd/ventas.csv')
detalles = pd.read_csv('src/bd/detalle_ventas.csv')

# 2. Validar columnas esperadas
check_columns(clientes, expected_clientes_columns)

# 3. Normalizar tipos
clientes['fecha_alta'] = pd.to_datetime(clientes['fecha_alta'], errors='coerce')
productos['precio_unitario'] = pd.to_numeric(productos['precio_unitario'], errors='coerce')
detalles['cantidad'] = pd.to_numeric(detalles['cantidad'], errors='coerce')
detalles['precio_unitario'] = pd.to_numeric(detalles['precio_unitario'], errors='coerce')

# 4. Limpieza y recategorización (heurística simple)
productos['categoria'] = productos['categoria'].str.strip().str.title()
productos = recategorizar_por_nombre(productos)

# 5. Recalcular importe y comparar
detalles['importe_calc'] = detalles['cantidad'] * detalles['precio_unitario']
detalles['importe_ok'] = detalles['importe'] == detalles['importe_calc']

# 6. Detectar inconsistencias
ventas_sin_detalle = set(ventas['id_venta']) - set(detalles['id_venta'])
detalles_sin_venta = set(detalles['id_venta']) - set(ventas['id_venta'])

# 7. Guardar resultados limpios y reportes
productos.to_csv('clean/productos.csv', index=False)
clientes.to_csv('clean/clientes.csv', index=False)
ventas.to_csv('clean/ventas.csv', index=False)
detalles.to_csv('clean/detalle_ventas.csv', index=False)
report_inconsistencias(...)
```