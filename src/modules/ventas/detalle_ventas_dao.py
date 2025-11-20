import pathlib, logging, csv
from sqlite3 import Connection
from typing import List, Dict, Any, Tuple
from .detalle_venta_model import DetalleVentaModel

logger = logging.getLogger(__file__)

GET_ALL = 'SELECT * FROM detalle_ventas_view'
COUNT = "SELECT COUNT(*) FROM detalle_ventas"
INSERT = '''
    INSERT INTO detalle_ventas(id_venta, id_producto, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
'''

class DetalleVentasDao:
    def __init__(self, conn: 'Connection'):
        self.conn = conn
        self.db_path = (pathlib.Path(__file__).parents[3] / "bd" / "detalle_ventas.csv").resolve()
        self._initialize()

    def _initialize(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalle_ventas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_venta INTEGER NOT NULL,
                    id_producto INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
                )
            ''')
            conn.commit()
            cursor.close()
        if self.count() == 0:
            self._load_from_csv()
    
    def count(self) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            (count,) = cursor.execute(COUNT).fetchone()
            cursor.close()
            return count
    
    def _create_view(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE VIEW IF NOT EXISTS detalle_venta_view AS SELECT
                dv.id_venta as id_venta,
                dv.id_producto as id_producto,
                p.nombre_producto as nombre_producto,
                dv.cantidad as cantidad,
                dv.precio_unitario as precio_unitario,
                (dv.cantidad * dv.precio_unitario) as importe,
                v.fecha as fecha
            FROM detalle_ventas dv 
            LEFT JOIN productos p ON dv.id_producto = p.id_producto
            LEFT JOIN ventas v ON v.id_venta = dv.id_venta''')
            conn.commit()
            cursor.close()

    def get_all(self) -> List[DetalleVentaModel]:
        with self.conn as conn:
            try:
                cursor = conn.cursor()
                data = cursor.execute(GET_ALL).fetchall()
                return [DetalleVentaModel(*detalle) for detalle in data]
            except Exception as e:
                logger.error(f"Error fetching all detalle ventas: {e}")
            finally:
                cursor.close()

    def insert_detalle_venta(self, id_venta: int, id_producto: int, cantidad: int, precio_unitario: float):
        with self.conn as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(INSERT, (id_venta, id_producto, cantidad, precio_unitario))
                conn.commit()
            except Exception as e:
                logger.error(f"Error inserting detalle venta: {e}")
            finally:
                cursor.close()
    
    def get_by_venta(self, id_venta: int) -> List[DetalleVentaModel]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL+' WHERE id_venta = ?', (id_venta,)).fetchall()
            cursor.close()
            return [DetalleVentaModel(*detalle) for detalle in data]
    
    def get_by_producto(self, id_producto: int) -> List[DetalleVentaModel]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL+' WHERE id_producto = ?', (id_producto,)).fetchall()
            cursor.close()
            return [DetalleVentaModel(*detalle) for detalle in data]
        
    def _load_from_csv(self):
        """
        Loads the data from the CSV file into the repository.
        """
        with open(self.db_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keys: List[str] = []
            for row in reader:
                dict: Dict[str, Any] = {}
                if len(keys) == 0:
                    keys = row
                    continue
                for i in range(0,len(keys)):
                    dict[keys[i]] = row[i] or ''
                self.insert_detalle_venta(
                    int(dict['id_venta']), 
                    int(dict['id_producto']),
                    int(dict['cantidad']),
                    float(dict['precio_unitario'])
                )
            csvfile.close()