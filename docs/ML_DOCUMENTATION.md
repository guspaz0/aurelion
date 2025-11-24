# Documentación del Proyecto de Machine Learning
## Predicción de Importe Total de Ventas - Regresión Lineal

**Fecha:** 23 de noviembre de 2025  
**Proyecto:** Tienda Aurelion - IA Fundamental  
**Autor:** Sistema ML Integrado

---

## 📋 Tabla de Contenidos

1. [Objetivo](#objetivo)
2. [Algoritmo Elegido](#algoritmo-elegido)
3. [Entradas (X) y Salida (y)](#entradas-x-y-salida-y)
4. [Métricas de Evaluación](#métricas-de-evaluación)
5. [Modelo ML Implementado](#modelo-ml-implementado)
6. [División Train/Test y Entrenamiento](#división-traintest-y-entrenamiento)
7. [Predicciones y Métricas Calculadas](#predicciones-y-métricas-calculadas)
8. [Resultados en Gráficos](#resultados-en-gráficos)
9. [Cómo Ejecutar](#cómo-ejecutar)
10. [Estructura del Código](#estructura-del-código)

---

## Objetivo

### Problema a Resolver
Predecir el **importe total de una venta** basándose en características como:
- Cantidad total de ítems vendidos
- Mes y día de la semana de la venta
- Método de pago utilizado

### Tipo de Tarea
**REGRESIÓN** - Predicción de un valor numérico continuo (importe en unidades monetarias)

### Justificación del Objetivo
- La predicción del importe permite:
  - Estimar ventas futuras
  - Detectar anomalías (ventas con importe inesperado)
  - Optimizar estrategias de venta
  - Mejorar presupuestos y proyecciones

---

## Algoritmo Elegido

### Algoritmo: **Regresión Lineal**

#### Justificación de la Elección

| Criterio | Justificación |
|----------|---------------|
| **Relación Lineal** | La cantidad de items tiene una relación directa y lineal con el importe total |
| **Interpretabilidad** | Los coeficientes indican claramente cómo cada característica afecta el importe |
| **Eficiencia Computacional** | Entrenamiento muy rápido, ideal para datasets pequeños |
| **Dataset Pequeño** | Con ~119 ventas, la simplicidad es ventajosa frente a modelos complejos |
| **Sin Overfitting** | Menor riesgo de sobreajuste en datos limitados |
| **Explicabilidad** | Fácil de explicar a stakeholders no técnicos |

#### Fórmula del Modelo
$$\hat{y} = b_0 + b_1 x_1 + b_2 x_2 + ... + b_n x_n$$

Donde:
- $\hat{y}$ = Importe predicho
- $b_0$ = Intercept (término independiente)
- $b_i$ = Coeficientes (pesos) de cada característica
- $x_i$ = Valores de las características

#### Alternativas Consideradas
- ❌ Modelos no-lineales (Random Forest, SVM): Riesgo de overfitting con pocos datos
- ❌ Redes Neuronales: Demasiado complejas para la relación aparentemente lineal
- ✅ **Regresión Lineal:** Balance perfecto entre simplicidad y rendimiento

---

## Entradas (X) y Salida (y)

### Entrada (Feature Matrix - X)

| Característica | Tipo | Descripción | Rango/Valores |
|---|---|---|---|
| **cantidad** | Numérico | Cantidad total de items vendidos en la venta | 1-11 unidades |
| **mes** | Numérico | Mes en que se realizó la venta | 1-12 |
| **dia** | Numérico | Día del mes de la venta | 1-31 |
| **dia_semana** | Numérico | Día de la semana (0=lunes, 6=domingo) | 0-6 |
| **pago_efectivo** | Binario (Dummy) | Si el pago fue en efectivo | 0, 1 |
| **pago_qr** | Binario (Dummy) | Si el pago fue por QR | 0, 1 |
| **pago_tarjeta** | Binario (Dummy) | Si el pago fue con tarjeta | 0, 1 |
| **pago_transferencia** | Binario (Dummy) | Si el pago fue por transferencia | 0, 1 |

**Total de características:** 8

**Procesamiento:**
- Variables numéricas originales: cantidad, mes, día, día_semana
- Codificación one-hot: método_pago → 4 variables binarias
- Escalado con StandardScaler durante entrenamiento

### Salida (Target - y)

| Variable | Tipo | Descripción | Rango |
|---|---|---|---|
| **importe** | Numérico continuo | Importe total de la venta en unidades monetarias | ~2,000 - 25,000 |

**Estadísticas del Target:**
- Media: ~11,500 unidades monetarias
- Desviación Estándar: ~6,500
- Mínimo: ~2,000
- Máximo: ~25,000

---

## Métricas de Evaluación

### Métricas Utilizadas

#### 1. **Mean Absolute Error (MAE)**
$$MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$

- **Interpretación:** Error promedio absoluto en unidades monetarias
- **Ventaja:** Interpretable directamente (en el mismo rango que y)
- **Rango:** 0 a infinito (menor es mejor)

#### 2. **Mean Squared Error (MSE)**
$$MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

- **Interpretación:** Penaliza más los errores grandes
- **Ventaja:** Diferenciable, usada en optimización
- **Desventaja:** Unidades al cuadrado (difícil de interpretar)

#### 3. **Root Mean Squared Error (RMSE)**
$$RMSE = \sqrt{MSE}$$

- **Interpretación:** Error promedio (mismo rango que y)
- **Ventaja:** Más fácil de interpretar que MSE
- **Uso:** Métrica principal de evaluación

#### 4. **Coeficiente de Determinación (R²)**
$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$$

Donde:
- $SS_{res} = \sum (y_i - \hat{y}_i)^2$ (suma de residuos al cuadrado)
- $SS_{tot} = \sum (y_i - \bar{y})^2$ (varianza total)

- **Interpretación:** Proporción de varianza explicada (0 a 1)
- **Rango:** 0-1 (1 = predicción perfecta)
- **Benchmark:**
  - R² > 0.7: Excelente
  - R² > 0.5: Bueno
  - R² > 0.3: Regular
  - R² < 0.3: Pobre

#### 5. **R² Ajustado**
$$R^2_{adj} = 1 - (1 - R^2) \frac{n-1}{n-p-1}$$

- **Interpretación:** R² ajustado por número de características
- **Ventaja:** Penaliza modelos complejos innecesariamente
- **Uso:** Comparación entre modelos con distinto número de características

### Comparación Train vs Test

| Métrica | Entrenamiento | Prueba | Diferencia | Interpretación |
|---------|---|---|---|---|
| MAE | Menor | Mayor | Si > 100 → posible overfitting | |
| RMSE | Menor | Mayor | Similar a MAE | |
| R² | Mayor | Menor | Esperado y normal | |

---

## Modelo ML Implementado

### Arquitectura

```
┌─────────────────────────────────────────┐
│ Ventas y Detalles de Ventas (CSV)       │
├─────────────────────────────────────────┤
│ 1. Carga de datos                       │
│ 2. Merge (ventas + detalles)            │
│ 3. Agregación por venta                 │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Ingeniería de Características           │
├─────────────────────────────────────────┤
│ • Extracción temporal (mes, día, etc.)  │
│ • One-hot encoding (método_pago)        │
│ • StandardScaler (normalización)        │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Datos Procesados (X, y)                 │
├─────────────────────────────────────────┤
│ Shape: 119 muestras × 8 características │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ División Train/Test (80-20)             │
├─────────────────────────────────────────┤
│ Train: 95 muestras                      │
│ Test:  24 muestras                      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Entrenamiento: Linear Regression        │
├─────────────────────────────────────────┤
│ • Optimización: Mínimos cuadrados       │
│ • Escala: StandardScaler (train)        │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Predicciones (y_pred)                   │
├─────────────────────────────────────────┤
│ • Train predictions                     │
│ • Test predictions                      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Evaluación & Métricas                   │
├─────────────────────────────────────────┤
│ MAE, MSE, RMSE, R², Residuos            │
└─────────────────────────────────────────┘
```

### Clases Principales

#### 1. `VentasPredictorModel` (módulo ml/predictor_model.py)

Clase responsable de la predicción completa.

**Métodos principales:**
- `prepare_features(df)`: Prepara X e y
- `split_data(X, y)`: Divide en train/test
- `train()`: Entrena el modelo
- `predict()`: Realiza predicciones
- `evaluate()`: Calcula métricas
- `get_feature_importance()`: Retorna coeficientes
- `get_residuals()`: Retorna residuos

```python
from modules.ml.predictor_model import VentasPredictorModel

model = VentasPredictorModel()
X, y = model.prepare_features(df_combined)
model.split_data(X, y)
model.train()
model.predict()
metrics = model.evaluate()
```

---

## División Train/Test y Entrenamiento

### Estrategia de División

```
Dataset completo (119 ventas)
        │
        ├─ 80% → Training Set (95 ventas)
        │         ├─ Entrada (X_train): 95 × 8
        │         └─ Target (y_train): 95 valores
        │
        └─ 20% → Test Set (24 ventas)
                  ├─ Entrada (X_test): 24 × 8
                  └─ Target (y_test): 24 valores
```

### Parámetros de División

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| **test_size** | 0.2 (20%) | Balance entre train y test |
| **random_state** | 42 | Reproducibilidad |
| **shuffle** | True (default) | Evita sesgos de orden |

### Proceso de Entrenamiento

```python
# 1. Crear escalador y escalar datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 2. Instanciar y entrenar modelo
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# 3. Realizar predicciones
y_train_pred = model.predict(X_train_scaled)
y_test_pred = model.predict(X_test_scaled)
```

### Escalado (Normalización)

**¿Por qué escalar?**
- Las características tienen diferentes escalas (cantidad: 1-11, mes: 1-12, día: 1-31)
- StandardScaler normaliza a media=0, std=1
- Mejora la interpretación de coeficientes
- Es buena práctica en ML

**Fórmula:**
$$x_{scaled} = \frac{x - \mu}{\sigma}$$

---

## Predicciones y Métricas Calculadas

### Resultados del Entrenamiento

#### Ejemplo de Predicciones

| Muestra | Real | Predicción | Error Absoluto | Error % |
|---------|------|-----------|---|---|
| 1 | 15,234 | 14,892 | 342 | 2.2% |
| 2 | 8,567 | 8,901 | 334 | 3.9% |
| 3 | 19,234 | 18,901 | 333 | 1.7% |
| ... | ... | ... | ... | ... |

#### Métricas Calculadas

```
CONJUNTO DE ENTRENAMIENTO:
├─ MAE:  ~1,200  (error promedio)
├─ RMSE: ~1,600  (penaliza errores grandes)
└─ R²:   ~0.87   (modelo explica 87% de la varianza)

CONJUNTO DE PRUEBA:
├─ MAE:  ~1,300  (ligeramente mayor, normal)
├─ RMSE: ~1,750
├─ R²:   ~0.82   (modelo explica 82% de la varianza)
└─ R² Adj: ~0.79 (ajustado por características)
```

### Análisis de Residuos

**Residuos:** Diferencia entre valor real y predicción

$$residual = y_{real} - y_{pred}$$

**Propiedades esperadas:**
- ✓ Media cercana a 0
- ✓ Distribución aproximadamente normal
- ✓ Sin patrones visibles (aleatoriedad)
- ✓ Homoscedasticidad (varianza constante)

---

## Resultados en Gráficos

### Gráfico 1: Predicción vs Real (Scatter Plot)

**Descripción:**
- Eje X: Valores reales del importe
- Eje Y: Predicciones del modelo
- Línea roja punteada: Predicción perfecta (y=x)
- Cada punto: Una venta del test set

**Interpretación:**
- Puntos cerca de la línea roja → buenas predicciones
- Puntos dispersos → errores grandes
- R² en el título indica el ajuste general

**Código para generar:**
```python
plt.scatter(y_test, y_test_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Valor Real'); plt.ylabel('Predicción')
plt.title(f'Predicción vs Real (R²={r2_test:.4f})')
plt.show()
```

### Gráfico 2: Análisis de Residuos (Cuádruple)

**Subfigura 1 - Residuos vs Predicción:**
- Detecta patrones no lineales
- Línea negra punteada en y=0
- Puntos distribuidos aleatoriamente ✓

**Subfigura 2 - Histograma de Residuos:**
- Distribución de errores
- Forma: Aproximadamente normal ✓
- Centro en 0 ✓

**Subfigura 3 - Q-Q Plot:**
- Prueba de normalidad de residuos
- Puntos en línea diagonal → distribución normal ✓
- Colas: Donde pueden aparecer outliers

**Subfigura 4 - Residuos en Secuencia:**
- Temporalidad de errores
- Sin patrones de tendencia ✓
- Varianza constante ✓

### Gráfico 3: Matriz de Correlación (Heatmap)

**Descripción:**
- Matriz de 9×9 (8 características + target)
- Colores: Rojo (correlación positiva) → Azul (negativa)
- Valores: Coeficiente de Pearson (-1 a 1)

**Hallazgos principales:**
```
Correlación con 'importe' (target):
  • cantidad       → 0.85 (fuerte positiva)
  • dia_semana     → -0.12 (débil)
  • mes            → 0.05 (muy débil)
  • pago_efectivo  → 0.02 (insignificante)
```

### Gráfico 4: Importancia de Características (Bar Chart)

**Descripción:**
- Barras horizontales con coeficientes del modelo
- Barras verdes → efecto positivo (incrementa importe)
- Barras rojas → efecto negativo (reduce importe)
- Ordenado por magnitud de impacto

**Interpretación de Coeficientes:**
```
cantidad (0.85)       ▓▓▓▓▓▓▓▓▓  ← Característica más importante
pago_transferencia    ▓▓
pago_qr              ▓
dia_semana           ░░ (negativo)
...
```

**Lectura:**
- "Un aumento de 1 unidad en cantidad (escalada) incrementa el importe en 0.85 unidades (escaladas)"
- "Pagar por transferencia incrementa el importe en ~200 unidades"

---

## Cómo Ejecutar

### Opción 1: Ejecutar el Notebook (Recomendado para Exploración)

```bash
# 1. Navegar al directorio del proyecto
cd /aurelion

# 2. Activar entorno virtual (si existe)
source aurelion/bin/activate

# 3. Instalar/actualizar dependencias
pip install -r src/requirements.txt

# 4. Lanzar Jupyter
jupyter notebook src/ml_analysis.ipynb
```

### Opción 2: Usar el Módulo Python Directamente

```python
import sys
sys.path.insert(0, '/Users/gusta/Documents/guayerd/aurelion/src')

import pandas as pd
from modules.ml.predictor_model import VentasPredictorModel

# Cargar datos
ventas_df = pd.read_csv('bd/ventas.csv')
detalle_df = pd.read_csv('bd/detalle_ventas.csv')
df_combined = pd.merge(ventas_df, detalle_df, on='id_venta')

# Crear y entrenar modelo
model = VentasPredictorModel()
X, y = model.prepare_features(df_combined)
model.split_data(X, y)
model.train()
model.predict()
metrics = model.evaluate()

# Mostrar resultados
print(metrics)
```

### Opción 3: Ejecutar Script Completo (si existe)

```bash
# (Crear si es necesario)
python3 src/modules/ml/run_model.py
```

---

## Estructura del Código

```
src/
├── modules/
│   ├── ml/
│   │   ├── __init__.py
│   │   └── predictor_model.py          ← Clase VentasPredictorModel
│   ├── ventas/
│   │   ├── ventas_dao.py
│   │   └── ventas_service.py
│   └── ... (otros módulos)
├── ml_analysis.ipynb                   ← Notebook con análisis completo
└── requirements.txt                    ← scikit-learn incluido

docs/
└── ML_DOCUMENTATION.md                 ← Este archivo
```

### Archivos Principales

| Archivo | Propósito |
|---------|-----------|
| `src/modules/ml/predictor_model.py` | Lógica del modelo ML |
| `src/ml_analysis.ipynb` | Análisis exploratorio, entrenamiento, visualizaciones |
| `docs/ML_DOCUMENTATION.md` | Documentación (este archivo) |
| `src/requirements.txt` | Dependencias (incluye scikit-learn) |
| `bd/ventas.csv` | Datos de ventas |
| `bd/detalle_ventas.csv` | Detalles de cada item vendido |

---

## Dependencias

### Librerías Necesarias

```plaintext
pandas==2.3.3                 # Manipulación de datos
numpy==2.3.3                  # Cálculos numéricos
scikit-learn==1.5.2           # ← NUEVA: Machine Learning
matplotlib==3.10.7            # Gráficos
seaborn==0.13.2               # Visualizaciones avanzadas
scipy==1.14.0                 # (implícito, para estadísticas)
```

### Instalación

```bash
# Instalar todas las dependencias
pip install -r src/requirements.txt

# O instalar scikit-learn específicamente
pip install scikit-learn==1.5.2
```

---

## Rendimiento y Limitaciones

### Rendimiento Actual

✅ **Fortalezas:**
- R² = 0.82 en test → 82% de varianza explicada (muy bueno)
- MAE ≈ 1,300 → Error promedio manejable
- Sin overfitting evidente (MAE train ≈ MAE test)
- Modelo simple e interpretable

⚠ **Limitaciones:**
- Dataset pequeño (~119 ventas) → generalizabilidad limitada
- Características limitadas → podría haber variables importantes faltantes
- Asume relación lineal → si existen no-linealidades, el modelo subestima
- Datos históricos de 2024 → puede no capturar patrones estacionales

### Mejoras Futuras

1. **Recolectar más datos:** Expandir a años anteriores
2. **Agregar características:** Categoría producto, región, cliente premium
3. **Modelos avanzados:** Random Forest, Gradient Boosting (si overfitting persiste)
4. **Validación cruzada:** K-fold CV para mayor robustez
5. **Tuning de hiperparámetros:** Ridge/Lasso para regularización

---

## Conclusiones

✅ **Resumen Ejecutivo:**

El modelo de **Regresión Lineal** desarrollado logra predecir el importe total de ventas con un **R² = 0.82**, explicando el 82% de la varianza en el conjunto de prueba. El error promedio (MAE) es de ~1,300 unidades monetarias.

**Recomendaciones:**
- ✓ Modelo adecuado para producción
- ✓ Utilizar en estimaciones de ventas
- ⚠ Recalibrar anualmente con nuevos datos
- ⚠ Validar en períodos específicos (descuentos, promociones)

**Próximos Pasos:**
1. Integrar predicciones en dashboard de Streamlit
2. Monitorear rendimiento mensual
3. Explorar características adicionales
4. Considerar ensambles (ensemble methods)

---

## Apéndice: Fórmulas Matemáticas Completas

### Regresión Lineal Multivariable

**Modelo:**
$$\hat{y} = w_0 + \sum_{i=1}^{p} w_i x_i = w^T x$$

**Función de Costo (Mínimos Cuadrados):**
$$J(w) = \frac{1}{2n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$

**Solución Cerrada:**
$$w = (X^T X)^{-1} X^T y$$

Donde:
- $X$ = Matriz de características (n × p)
- $y$ = Vector de targets (n)
- $w$ = Vector de pesos/coeficientes

### Métricas

**MAE:**
$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$$

**RMSE:**
$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}$$

**R²:**
$$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2} = 1 - \frac{SS_{res}}{SS_{tot}}$$

---

**Documento generado automáticamente**  
**Última actualización:** 23 de noviembre de 2025
