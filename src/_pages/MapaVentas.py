from datetime import datetime
import streamlit as st
import folium
from streamlit_folium import st_folium
from app_state import app
import pandas as pd
import logging
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Ventas",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

def get_ventas_ciudades(desde: datetime | str = None, hasta: datetime | str = None):
    return app.ventas_service.get_ventas_por_ciudad(desde, hasta)

def mapa():
    logger.info("refresco")
    st.header("Mapa de Ventas")
    with st.sidebar:
        st.subheader("filtros de ventas")

        f_desde = st.date_input("Fecha desde", value=datetime.strptime('2024-01-01',"%Y-%m-%d"), format="YYYY-MM-DD")
        f_hasta = st.date_input("Fecha hasta", value=datetime.strptime('2024-06-30',"%Y-%m-%d"), format="YYYY-MM-DD")

    st.write(f"Importe total vendido por departamento {f_desde.strftime('%Y-%m-%d')} - {f_hasta.strftime('%Y-%m-%d')}")
    ventas_ciudades = get_ventas_ciudades(f_desde, f_hasta)

    map = folium.Map(location=[-32.151815, -63.774050], zoom_start=7)

    geo_data = "https://raw.githubusercontent.com/mgaitan/departamentos_argentina/refs/heads/master/departamentos-cordoba.json"

    columns_list = list(ventas_ciudades[0].keys())

    df = pd.DataFrame(
        data=[ventas.values() for ventas in ventas_ciudades],
        columns=columns_list
    )

    mapa, tabla = st.tabs(["Mapa","Tabla"])

    with tabla:
        st.dataframe(df, hide_index=True)

    with mapa:
        folium.Choropleth(
            geo_data=geo_data,
            name="choropleth",
            data=df,
            columns=["departamento","importe"],
            key_on="feature.properties.departamento",
            fill_color ='YlGn',
            fill_opacity=0.7,
            line_opacity=0.2,
            #threshold_scale=[0, 200000, 400000, 600000, 800000, 1000000],
            legend_name=f"Importe total",
        ).add_to(map)

        st_data = st_folium(map, width=725)
   

if __name__ == "__main__":
    mapa()
