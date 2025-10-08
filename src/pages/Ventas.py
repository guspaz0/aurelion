from datetime import datetime, date
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from index import app
import logging
logger = logging.getLogger(__name__)


st.set_page_config(
    page_title="Ventas",
    page_icon=":person:",
    layout="wide"
)

def get_ventas(desde: date, hasta: date):
    return app.ventas_service.get_all(desde,hasta)

def ventas():
    logger.info("refresco")
    st.title("Ventas")

    with st.sidebar:
        st.subheader("filtros de ventas")

        f_desde = st.date_input("Fecha desde", value=datetime.strptime('2024-01-01',"%Y-%m-%d"), format="YYYY-MM-DD")
        f_hasta = st.date_input("Fecha hasta", value=datetime.strptime('2024-06-30',"%Y-%m-%d"), format="YYYY-MM-DD")

    st.write(f"Importe total vendido por mes {f_desde.strftime('%Y-%m-%d')} - {f_hasta.strftime('%Y-%m-%d')}")

    ventas = get_ventas(f_desde, f_hasta)

    df = pd.DataFrame(
        data=[venta.to_dict() for venta in ventas],
        columns=["importe", "fecha", 'medio_pago']
    )
    # Ensure 'fecha' is datetime and handle empty data
    df['fecha'] = pd.to_datetime(df['fecha'])
    if df.empty:
        st.info("No ventas found for the selected date range.")
        return

    # Group by month and payment method, filling missing values with 0
    df['month'] = df['fecha'].dt.to_period('M')
    grouped_df = df.groupby(['month', 'medio_pago'])['importe'].sum().unstack(fill_value=0)
    grouped_df = grouped_df.sort_index()

    fig, ax = plt.subplots()
    # bottom must be aligned with the x-axis (rows), not with the payment-method columns
    bottom = pd.Series(0.0, index=grouped_df.index)

    for i,medio_pago in enumerate(iter(grouped_df.columns)):
        values = grouped_df[medio_pago].fillna(0.0)
        ax.bar(grouped_df.index.astype(str), values, label=str(medio_pago), bottom=bottom)
        ax.bar_label(ax.containers[i], padding=0)
        # increment bottom by the values we just plotted (aligns by index)
        bottom = bottom.add(values, fill_value=0.0)

    ax.legend()
    ax.set_ylabel("Importe")
    ax.set_title("Ventas por mes y medio de pago")


    left, right = st.columns(2)

    with left:
        st.dataframe(grouped_df)
        st.write("")

    with right:
        st.pyplot(fig)
        #st.bar_chart(data=grouped_df.set_index('month')['importe'], y_label='importe')


if __name__ == "__main__":
    ventas()