import logging
import streamlit as st
import pandas as pd
import importlib
import traceback
# try to import app from package or local module name depending on execution context
try:
    from src.app_state import app
except Exception:
    from app_state import app

logger = logging.getLogger(__name__)

def home():
    logger.info("render home page")
    _author_ = "https://www.linkedin.com/in/gustavo-rodolfo-paz/"

    st.set_page_config(
        page_title="Aurelion",
        page_icon=":nerd:",
        layout="wide"
    )

    st.title("Dashboard Aurelion")
    st.header("Bienvenido/a")
    st.markdown(
        """
        Aurelion es una tienda/despensa/supermercado que vende productos de limpieza y alimentos al por menor y mayor. Desarrolla sus actividades principales dentro de la provincia de cordoba, Argentina.
        Desarrollado por [Gustavo Rodolfo Paz](%s).
        
        """
        % _author_
    )

    st.subheader("Ultimas ventas")

    ventas = app.ventas_service.get_all()[:5]

    st.dataframe(
        pd.DataFrame(
            data=[venta.__dict__.values() for venta in ventas],
            columns=ventas[0].__dict__.keys()
        ),
        hide_index=True
    )

if __name__ == "__main__":
    home()