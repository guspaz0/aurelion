import logging
import streamlit as st
import pandas as pd
import traceback

# Set up the logger to log to console with a custom format
logging.basicConfig(
    level=logging.INFO,
    format='\x1b[36m%(asctime)s\x1b[0m │ %(levelname)s │ \x1b[90m%(module)s:%(lineno)s\x1b[0m │ %(funcName)s │ %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

clientes = st.Page("_pages/Clientes.py", title="Clientes", icon="👤")
mapa_ventas = st.Page("_pages/MapaVentas.py", title="Mapa Ventas", icon="📍")
ventas = st.Page("_pages/Ventas.py", title="Ventas", icon="📈")
home_page = st.Page("_pages/home.py", title="Home", icon="🏠", default=True)
productos = st.Page("_pages/Productos.py", title="Productos", icon="📦")
documentacion = st.Page("_pages/Documentacion.py", title="Documentación", icon="📖")
analisisEDA = st.Page("_pages/analisisEda.py", title="Analisis EDA", icon="📊")

def run_app():
    try:
        pg = st.navigation({
            "Home": [home_page],  # default page
            "Reportes": [ventas, mapa_ventas, clientes, productos],
            "Analisis EDA": [analisisEDA],
            "Documentación": [documentacion]
        }, position="sidebar", expanded=True)
        pg.run()
    except Exception as e:
        st.error(f"Error al cargar la página: {e}")
        st.text(traceback.format_exc())


if __name__ == "__main__":
    run_app()