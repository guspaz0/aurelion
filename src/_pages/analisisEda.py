import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app_state import app

st.set_page_config(
    page_title="Analisis Eda",
    page_icon=":chart:",
    layout="wide"
)

def analisis_eda():

    st.markdown("## 1) Histograma de `precio_unitario` (productos). distribución de precios e importes")

    productos = [p.to_dict() for p in app.productos_service.get_all()]
    df_productos = pd.DataFrame(productos)

    ventas = [v.to_dict() for v in app.ventas_service.get_all()]
    df_ventas = pd.DataFrame(ventas)
    if not df_ventas.empty:
        df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'], errors='coerce')

    # Expandir detalle de ventas en un dataframe separado
    rows = []
    for v in ventas:
        for d in v.get('detalle', []):
            row = dict(d)
            row['id_venta'] = v.get('id_venta')
            row['fecha'] = v.get('fecha')
            rows.append(row)

    if rows:
        df_detalle = pd.DataFrame(rows)
    else:
        df_detalle = pd.DataFrame()
    
    # Asegurar tipos numéricos
    for col in ['cantidad','precio_unitario','importe']:
        if col in df_detalle.columns:
            df_detalle[col] = pd.to_numeric(df_detalle[col], errors='coerce')
    if 'precio_unitario' in df_productos.columns:
        df_productos['precio_unitario'] = pd.to_numeric(df_productos['precio_unitario'], errors='coerce')
    
    sns.set_style('whitegrid')
    histograma = plt.figure(figsize=(8,4))
    
    if 'precio_unitario' in df_productos.columns and not df_productos['precio_unitario'].dropna().empty:
        sns.histplot(df_productos['precio_unitario'].dropna(), bins=30, kde=True)
        plt.title('Distribución de precio_unitario (productos)')
        plt.xlabel('Precio unitario')
        plt.ylabel('Frecuencia')

    tab_histograma, tab_df_productos = st.tabs(["Gráfico", "Dataframe Head"])

    with tab_df_productos:
        df_productos_head = df_productos.rename(columns={'id_cliente': 'id'})
        st.dataframe(df_productos_head.head(), hide_index=True)

    with tab_histograma:
        st.pyplot(histograma)

    st.markdown("## 2) Boxplot de importes por `categoria`")

    if not df_detalle.empty and 'id_producto' in df_detalle.columns:
        df_detalle['id_producto'] = pd.to_numeric(df_detalle['id_producto'], errors='coerce')
        merged = df_detalle.merge(df_productos, left_on='id_producto', right_on='id_producto', how='left', suffixes=('_det','_prod'))
        # recalcular importe si no existe
        merged['importe_calc'] = merged['cantidad'] * merged['precio_unitario_det']
        merged['importe'] = merged['importe'].fillna(merged['importe_calc'])
        merged['categoria'] = merged.get('categoria', pd.Series(['SIN_CATEGORIA']*len(merged)))
        boxplot = plt.figure(figsize=(10,6))
        sns.boxplot(x='categoria', y='importe', data=merged)
        plt.xticks(rotation=45, ha='right')
        plt.title('Boxplot de importes por categoría')
        plt.tight_layout()
        plt.show()
    else:
        print('No hay detalle de ventas o id_producto para generar boxplot.')

    tab_boxplot, tab_df_detalle_ventas = st.tabs(["Gráfico", "Dataframe Head"])

    with tab_boxplot:
        st.pyplot(boxplot)

    with tab_df_detalle_ventas:
        st.dataframe(merged.head(), hide_index=True)

    st.markdown("## 3) Heatmap de correlaciones entre variables numéricas")

    if not df_detalle.empty:
        num = df_detalle[['cantidad','precio_unitario','importe']].copy()
        num = num.apply(pd.to_numeric, errors='coerce')
        corr = num.corr(method='pearson')
        heatmap = plt.figure(figsize=(6,4))
        sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Correlación entre cantidad, precio_unitario e importe')
        plt.show()
        st.pyplot(heatmap)
    else:
        print('No hay datos numéricos en detalle para calcular correlaciones.')

if __name__ == "__main__":
    st.title("Analisis Exploratorio ")
    analisis_eda()