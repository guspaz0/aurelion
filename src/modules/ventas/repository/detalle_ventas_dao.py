import pathlib, logging, csv
from modules.db.db_connection import db
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__file__)

class DetalleVentasDao:
    def __init__(self):
        self.conn = db.get_connection()
        self.db_path = (pathlib.Path(__file__).parents[4] / "bd" / "detalle_ventas.csv").resolve()
        self.initialize()

    def initialize(self):
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
            cursor.close()
        if self.count() == 0:
            self._load_from_csv()
    
    def count(self):
        with self.conn as conn:
            cursor = conn.cursor()
            (count,) = cursor.execute("SELECT COUNT(*) FROM detalle_ventas").fetchone()
            cursor.close()
            return count
        
    def get_all(self):
        with self.conn as conn:
            try:
                cursor = conn.cursor()
                data = cursor.execute('''SELECT
                        dv.id_venta as id_venta,
                        dv.id_producto as id_producto,
                        p.nombre_producto as nombre_producto,
                        dv.cantidad as cantidad,
                        dv.precio_unitario as precio_unitario,
                        (dv.cantidad * dv.precio_unitario) as importe
                    FROM detalle_ventas dv 
                    LEFT JOIN productos p ON dv.id_producto = p.id_producto
                ''').fetchall()
                return data
            except Exception as e:
                logger.error(f"Error fetching all detalle ventas: {e}")
            finally:
                cursor.close()

    def insert_detalle_venta(self, id_venta: int, id_producto: int, cantidad: int, precio_unitario: float):
        with self.conn as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO detalle_ventas(id_venta, id_producto, cantidad, precio_unitario)
                            VALUES (?, ?, ?, ?)
                ''', (id_venta, id_producto, cantidad, precio_unitario))
                conn.commit()
            except Exception as e:
                logger.error(f"Error inserting detalle venta: {e}")
            finally:
                cursor.close()
    
    def get_by_venta(self, id_venta: int) -> List[Tuple]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('''SELECT
                        dv.id_venta as id_venta,
                        dv.id_producto as id_producto,
                        p.nombre_producto as nombre_producto,
                        dv.cantidad as cantidad,
                        dv.precio_unitario as precio_unitario,
                        (dv.cantidad * dv.precio_unitario) as importe
                    FROM detalle_ventas dv 
                    LEFT JOIN productos p ON dv.id_producto = p.id_producto
                    WHERE id_venta = ?''', (id_venta,)).fetchall()
            cursor.close()
            return data
    
    def get_by_producto(self, id_producto: int) -> List[Tuple]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('''SELECT 
                        dv.id_venta as id_venta,
                        dv.id_producto as id_producto,
                        p.nombre_producto as nombre_producto,
                        dv.cantidad as cantidad,
                        dv.precio_unitario as precio_unitario,
                        (dv.cantidad * dv.precio_unitario) as importe
                    FROM detalle_ventas dv 
                    LEFT JOIN productos p ON dv.id_producto = p.id_producto
                    WHERE id_producto = ?''', (id_producto,)).fetchall()
            cursor.close()
            return data
        
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