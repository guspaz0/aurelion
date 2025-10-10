from modules import VentasService, ProductoService, ClienteService


class App:
    """Simple container for service instances used by pages.

    This module exists so pages can import `app` without triggering
    the top-level Streamlit UI code in `index.py` (prevents circular imports).
    """
    def __init__(self):
        self.ventas_service = VentasService()
        self.productos_service = ProductoService()
        self.clientes_service = ClienteService()


app = App()
