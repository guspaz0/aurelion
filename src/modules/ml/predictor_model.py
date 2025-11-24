"""
Modelo de Machine Learning para predecir el importe total de ventas.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


class VentasPredictorModel:
    """
    Modelo de regresión lineal para predecir el importe total de una venta
    basándose en características como cantidad de ítems, mes, día, medio de pago.
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_trained = False
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.predictions_train = None
        self.predictions_test = None
        self.metrics = {}
    
    def prepare_features(self, df: 'pd.DataFrame'):
        """
        Prepara las características (X) y el objetivo (y) a partir del dataframe.
        
        Parámetros:
        -----------
        df : pandas.DataFrame
            DataFrame con las ventas y detalles de ventas combinados.
            Debe incluir: id_venta, cantidad, fecha, medio_pago, importe
        
        Retorna:
        --------
        X : pandas.DataFrame
            Matriz de características
        y : pandas.Series
            Serie de valores objetivo (importe total)
        """
        # Agrupar por venta para obtener cantidad total de ítems e importe total
        ventas_agregadas = df.groupby('id_venta').agg({
            'cantidad': 'sum',
            'importe': 'sum',
            'fecha': 'first',
            'medio_pago': 'first'
        }).reset_index()
        
        # Extraer características temporales
        ventas_agregadas['fecha'] = pd.to_datetime(ventas_agregadas['fecha'])
        ventas_agregadas['mes'] = ventas_agregadas['fecha'].dt.month
        ventas_agregadas['dia_semana'] = ventas_agregadas['fecha'].dt.dayofweek
        ventas_agregadas['dia'] = ventas_agregadas['fecha'].dt.day
        
        # Codificar medio_pago como variables dummy
        medio_pago_encoded = pd.get_dummies(ventas_agregadas['medio_pago'], 
                                             prefix='pago')
        
        # Construir la matriz X
        X = pd.DataFrame({
            'cantidad': ventas_agregadas['cantidad'],
            'mes': ventas_agregadas['mes'],
            'dia': ventas_agregadas['dia'],
            'dia_semana': ventas_agregadas['dia_semana']
        })
        
        # Combinar con las variables de medio de pago
        X = pd.concat([X, medio_pago_encoded], axis=1)
        
        # El objetivo es el importe total
        y = ventas_agregadas['importe']
        
        self.feature_names = X.columns.tolist()
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Divide los datos en conjuntos de entrenamiento y prueba.
        
        Parámetros:
        -----------
        X : pandas.DataFrame
            Matriz de características
        y : pandas.Series
            Serie de valores objetivo
        test_size : float, default=0.2
            Proporción del conjunto de prueba
        random_state : int, default=42
            Semilla para reproducibilidad
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
    
    def train(self):
        """
        Entrena el modelo de regresión lineal.
        """
        if self.X_train is None:
            raise ValueError("Datos de entrenamiento no preparados. Ejecute split_data() primero.")
        
        # Escalar las características
        X_train_scaled = self.scaler.fit_transform(self.X_train)
        
        # Entrenar el modelo
        self.model.fit(X_train_scaled, self.y_train)
        self.is_trained = True
    
    def predict(self):
        """
        Realiza predicciones en los conjuntos de entrenamiento y prueba.
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado. Ejecute train() primero.")
        
        X_train_scaled = self.scaler.transform(self.X_train)
        X_test_scaled = self.scaler.transform(self.X_test)
        
        self.predictions_train = self.model.predict(X_train_scaled)
        self.predictions_test = self.model.predict(X_test_scaled)
    
    def evaluate(self):
        """
        Calcula métricas de evaluación del modelo.
        
        Retorna:
        --------
        dict
            Diccionario con las métricas calculadas (MAE, MSE, RMSE, R², R² ajustado)
        """
        if self.predictions_train is None or self.predictions_test is None:
            raise ValueError("Predicciones no realizadas. Ejecute predict() primero.")
        
        # Calcular métricas en entrenamiento
        mae_train = mean_absolute_error(self.y_train, self.predictions_train)
        mse_train = mean_squared_error(self.y_train, self.predictions_train)
        rmse_train = np.sqrt(mse_train)
        r2_train = r2_score(self.y_train, self.predictions_train)
        
        # Calcular métricas en prueba
        mae_test = mean_absolute_error(self.y_test, self.predictions_test)
        mse_test = mean_squared_error(self.y_test, self.predictions_test)
        rmse_test = np.sqrt(mse_test)
        r2_test = r2_score(self.y_test, self.predictions_test)
        
        # R² ajustado para el conjunto de prueba
        n_samples = len(self.y_test)
        n_features = self.X_test.shape[1]
        r2_adj_test = 1 - (1 - r2_test) * (n_samples - 1) / (n_samples - n_features - 1)
        
        self.metrics = {
            'entrenamiento': {
                'MAE': mae_train,
                'MSE': mse_train,
                'RMSE': rmse_train,
                'R2': r2_train
            },
            'prueba': {
                'MAE': mae_test,
                'MSE': mse_test,
                'RMSE': rmse_test,
                'R2': r2_test,
                'R2_ajustado': r2_adj_test
            }
        }
        
        return self.metrics
    
    def get_feature_importance(self):
        """
        Retorna los coeficientes del modelo (importancia de características).
        """
        if not self.is_trained:
            raise ValueError("El modelo no ha sido entrenado.")
        
        feature_importance = pd.DataFrame({
            'caracteristica': self.feature_names,
            'coeficiente': self.model.coef_
        }).sort_values('coeficiente', key=abs, ascending=False)
        
        return feature_importance
    
    def get_residuals(self):
        """
        Calcula los residuos del modelo.
        """
        residuals_train = self.y_train - self.predictions_train
        residuals_test = self.y_test - self.predictions_test
        
        return {
            'entrenamiento': residuals_train,
            'prueba': residuals_test
        }
