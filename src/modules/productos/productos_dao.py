import pathlib, logging, csv
from modules.db.db_connection import db
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__file__)

class ProductosDao:
    def __init__(self):
        self.conn = db.get_connection()
        self.csv_path = (pathlib.Path(__file__).parents[3] / "bd" / "productos.csv").resolve()
        self.initialize()

    def initialize(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_producto TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    precio_unitario REAL NOT NULL
                )
            ''')
            conn.commit()
            cursor.close()
            if (self.count() == 0):
                self._load_csv_to_db()
    
    def count(self) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            (count,) = cursor.execute('SELECT COUNT(*) FROM productos').fetchall()
            cursor.close()
            return count
    
    def insert_product(self, id_producto, nombre_producto, categoria, precio_unitario) -> None:
        with self.conn as conn:
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO productos (id_producto, nombre_producto, categoria, precio_unitario)
                        VALUES (?, ?, ?, ?);
                    ''', (id_producto, nombre_producto, categoria, precio_unitario))
                conn.commit()
            except Exception as e:
                logger.error(f"Error inserting product: {e}")
            finally:
                cursor.close()
    
    def get_all(self) -> List[Tuple]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('SELECT * FROM productos').fetchall()
            cursor.close()
            return data
    
    def update_product(self, id_producto, nombre_producto, categoria, precio_unitario) -> None:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE productos SET nombre_producto = ?, categoria = ?, precio_unitario = ? 
                WHERE id_producto = ?; ''',
                (nombre_producto, categoria, precio_unitario, id_producto))
            conn.commit()
            cursor.close()

    def delete_product(self, id_producto) -> None:
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM productos WHERE id_producto = ?', (id_producto,))
            conn.commit()
            cursor.close()

    def get_by_id(self, id_producto: int) -> Tuple:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('SELECT * FROM productos WHERE id_producto = ?', (id_producto,)).fetchone()
            cursor.close()
            return data
        
    def _load_csv_to_db(self):
        """
        Loads the data from the csv file into memory.
        """
        db_path = (pathlib.Path(__file__).parents[3] / "bd" / "productos.csv").resolve()
        with open(db_path, mode='r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keys: List[str] = []
            for row in reader:
                dict: Dict[str, Any] = {}
                if len(keys) == 0:
                    keys = row
                    continue
                for i in range(0,len(keys)):
                    dict[keys[i]] = row[i] or ''
                dict['id_producto'] = int(dict['id_producto'])
                dict['precio_unitario'] = float(dict['precio_unitario'])
                self.insert_product(**dict)
            csvfile.close()