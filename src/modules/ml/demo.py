#!/usr/bin/env python3
"""
Script de demostración del modelo ML de Aurelion
Predicción de importe total de ventas usando Regresión Lineal
"""

import pathlib

path = pathlib.Path(__file__).parents[3] / 'bd'
VENTAS_CSV = path / 'ventas.csv'
DETALLE_VENTAS_CSV = path / 'detalle_ventas.csv'

import pandas as pd
import numpy as np
from predictor_model import VentasPredictorModel

def main():
    print("\n" + "="*80)
    print("DEMOSTRACIÓN - MODELO ML AURELION")
    print("Predicción de Importe Total de Ventas")
    print("="*80)
    
    # 1. Cargar datos
    print("\n📥 Cargando datos...")
    ventas_df = pd.read_csv(VENTAS_CSV)
    detalle_df = pd.read_csv(DETALLE_VENTAS_CSV)
    df_combined = pd.merge(ventas_df, detalle_df, on='id_venta', how='inner')
    print(f"   ✓ {len(df_combined)} registros de detalles de ventas cargados")
    
    # 2. Preparar modelo
    print("\n🔧 Preparando modelo...")
    model = VentasPredictorModel()
    X, y = model.prepare_features(df_combined)
    print(f"   ✓ Características: {X.shape[1]}")
    print(f"   ✓ Muestras: {X.shape[0]} ventas")
    
    # 3. Dividir datos
    print("\n📊 Dividiendo en train/test...")
    model.split_data(X, y, test_size=0.2, random_state=42)
    print(f"   ✓ Train: {len(model.X_train)} muestras")
    print(f"   ✓ Test:  {len(model.X_test)} muestras")
    
    # 4. Entrenar
    print("\n🎓 Entrenando modelo...")
    model.train()
    print(f"   ✓ Modelo entrenado")
    print(f"   ✓ Intercept: {model.model.intercept_:.2f}")
    
    # 5. Predecir
    print("\n🔮 Generando predicciones...")
    model.predict()
    print(f"   ✓ Predicciones realizadas en train y test")
    
    # 6. Evaluar
    print("\n📈 Calculando métricas...")
    metrics = model.evaluate()
    
    print("\n   RESULTADOS:")
    print(f"\n   ╔════════════════════════════════════════╗")
    print(f"   ║  ENTRENAMIENTO                         ║")
    print(f"   ╠════════════════════════════════════════╣")
    print(f"   ║ MAE:  {metrics['entrenamiento']['MAE']:>30.2f} ║")
    print(f"   ║ RMSE: {metrics['entrenamiento']['RMSE']:>30.2f} ║")
    print(f"   ║ R²:   {metrics['entrenamiento']['R2']:>30.4f} ║")
    print(f"   ╠════════════════════════════════════════╣")
    print(f"   ║  PRUEBA                                ║")
    print(f"   ╠════════════════════════════════════════╣")
    print(f"   ║ MAE:  {metrics['prueba']['MAE']:>30.2f} ║")
    print(f"   ║ RMSE: {metrics['prueba']['RMSE']:>30.2f} ║")
    print(f"   ║ R²:   {metrics['prueba']['R2']:>30.4f} ║")
    print(f"   ║ R² Adj: {metrics['prueba']['R2_ajustado']:>27.4f} ║")
    print(f"   ╚════════════════════════════════════════╝")
    
    # 7. Mostrar importancia de características
    print("\n🔑 Características Más Importantes:")
    feature_importance = model.get_feature_importance()
    print(feature_importance.head(5).to_string(index=False))
    
    # 8. Ejemplos de predicción
    print("\n💡 Ejemplos de Predicción:")
    print(f"\n   {'Índice':<8} {'Real':<12} {'Predicción':<15} {'Error':<10} {'Error %':<8}")
    print("   " + "-" * 55)
    
    for i in range(min(5, len(model.y_test))):
        real = model.y_test.iloc[i]
        pred = model.predictions_test[i]
        error = abs(real - pred)
        error_pct = (error / real * 100) if real != 0 else 0
        print(f"   {i+1:<8} {real:<12.0f} {pred:<15.2f} {error:<10.2f} {error_pct:<8.1f}%")
    
    # 9. Conclusión
    print("\n" + "="*80)
    print("✅ CONCLUSIÓN:")
    r2 = metrics['prueba']['R2']
    mae = metrics['prueba']['MAE']
    
    if r2 > 0.7:
        calidad = "EXCELENTE"
    elif r2 > 0.5:
        calidad = "BUENO"
    else:
        calidad = "REGULAR"
    
    print(f"   El modelo tiene un rendimiento {calidad}")
    print(f"   → R² = {r2:.4f} (explica {r2*100:.1f}% de la varianza)")
    print(f"   → Error promedio = ${mae:.2f}")
    print(f"   → Adecuado para: Estimaciones de ventas, detección de anomalías")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
