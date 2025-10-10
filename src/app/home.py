import logging
import streamlit as st

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

        Desarrollado con [Streamlit](https://streamlit.io/) y [Python](https://www.python.org/).
        
        """
        % _author_
    )

    st.page_link("app/Documentacion.py", label="Documentación", icon="📖")


if __name__ == "__main__":
    home()