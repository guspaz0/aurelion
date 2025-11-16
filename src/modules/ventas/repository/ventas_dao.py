import csv, logging, pathlib
from modules.db.db_connection import db
from typing import List, Dict, Any, Tuple
from datetime import datetime, date

logger = logging.getLogger(__file__)

class VentasDao:
    def __init__(self):
        self.conn = db.get_connection()
        self.csv_path = (pathlib.Path(__file__).parents[4] / "bd" / "ventas.csv").resolve()
        self.initialize()
    
    def initialize(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha TEXT NOT NULL,
                        id_cliente INTEGER NOT NULL,
                        medio_pago TEXT NOT NULL,
                        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                    )
                """)
            conn.commit()
            cursor.close()
        if self.count() == 0:
            self._load_from_csv()

    def count(self):
        with self.conn as conn:
            cursor = conn.cursor()
            (count,) = cursor.execute("SELECT COUNT(*) FROM ventas").fetchone()
            cursor.close()
            return count
        
    def get_all(self, desde = None, hasta = None):
        with self.conn as conn:
            cursor = conn.cursor()
            try:
                data = cursor.execute('''SELECT 
                        v.id_venta as id_venta,
                        v.fecha as fecha,
                        v.id_cliente as id_cliente,
                        c.nombre_cliente as nombre_cliente,
                        c.email as email,
                        v.medio_pago as medio_pago
                    FROM ventas v 
                    LEFT JOIN clientes c on c.id_cliente = v.id_cliente
                    WHERE v.fecha BETWEEN ? AND ?
                    ''', (
                        desde or date.fromisoformat("1980-01-01").strftime("%Y-%m-%d"), 
                        hasta or date.today().strftime("%Y-%m-%d"))
                    ).fetchall()
                return data
            except Exception as e:
                logger.error(f"Error: {e}")
            finally:
                cursor.close()
    
    def get_by_id(self, id_venta: int):
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('''SELECT
                        v.id_venta as id_venta,
                        v.fecha as fecha,
                        v.id_cliente as id_cliente,
                        c.nombre_cliente as nombre_cliente,
                        c.email as email,
                        v.medio_pago as medio_pago
                    FROM ventas v 
                    LEFT JOIN clientes c on c.id_cliente = v.id_cliente
                    WHERE v.id_venta = ?''', (id_venta,)).fetchone()
            cursor.close()
            return data
    
    def get_by_cliente(self, id_cliente: int) -> List[Tuple]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('''SELECT 
                        v.id_venta as id_venta,
                        v.fecha as fecha,
                        v.id_cliente as id_cliente,
                        c.nombre_cliente as nombre_cliente,
                        c.email as email,
                        v.medio_pago as medio_pago
                    FROM ventas v 
                    LEFT JOIN clientes c on c.id_cliente = v.id_cliente
                    WHERE v.id_cliente = ?''', (id_cliente,)).fetchall()
            cursor.close()
            return data
        
    def insert_venta(self, id_cliente: int, fecha: str, medio_pago: str, id_venta: int = None) -> int:
        with self.conn as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ventas (id_venta, fecha, id_cliente, medio_pago) VALUES (?, ?, ?, ?)", (id_venta or 'DEFAULT', fecha, id_cliente, medio_pago,))
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                logger.error(f"Error al insertar registro: {e}")
            finally:
                cursor.close()

    def get_medios_de_pago(self) -> List[str]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute("SELECT DISTINCT medio_pago FROM ventas").fetchall()
            cursor.close()
            return [medio for (medio,) in data]

    def _load_from_csv(self):
        """
        Loads the data from the CSV file into the repository.
        """
        with open(self.csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keys: List[str] = []
            for row in reader:
                dict: Dict[str, Any] = {}
                if len(keys) == 0:
                    keys = row
                    continue
                for i in range(0,len(keys)):
                    dict[keys[i]] = row[i] or ''
                self.insert_venta(
                    int(dict['id_cliente']),
                    dict['fecha'],
                    dict['medio_pago'],
                    int(dict['id_venta']),
                )
            csvfile.close()
                