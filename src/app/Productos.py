from datetime import datetime,date
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from app_state import app
import logging
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Productos",
    page_icon=":shopping_cart:",
    layout="wide"
)

def get_top_products(desde: date | datetime, hasta: date | datetime):
    return app.productos_service.mas_vendidos(desde,hasta)

def top_productos():
    logger.info("refresco")

    st.title("Productos")

    with st.sidebar:
        st.subheader("filtros de ventas")

        f_desde = st.date_input("Fecha desde", value=datetime.strptime('2024-01-01',"%Y-%m-%d"), format="YYYY-MM-DD")
        f_hasta = st.date_input("Fecha hasta", value=datetime.strptime('2024-06-30',"%Y-%m-%d"), format="YYYY-MM-DD")

    st.write(f"Total Productos vendidos desde {f_desde.strftime('%Y-%m-%d')} - {f_hasta.strftime('%Y-%m-%d')}")

    top_products = get_top_products(f_desde,f_hasta)

    df = pd.DataFrame(
        data=[producto.values() for producto in top_products],
        columns=top_products[0].keys()
    )

    grafico, tabla = st.tabs(["Gráfico", "Tabla"])

    with grafico:

        category_totals = df.groupby('categoria')['importe'].sum()

        fig1, ax1 = plt.subplots()

        wedges, texts, autotexts = ax1.pie(
            category_totals,
            autopct='%1.1f%%', 
            startangle=90, 
            textprops={'fontsize': 12}
        )
        for i, (wedge, text, autotext) in enumerate(zip(wedges, texts, autotexts)):
            category = category_totals.index[i]
            text.set_text(f'{category} ${category_totals[i]:,.2f}')
            text.set_fontsize(10)

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Display the pie chart in Streamlit
        st.pyplot(fig1)

    with tabla:
        df = df.rename(columns={'id_producto': 'id'})
        st.dataframe(df, hide_index=True)

if __name__ == "__main__":
    top_productos()