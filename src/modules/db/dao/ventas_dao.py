import csv, logging, pathlib
from typing import List, Dict, Any, Tuple, TYPE_CHECKING
from datetime import datetime, date
from modules.ventas.models.venta_model import VentaModel

if TYPE_CHECKING:
    from modules.db.db_connection import DbConnection

logger = logging.getLogger(__file__)

GET_ALL = 'SELECT * FROM ventas_detalles_view'

class VentasDao:
    def __init__(self, db: 'DbConnection'):
        self.departamentos = db.clientesDao.departamentos
        self.conn = db.get_connection()
        self.csv_path = (pathlib.Path(__file__).parents[4] / "bd" / "ventas.csv").resolve()
    
    def _initialize(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ventas (
                        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                        fecha TEXT NOT NULL,
                        id_cliente INTEGER NOT NULL,
                        medio_pago TEXT NOT NULL,
                        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                    )
                ''')
            conn.commit()
            cursor.close()
        if self.count() == 0:
            self._load_from_csv()
    
    def _create_view(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE VIEW IF NOT EXISTS ventas_detalles_view AS
                SELECT 
                    v.id_venta as id_venta,
                    v.fecha as fecha,
                    v.id_cliente as id_cliente,
                    c.nombre_cliente as nombre_cliente,
                    c.email as email,
                    v.medio_pago as medio_pago,
                    c.ciudad as ciudad,
                    SUM(dv.cantidad * dv.precio_unitario) as importe,
                    json_group_array(json_object(
                        'id_venta', dv.id_venta,
                        'id_producto', dv.id_producto,
                        'nombre_producto', p.nombre_producto,
                        'cantidad', dv.cantidad,
                        'precio_unitario', dv.precio_unitario,
                        'importe', (dv.cantidad * dv.precio_unitario),
                        'fecha', v.fecha
                    )) as detalle
                FROM ventas v 
                LEFT JOIN clientes c ON c.id_cliente = v.id_cliente
                LEFT JOIN detalle_ventas dv ON dv.id_venta = v.id_venta
                LEFT JOIN productos p ON dv.id_producto = p.id_producto
                GROUP BY v.id_venta
            ''')
            conn.commit()
            cursor.close()

    def count(self) -> int:
        with self.conn as conn:
            cursor = conn.cursor()
            (count,) = cursor.execute("SELECT COUNT(*) FROM ventas").fetchone()
            cursor.close()
            return count
        
    def get_all(self, desde = None, hasta = None) -> List['VentaModel']:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL+' WHERE fecha BETWEEN ? AND ?', (
                    desde or date.fromisoformat("1980-01-01").strftime("%Y-%m-%d"), 
                    hasta or date.today().strftime("%Y-%m-%d"))
                ).fetchall()
            ventas = [VentaModel(*venta) for venta in data]
            for venta in ventas:
                venta.departamento = self.departamentos[venta.ciudad]
            return ventas

    
    def get_by_id(self, id_venta: int) -> VentaModel:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL+' WHERE id_venta = ?', (id_venta,)).fetchone()
            cursor.close()
            venta = VentaModel(*data)
            venta.departamento = self.departamentos[venta.ciudad]
            return venta
    
    def get_by_cliente(self, id_cliente: int) -> List[VentaModel]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL+' WHERE id_cliente = ?', (id_cliente,)).fetchall()
            cursor.close()
            ventas = [VentaModel(*venta) for venta in data]
            return ventas
    
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
    
    def total_ventas_grouped_by_medio_de_pago(self, desde = None,hasta = None) -> Dict[str,float]:
        with self.conn as conn:
            cusor = conn.cursor()
            query = "SELECT medio_pago, SUM(total) FROM ventas"

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
                