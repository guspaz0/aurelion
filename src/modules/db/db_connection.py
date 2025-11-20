import sqlite3, pathlib, logging
import threading
from modules.clientes.clientes_dao import ClientesDao
from modules.productos.producto_dao import ProductoDao
from modules.ventas.ventas_dao import VentasDao
from modules.ventas.detalle_ventas_dao import DetalleVentasDao

logger = logging.getLogger(__file__)

db_path = (pathlib.Path(__file__).parents[3] / 'bd' / 'bd.sqlite').resolve()

class DbConnection:
    def __init__(self):
        # Allow sharing the connection across threads. Streamlit may access
        # the DB from different threads; set check_same_thread=False to avoid
        # the "SQLite objects created in a thread can only be used in that same thread" error.
        # Note: this does NOT make sqlite3 fully thread-safe — consider
        # creating a connection per request or serializing access with a Lock
        # for a more robust solution.
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._lock = threading.RLock()
        logger.info("Connected to database (check_same_thread=False)")
        self.clientesDao = ClientesDao(self.conn)
        self.detalleVentasDao = DetalleVentasDao(self.conn)
        self.productosDao = ProductoDao(self.conn)
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
        self.clientesDao._create_view()

    def get_connection(self):
        return self.conn

    def execute_query(self, query):
        # Use a local cursor and guard with a lock to reduce race conditions
        # when multiple threads use the same connection.
        with self._lock:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return rows

    def close(self):
        self.conn.close()
