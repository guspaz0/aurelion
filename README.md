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


# Entrega 2: Actualizacion

## Migración de datos: CSV → SQLite

- **Resumen:** el proyecto incluye un flujo sencillo para migrar los datos originales en CSV a una base de datos SQLite (`src/bd/bd.sqlite`). La migración valida, normaliza y carga los archivos CSV (`clientes.csv`, `productos.csv`, `ventas.csv`, `detalle_ventas.csv`) en tablas relacionales y crea vistas útiles para análisis.

- **Cómo funciona (alto nivel):**
    - Al inicializar la aplicación (instanciando `App` en `src/app_state.py`) se crea una conexión gestionada por `modules.db.db_connection.DbConnection`.
    - `DbConnection` crea las tablas necesarias y llama a los métodos `_load_from_csv()` de cada DAO (`ClientesDao`, `ProductoDao`, `VentasDao`, `DetalleVentasDao`) cuando las tablas están vacías.
    - Cada DAO valida y transforma los datos (tipos, fechas, recomputación de importes) antes de insertarlos en la base.

- **Reproducir la migración (rápido):** ejecutar desde la raíz del proyecto con `src` en `PYTHONPATH`:

```bash
PYTHONPATH=src python3 -c "from app_state import App; App()"
```

- **Notas:** revisa los CSV por inconsistencias antes de la migración; por defecto los DAOs insertan registros según los CSV (no realizan deduplicación avanzada). Para ETL más robusto, extrae y extiende los `_load_from_csv()` o añade un paso previo de limpieza.


**Análisis Exploratorio de Datos (EDA)**

- **Objetivo:** entender la calidad y las características principales de los datos (clientes, productos, ventas y detalle de ventas) para guiar limpieza, normalización y análisis posteriores.

- **Estadísticas descriptivas básicas calculadas:** conteo, media, mediana, desviación estándar, mínimo, máximo y percentiles para variables numéricas (por ejemplo `precio_unitario`, `cantidad`, `importe`), y tablas de frecuencia para variables categóricas (`categoria`, `medio_pago`, `ciudad`).

- **Identificación del tipo de distribución de variables:** inspección visual mediante histogramas y QQ-plots; pruebas estadísticas opcionales (Shapiro-Wilk, Kolmogorov-Smirnov) para caracterizar si variables siguen distribuciones aproximadas (normal, log-normal, etc.).

- **Análisis de correlaciones entre variables principales:** cálculo de correlaciones de Pearson y Spearman según corresponda; matriz de correlación y mapa de calor (heatmap) para identificar relaciones entre `precio_unitario`, `cantidad`, `importe` y agregados por producto/cliente.

- **Detección de outliers (valores extremos):** identificación mediante IQR (1.5×IQR) y puntuaciones Z; revisión de casos atípicos para decidir si corregir, recomputar o excluir (p. ej. `importe` que no coincide con `cantidad * precio_unitario`).

- **Gráficos representativos (al menos 3):**
    - Histogramas de `precio_unitario` y `importe` (distribución de precios e importes)
    - Boxplots por `categoria` para comparar dispersión y detectar outliers por categoría
    - Heatmap de correlaciones entre variables numéricas
    - (Adicionales recomendados) Series temporales de ventas, mapa/tabla de ventas por `ciudad`, gráfico de barras de productos más vendidos

- **Interpretación de resultados orientada al problema:** cada resultado del EDA debe traducirse a acciones concretas: recategorización de productos con incoherencias, recomputación de importes erróneos, identificación de clientes o periodos atípicos que requieren limpieza o verificación, y recomendaciones para mejorar la calidad de los CSV de origen.


# Entrega 3: Machine Learning con scikit-learn

## Modelo de Predicción de Importe Total de Ventas

**📊 Resumen:**
Se ha implementado un modelo de **Regresión Lineal** para predecir el importe total de ventas basándose en características como cantidad de items, mes, día de la semana y método de pago.

**🎯 Resultados:**
- **R² (Test Set): 0.787** - El modelo explica el 78.7% de la varianza
- **MAE (Test Set): $5,158.86** - Error promedio manejable
- **Sin overfitting evidente** - Balance correcto entre train/test

### Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `src/modules/ml/predictor_model.py` | Clase `VentasPredictorModel` con lógica completa de ML |
| `src/ml_analysis.ipynb` | Notebook con análisis, entrenamiento y visualizaciones |
| `docs/ML_DOCUMENTATION.md` | 📋 Documentación detallada del proyecto |
| `src/requirements.txt` | Actualizado con `scikit-learn==1.5.2` |

### Cómo Ejecutar el Análisis

```bash
# 1. Activar entorno virtual
source aurelion/bin/activate

# 2. Instalar dependencias
pip install -r src/requirements.txt

# 3. Abrir notebook
jupyter notebook src/ml_analysis.ipynb
```

### Modelo & Características

**Algoritmo:** Regresión Lineal  
**Entrada (X):** 8 características
- `cantidad`: Cantidad total de items vendidos
- `mes`: Mes de la venta (1-12)
- `dia`: Día del mes (1-31)
- `dia_semana`: Día de la semana (0-6)
- `pago_*`: Método de pago (one-hot encoded)

**Salida (y):** `importe` (valor numérico continuo)

### División Train/Test
- **Entrenamiento:** 96 muestras (80%)
- **Prueba:** 24 muestras (20%)
- **Random state:** 42 (reproducibilidad)

### Métricas Principales

| Métrica | Entrenamiento | Prueba |
|---------|---|---|
| MAE | $5,516.52 | $5,158.86 |
| RMSE | 7,077.96 | 6,641.64 |
| R² | 0.7046 | **0.7870** |

### Visualizaciones Generadas
1. ✅ Matriz de Correlación (características vs target)
2. ✅ Predicción vs Real (scatter plots train/test)
3. ✅ Análisis de Residuos (4 gráficos: residuos, histograma, Q-Q plot, secuencia)
4. ✅ Importancia de Características (coeficientes del modelo)

### Características Más Importantes
1. **cantidad** (coef: 10,517.55) - Característica dominante
2. **mes** (coef: 1,092.58) - Efecto temporal
3. **pago_efectivo** (coef: 717.63) - Método de pago

### Documentación Completa
📖 **Ver:** `docs/ML_DOCUMENTATION.md` para detalles extensos incluyendo:
- Objetivo y justificación del algoritmo
- Fórmulas matemáticas completas
- Análisis detallado de métricas
- Limitaciones y mejoras futuras
- Cómo integrar el modelo en producción

- **Reproducir el EDA:** existe el notebook `src/prueba_entidades.ipynb` que puede usarse como punto de partida para visualizar y calcular las métricas anteriores. Pasos rápidos:

```bash
# (1) Crear e activar entorno si no está activo
python3 -m venv .venv
source .venv/bin/activate

# (2) Instalar dependencias (si no están en `src/requirements.txt`, instalar pandas, matplotlib, seaborn, scipy)
pip install -r src/requirements.txt || pip install pandas matplotlib seaborn scipy

# (3) Abrir el notebook
python3 -m jupyter notebook src/prueba_entidades.ipynb
```

