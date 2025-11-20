from modules.db.db_connection import DbConnection
from modules.ventas.ventas_service import VentasService
from modules.clientes.cliente_service import ClienteService
from modules.productos.producto_service import ProductoService


class App:
    """Simple container for service instances used by pages.

    This module exists so pages can import `app` without triggering
    the top-level Streamlit UI code in `main.py` (prevents circular imports).
    """
    def __init__(self):
        db = DbConnection()  # Initialize the
        self.ventas_service = VentasService(db)
        self.productos_service = ProductoService(db.productosDao)
        self.clientes_service = ClienteService(db.clientesDao)

app = App()