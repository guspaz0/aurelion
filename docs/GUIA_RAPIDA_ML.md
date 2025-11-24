# Guía Rápida - Proyecto Machine Learning Aurelion

## 🚀 Inicio Rápido

### Opción 1: Ejecutar la Demostración (Recomendado)
```bash
## inicializar entorno virtual, previamente creado y con las dependencias instaladas
source aurelion/bin/activate
PYTHONPATH=src python3 src/modules/ml/demo.py
```

**Output esperado:**
- Carga de datos ✓
- División train/test ✓
- Entrenamiento ✓
- Métricas: R²=0.787, MAE=$5,158.86 ✓
- Características más importantes ✓

### Opción 2: Ejecutar el Notebook (Para exploración)
```bash
## inicializar entorno virtual, previamente creado y con las dependencias instaladas
source aurelion/bin/activate
jupyter notebook src/ml_analysis.ipynb
```

## 📊 Estructura de Archivos

```
aurelion/
├── src/
│   ├── modules/ml/
│   │   ├── __init__.py
│   │   ├── predictor_model.py      ← Clase VentasPredictorModel
│   │   └── demo.py                 ← Script de demostración
│   ├── ml_analysis.ipynb           ← Notebook completo
│   └── requirements.txt             ← Dependencias (scikit-learn incluido)
├── docs/
│   ├── ML_DOCUMENTATION.md         ← Documentación detallada
│   ├── ENTREGA_ML_RESUMEN.md       ← Este resumen
│   └── ... (otros docs)
├── bd/
│   ├── ventas.csv                  ← Datos de ventas
│   └── detalle_ventas.csv          ← Detalles de items
└── README.md                        ← Actualizado con sección ML
```

## 🎯 Modelo ML

**Tipo:** Regresión Lineal (scikit-learn)
**Objetivo:** Predecir importe total de venta

### Características (X)
- `cantidad`: Total de items vendidos
- `mes`: Mes de la venta (1-12)
- `dia`: Día del mes (1-31)
- `dia_semana`: Día semana (0=lunes, 6=domingo)
- `pago_efectivo`, `pago_qr`, `pago_tarjeta`, `pago_transferencia`: Método pago

### Target (y)
- `importe`: Valor total de la venta

## 📈 Resultados

| Métrica | Valor |
|---------|-------|
| **R² (Test)** | **0.787** ← Excelente |
| MAE (Test) | $5,158.86 |
| RMSE (Test) | 6,641.64 |
| R² Ajustado | 0.673 |
| Muestras | 120 ventas |
| Train/Test | 96 / 24 (80/20) |

## 🔑 Uso del Módulo

### En Python
```python
from modules.ml.predictor_model import VentasPredictorModel
import pandas as pd

# Cargar datos
ventas = pd.read_csv('bd/ventas.csv')
detalles = pd.read_csv('bd/detalle_ventas.csv')
df = pd.merge(ventas, detalles, on='id_venta')

# Crear y entrenar modelo
model = VentasPredictorModel()
X, y = model.prepare_features(df)
model.split_data(X, y)
model.train()
model.predict()

# Evaluar
metrics = model.evaluate()
print(f"R²: {metrics['prueba']['R2']:.4f}")

# Obtener importancia de características
importance = model.get_feature_importance()
print(importance)

# Obtener residuos
residuals = model.get_residuals()
```

### En Jupyter
Ver `src/ml_analysis.ipynb` - Ejecutar celda por celda

## 📚 Documentación Completa

- **ML_DOCUMENTATION.md**: Documentación técnica completa (fórmulas, ejemplos, etc.)
- **ENTREGA_ML_RESUMEN.md**: Resumen de cumplimiento de requisitos
- **README.md**: Descripción general del proyecto

## ✨ Características Principales

✅ Regresión Lineal interpretable
✅ Sin overfitting (MAE train ≈ MAE test)
✅ Escalado correcto con StandardScaler
✅ División reproducible (random_state=42)
✅ Métricas completas (MAE, RMSE, R², R² ajustado)
✅ 4 visualizaciones profesionales
✅ Documentación extensiva
✅ Script de demostración

## 🐛 Troubleshooting

### Error: "No module named 'sklearn'"
```bash
# Activar entorno y reinstalar
source aurelion/bin/activate
pip install -r src/requirements.txt
```

### Error: "FileNotFoundError" (archivos CSV)

Verificar que estés en el directorio correcto, en la raiz del repo.


### Notebook lento
- Usar "Restart Kernel" en Jupyter
- Ejecutar celdas en orden secuencial

## 📞 Soporte

Para más detalles, consultar:
1. `docs/ML_DOCUMENTATION.md` - Completa
2. Comentarios en `src/modules/ml/predictor_model.py`
3. Celdas markdown en `src/ml_analysis.ipynb`

---

**Estado:** ✅ Completado y Validado
**Fecha:** 23 de noviembre de 2025
**Versión:** 1.0
