#!/usr/bin/env python3
"""
Script de demostración del modelo ML de Aurelion (versión con VentasService)
Predicción de importe total de ventas usando Regresión Lineal
Datos obtenidos directamente desde la base de datos a través del servicio VentasService
"""

import sys
import pathlib

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))

import pandas as pd
import numpy as np
from predictor_model import VentasPredictorModel
from modules.db.db_connection import DbConnection
from modules.ventas.ventas_service import VentasService


def convert_venta_models_to_dataframe(ventas_list, detalle_ventas_list):
    """
    Convierte la lista de VentaModel y DetalleVentaModel a un DataFrame de Pandas.
    
    :param ventas_list: Lista de VentaModel obtenida de VentasService
    :param detalle_ventas_list: Lista de DetalleVentaModel obtenida de la base de datos
    :return: DataFrame combinado con todos los detalles de ventas
    """
    # Convertir ventas a lista de diccionarios
    ventas_data = []
    for venta in ventas_list:
        ventas_data.append({
            'id_venta': venta.id_venta,
            'id_cliente': venta.id_cliente,
            'nombre_cliente': venta.nombre_cliente,
            'email': venta.email,
            'medio_pago': venta.medio_pago,
            'ciudad': venta.ciudad,
            'fecha': venta.fecha,
            'importe': venta.importe
        })
    
    # Convertir detalles de venta a lista de diccionarios
    detalles_data = []
    for detalle in detalle_ventas_list:
        detalles_data.append({
            'id_venta': detalle.id_venta,
            'id_producto': detalle.id_producto,
            'nombre_producto': detalle.nombre_producto,
            'cantidad': detalle.cantidad,
            'precio_unitario': detalle.precio_unitario,
            'importe': detalle.importe
        })
    
    # Crear DataFrames
    ventas_df = pd.DataFrame(ventas_data)
    detalles_df = pd.DataFrame(detalles_data)
    
    # Combinar por id_venta
    df_combined = pd.merge(ventas_df, detalles_df, on='id_venta', how='inner')
    
    return df_combined, ventas_df, detalles_df


def main():
    print("\n" + "="*80)
    print("DEMOSTRACIÓN - MODELO ML AURELION (Usando VentasService)")
    print("Predicción de Importe Total de Ventas - Datos desde Base de Datos")
    print("="*80)
    
    # 1. Conectar a la base de datos e inicializar servicios
    print("\n🔗 Conectando a la base de datos...")
    try:
        db_connection = DbConnection()
        ventas_service = VentasService(db_connection)
        print("   ✓ Conexión establecida")
    except Exception as e:
        print(f"   ✗ Error al conectar: {e}")
        return
    
    # 2. Cargar datos desde VentasService
    print("\n📥 Cargando datos desde VentasService...")
    try:
        ventas_list = ventas_service.get_all()
        detalles_list = get_all_detalle_ventas(db_connection)
        print(f"   ✓ {len(ventas_list)} ventas cargadas")
        print(f"   ✓ {len(detalles_list)} detalles de venta cargados")
    except Exception as e:
        print(f"   ✗ Error al cargar datos: {e}")
        db_connection.close()
        return
    
    # 3. Convertir a DataFrame
    print("\n📊 Preparando datos...")
    try:
        df_combined, ventas_df, detalles_df = convert_venta_models_to_dataframe(
            ventas_list, detalles_list
        )
        print(f"   ✓ {len(df_combined)} registros combinados")
        print(f"   ✓ Columnas: {', '.join(df_combined.columns.tolist())}")
    except Exception as e:
        print(f"   ✗ Error al preparar datos: {e}")
        db_connection.close()
        return
    
    # 4. Preparar modelo
    print("\n🔧 Preparando modelo...")
    try:
        model = VentasPredictorModel()
        X, y = model.prepare_features(df_combined)
        print(f"   ✓ Características: {X.shape[1]}")
        print(f"   ✓ Muestras: {X.shape[0]} ventas")
    except Exception as e:
        print(f"   ✗ Error al preparar modelo: {e}")
        db_connection.close()
        return
    
    # 5. Dividir datos
    print("\n📊 Dividiendo en train/test...")
    try:
        model.split_data(X, y, test_size=0.2, random_state=42)
        print(f"   ✓ Train: {len(model.X_train)} muestras")
        print(f"   ✓ Test:  {len(model.X_test)} muestras")
    except Exception as e:
        print(f"   ✗ Error al dividir datos: {e}")
        db_connection.close()
        return
    
    # 6. Entrenar
    print("\n🎓 Entrenando modelo...")
    try:
        model.train()
        print(f"   ✓ Modelo entrenado")
        print(f"   ✓ Intercept: {model.model.intercept_:.2f}")
    except Exception as e:
        print(f"   ✗ Error al entrenar: {e}")
        db_connection.close()
        return
    
    # 7. Predecir
    print("\n🔮 Generando predicciones...")
    try:
        model.predict()
        print(f"   ✓ Predicciones realizadas en train y test")
    except Exception as e:
        print(f"   ✗ Error al predecir: {e}")
        db_connection.close()
        return
    
    # 8. Evaluar
    print("\n📈 Calculando métricas...")
    try:
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
    except Exception as e:
        print(f"   ✗ Error al evaluar: {e}")
        db_connection.close()
        return
    
    # 9. Mostrar importancia de características
    print("\n🔑 Características Más Importantes:")
    try:
        feature_importance = model.get_feature_importance()
        print(feature_importance.head(5).to_string(index=False))
    except Exception as e:
        print(f"   ✗ Error al obtener importancia: {e}")
    
    # 10. Ejemplos de predicción
    print("\n💡 Ejemplos de Predicción (primeros 5 del conjunto de prueba):")
    try:
        print(f"\n   {'Índice':<8} {'Real':<12} {'Predicción':<15} {'Error':<10} {'Error %':<8}")
        print("   " + "-" * 55)
        
        for i in range(min(5, len(model.y_test))):
            real = model.y_test.iloc[i]
            pred = model.predictions_test[i]
            error = abs(real - pred)
            error_pct = (error / real * 100) if real != 0 else 0
            print(f"   {i+1:<8} {real:<12.0f} {pred:<15.2f} {error:<10.2f} {error_pct:<8.1f}%")
    except Exception as e:
        print(f"   ✗ Error al mostrar ejemplos: {e}")
    
    # 11. Información de las ventas por ciudad
    print("\n🌍 Resumen de Ventas por Ciudad:")
    try:
        ventas_ciudad = ventas_service.get_ventas_por_ciudad()
        print(f"\n   {'Ciudad':<20} {'Departamento':<20} {'Importe':<15}")
        print("   " + "-" * 55)
        for ciudad in ventas_ciudad[:5]:  # Top 5 ciudades
            print(f"   {ciudad['ciudad']:<20} {ciudad['departamento']:<20} ${ciudad['importe']:<14.2f}")
    except Exception as e:
        print(f"   ✗ Error al obtener ventas por ciudad: {e}")
    
    # 12. Conclusión
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
    
    # Cerrar conexión
    db_connection.close()
    print("   ✓ Conexión a base de datos cerrada")


if __name__ == '__main__':
    main()
