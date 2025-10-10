from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app_state import app
import logging
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Clientes",
    page_icon=":person:",
    layout="wide"
)

ROWS: int = 10

def get_top_customers(desde, hasta):
    return app.clientes_service.total_ventas(desde,hasta)[:ROWS]

def top_clientes():

    logger.info("refresco")

    st.title("Clientes Top")

    st.subheader(f"Top {ROWS} clientes")

    with st.sidebar:
        st.subheader("filtros de ventas")

        f_desde = st.date_input("Fecha desde", value=datetime.strptime('2024-01-01',"%Y-%m-%d"), format="YYYY-MM-DD")
        f_hasta = st.date_input("Fecha hasta", value=datetime.strptime('2024-06-30',"%Y-%m-%d"), format="YYYY-MM-DD")

    st.write(f"Importe total vendido por clientes {f_desde.strftime('%Y-%m-%d')} - {f_hasta.strftime('%Y-%m-%d')}")

    top_customers = get_top_customers(f_desde,f_hasta)

    df = pd.DataFrame(
        data=[cliente.values() for cliente in top_customers],
        columns=top_customers[0].keys()
    )

    df.drop(columns=["email", "fecha_alta", "cantidad_ventas", "ciudad"], inplace=True)    

    # If there are no top customers, stop early
    if df.empty:
        st.info("No clientes found for the selected date range.")
        return

    grafico, tabla = st.tabs(["Gráfico", "Tabla"])

    with tabla:
        # Hide internal id before showing
        df = df.rename(columns={'id_cliente': 'id'})
        st.dataframe(df, hide_index=True)

    with grafico:
        # Create a stacked bar chart grouped by client
        payment_methods = ['efectivo', 'transferencia', 'tarjeta', 'qr']

        x = df['id'].astype(str)

        fig, ax = plt.subplots(figsize=(10, 6))

        bottom = pd.Series(0.0, index=df.index)

        for i,payment in enumerate(iter(payment_methods)):
            values = df[payment].fillna(0.0)
            # Matplotlib accepts an array-like 'bottom' of the same length as x
            ax.bar(x, values, label=str(payment), bottom=bottom.values)
            ax.bar_label(ax.containers[i], padding=0)
            bottom = bottom.add(values, fill_value=0.0)

        ax.legend()
        ax.set_title("Ventas por cliente y medio de pago")
        fig.tight_layout()
        st.pyplot(fig)


if __name__ == "__main__":
    top_clientes()