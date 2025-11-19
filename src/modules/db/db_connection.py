import sqlite3, pathlib, logging
from .dao.clientes_dao import ClientesDao
from .dao.productos_dao import ProductosDao
from .dao.ventas_dao import VentasDao
from .dao.detalle_ventas_dao import DetalleVentasDao

logger = logging.getLogger(__file__)

db_path = (pathlib.Path(__file__).parents[3] / 'bd' / 'bd.sqlite').resolve()

class DbConnection:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        logger.info("Connected to database")
        self.clientesDao = ClientesDao(self.conn)
        self.detalleVentasDao = DetalleVentasDao(self.conn)
        self.productosDao = ProductosDao(self.conn)
        self.ventasDao = VentasDao(self)
        self._initialize()

    def _initialize(self):
        self.clientesDao._initialize()
        self.productosDao._initialize()
        self.ventasDao._initialize()
        self.detalleVentasDao._initialize()
        # Crear vistas
        self.productosDao._create_view()
        self.ventasDao._create_view()
        self.detalleVentasDao._create_view()

    def get_connection(self):
        return self.conn

    def execute_query(self, query):
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
