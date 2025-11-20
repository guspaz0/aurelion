import pathlib, logging, csv
from sqlite3 import Connection, OperationalError
from typing import List, Dict, Any, Tuple
from .cliente_model import ClienteModel

logger = logging.getLogger(__file__)

GET_ALL = 'SELECT * FROM clientes_detalle_view'
COUNT = "SELECT count(*) FROM clientes"
GET_CIUDADES = "SELECT DISTINCT ciudad FROM clientes"

class ClientesDao:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.csv_path = (pathlib.Path(__file__).parents[3] / "bd" / "clientes.csv").resolve()
        self.departamentos = {
            "mendiolaza": "COLON",
            "cordoba": "CAPITAL",
            "villa maria": "GENERAL SAN MARTIN",
            "alta gracia": "SANTA MARIA",
            "carlos paz": "PUNILLA",
            "rio cuarto": "RIO CUARTO"
        }

    def _initialize(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_cliente TEXT NOT NULL,
                    email TEXT NOT NULL,
                    ciudad TEXT NOT NULL,
                    departamento TEXT,
                    fecha_alta TEXT NOT NULL,
                    FOREIGN KEY(ciudad) REFERENCES ciudades(nombre_ciudad)
                )
            ''')
            conn.commit()
            if self.count() == 0:
                self._load_from_csv()
            cursor.close()
    
    def _create_view(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE VIEW IF NOT EXISTS clientes_detalle_view AS SELECT 
                c.*, 
                CASE 
                WHEN vdv.id_cliente IS NULL THEN json_array()
                ELSE json_group_array(json_object(
                    'id_venta', vdv.id_venta,
                    'id_cliente', vdv.id_cliente,
                    'nombre_cliente', vdv.nombre_cliente,
                    'email', vdv.email,
                    'medio_pago', vdv.medio_pago,
                    'ciudad', vdv.ciudad,
                    'fecha', vdv.fecha,
                    'importe', vdv.importe,
                    'detalle', vdv.detalle
                ))
                END as ventas
                FROM clientes c 
                LEFT JOIN ventas_detalles_view vdv ON c.id_cliente = vdv.id_cliente
                GROUP BY c.id_cliente''')
            conn.commit()
            cursor.close()

    def insert_cliente(self, id_cliente, nombre_cliente, email, ciudad, departamento, fecha_alta):
        with self.conn as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO clientes (id_cliente, nombre_cliente, email, ciudad, departamento, fecha_alta)
                                    VALUES (?, ?, ?, ?, ?, ?);
                ''', (id_cliente, nombre_cliente, email, ciudad, departamento, fecha_alta))
                conn.commit()
            except Exception as e:
                logger.error(f"Error inserting cliente: {e}")
            finally:
                cursor.close()

    def get_all(self) -> List[ClienteModel]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL).fetchall()
            cursor.close()
            return [ClienteModel(*cliente) for cliente in data]
    
    def get_by_id(self, id_cliente: int) -> ClienteModel:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_ALL+' WHERE id_cliente = ?',(id_cliente,)).fetchone()
            return ClienteModel(*data)

    def count(self) -> int:
        with self.conn as conn:
            try:
                cursor = conn.cursor()
                (count,) = cursor.execute(COUNT).fetchone()
                cursor.close()
                return count
            except OperationalError as e:
                (arg1,) = e.args
                if arg1.startswith('no such table'):
                    self.initialize()
    
    def get_ciudades(self) -> List[str]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute(GET_CIUDADES).fetchall()
            cursor.close()
            return [ciudad for (ciudad,) in data]

    def _load_from_csv(self):
        """
        Loads data from the csv file into the clientes list.
        """
        with open(self.csv_path, mode='r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keys: List[str] = []
            for row in reader:
                dict: Dict[str, Any] = {}
                if len(keys) == 0:
                    keys = row
                    continue
                for i in range(0,len(keys)):
                    dict[keys[i]] = row[i] or ''
                dict['id_cliente'] = int(dict['id_cliente'])
                dict['departamento'] = self.departamentos[dict['ciudad'].lower()] or ''
                self.insert_cliente(**dict)
            csvfile.close()