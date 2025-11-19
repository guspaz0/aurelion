from modules import VentasService, ProductoService, ClienteService, DbConnection
import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format='\x1b[36m%(asctime)s\x1b[0m │ %(levelname)s │ \x1b[90m%(module)s:%(lineno)s\x1b[0m │ %(funcName)s │ %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

class App:
    """Simple container for service instances used by pages.

    This module exists so pages can import `app` without triggering
    the top-level Streamlit UI code in `index.py` (prevents circular imports).
    """
    def __init__(self):
        db = DbConnection()  # Initialize the
        self.ventas_service = VentasService(db)
        self.productos_service = ProductoService(db)
        self.clientes_service = ClienteService(db)


app = App()

#Testing the services
cliente1 = app.clientes_service.buscar_por_id(2)
print(cliente1)
ventas_cliente1 = cliente1.ventas
print(ventas_cliente1[0].detalle)

# producto = app.productos_service.get_by_id(1)
# print(producto)
# print(producto.ventas)