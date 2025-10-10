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
clientes = st.Page("app/Clientes.py", title="Clientes", icon="👤")
mapa_ventas = st.Page("app/Mapa_ventas.py", title="Mapa Ventas", icon="📍")
ventas = st.Page("app/Ventas.py", title="Ventas", icon="📈")
home_page = st.Page("app/home.py", title="Home", icon="🏠", default=True)
productos = st.Page("app/Productos.py", title="Productos", icon="📦")

documentacion = st.Page("app/Documentacion.py", title="Documentación", icon="📖")



def run_app():
    try:
        pg = st.navigation({
            "Home": [home_page],  # default page
            "Ventas": [ventas, mapa_ventas],
            "Clientes": [clientes],
            "Productos": [productos],
            "Documentación": [documentacion]
        }, position="sidebar", expanded=True)
        pg.run()
    except Exception as e:
        st.error(f"Error al cargar la página: {e}")
        st.text(traceback.format_exc())


if __name__ == "__main__":
    run_app()