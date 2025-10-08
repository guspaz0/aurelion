from modules import VentasService, ProductoService, ClienteService
import logging
import streamlit as st
import pandas as pd

class App:
    """
    Backend class for the Aurelion application. This class is responsible for managing the application's state and providing access to the services.
    """
    def __init__(self):
        self.ventas_service = VentasService()
        self.productos_service = ProductoService()
        self.clientes_service = ClienteService()

app = App()

# Set up the logger to log to console with a custom format
logging.basicConfig(
    level=logging.INFO,
    format='\x1b[36m%(asctime)s\x1b[0m │ %(levelname)s │ \x1b[90m%(module)s:%(lineno)s\x1b[0m │ %(funcName)s │ %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Aurelion",
    page_icon=":nerd:",
    layout="wide"
)

def index():
    logger.info("refresco")
    _author_ = "https://www.linkedin.com/in/gustavo-rodolfo-paz/"
    
    st.title("Dashboard Aurelion")
    st.header("Bienvenido/a")
    st.markdown(
        """
        Aurelion es una tienda/despensa/supermercado que vende productos de limpieza y alimentos al por menor y mayor. Desarrolla sus actividades principales dentro de la provincia de cordoba, Argentina.
        Desarrollado por [Gustavo Rodolfo Paz](%s).
        
        """
        % _author_
    )

    # left, right = st.columns(2)

    # with left:
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
    index()
