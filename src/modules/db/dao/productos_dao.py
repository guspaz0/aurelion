import pathlib, logging, csv
from typing import List, Dict, Any, Tuple, TYPE_CHECKING
from modules.productos.producto_model import ProductoModel

if TYPE_CHECKING:
    from sqlite3 import Connection

logger = logging.getLogger(__file__)

GET_ALL = 'SELECT * FROM productos_detalle_view'
INSERT = '''
    INSERT INTO productos (id_producto, nombre_producto, categoria, precio_unitario)
        VALUES (?, ?, ?, ?);
'''

class ProductosDao:
    def __init__(self, conn: 'Connection'):
        self.conn = conn
        self.csv_path = (pathlib.Path(__file__).parents[3] / "bd" / "productos.csv").resolve()
        self._initialize()

    def _initialize(self):
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
            if self.count() == 0:
                self._load_csv_to_db()

    def count(self) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            (count,) = cursor.execute('SELECT COUNT(*) FROM productos').fetchone()
            cursor.close()
            return count

    def _create_view(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE VIEW IF NOT EXISTS productos_detalle_view AS SELECT
                p.id_producto as id_producto, 
                p.nombre_producto as nombre_producto,
                p.categoria as categoria,
                p.precio_unitario as precio_unitario,
                json_group_array(json_object(
                    'id_venta', dv.id_venta,
                    'id_producto', dv.id_producto,
                    'nombre_producto', p.nombre_producto,
                    'cantidad', dv.cantidad,
                    'precio_unitario', dv.precio_unitario,
                    'importe', (dv.cantidad * dv.precio_unitario),
                    'fecha', v.fecha
                )) as ventas
            FROM productos p
            LEFT JOIN detalle_ventas dv ON p.id_producto = dv.id_producto
            LEFT JOIN ventas v ON dv.id_venta = v.id_venta
            GROUP BY p.id_producto
            ''')
            conn.commit()
            cursor.close()
    
    def insert_product(self, id_producto, nombre_producto, categoria, precio_unitario) -> None:
        with self.conn as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(INSERT, (id_producto, nombre_producto, categoria, precio_unitario))
                conn.commit()
            except Exception as e:
                logger.error(f"Error inserting product: {e}")
            finally:
                cursor.close()
    
    def get_all(self) -> List[ProductoModel]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL).fetchall()
            cursor.close()
            return [ProductoModel(*producto) for producto in data]
    
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

    def get_by_id(self, id_producto: int) -> ProductoModel:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL+' WHERE id_producto = ?', (id_producto,)).fetchone()
            cursor.close()
            return ProductoModel(*data)
        
    def get_categorias(self) -> List[str]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('SELECT DISTINCT categoria FROM productos').fetchall()
            cursor.close()
            return [category for (category,) in data]
        
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