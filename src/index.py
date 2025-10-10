import logging
import streamlit as st
import pandas as pd
import importlib
import traceback

# Set up the logger to log to console with a custom format
logging.basicConfig(
    level=logging.INFO,
    format='\x1b[36m%(asctime)s\x1b[0m │ %(levelname)s │ \x1b[90m%(module)s:%(lineno)s\x1b[0m │ %(funcName)s │ %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

pages = [
    st.Page("pages/home.py", title="Home", icon="🏠"),
    st.Page("pages/Mapa_ventas.py", title="Mapa Ventas", icon="📍"),
    st.Page("pages/Clientes.py", title="Clientes", icon="👤"),
    st.Page("pages/Productos.py", title="Productos", icon="📦"),
    st.Page("pages/Ventas.py", title="Ventas", icon="📈"),
    st.Page("pages/documentacion/Documentacion.py", title="Documentación", icon="📖"),
]


def run_app():
    try:
        pg = st.navigation(pages=pages, position="sidebar", expanded=True)
        pg.run()
    except Exception as e:
        st.error(f"Error al cargar la página: {e}")
        st.text(traceback.format_exc())


if __name__ == "__main__":
    run_app()