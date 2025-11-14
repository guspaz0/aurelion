import pathlib, logging, csv
from modules.db.db_connection import db
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__file__)

class ClientesDao:
    def __init__(self):
        self.conn = db.get_connection()
        self.csv_path = (pathlib.Path(__file__).parents[3] / "bd" / "clientes.csv").resolve()
        self.departamentos = {
            "mendiolaza": "COLON",
            "cordoba": "CAPITAL",
            "villa maria": "GENERAL SAN MARTIN",
            "alta gracia": "SANTA MARIA",
            "carlos paz": "PUNILLA",
            "rio cuarto": "RIO CUARTO"
        }

    def initialize(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_cliente TEXT NOT NULL,
                    email TEXT NOT NULL,
                    ciudad TEXT NOT NULL,
                    departamento TEXT NOT NULL,
                    fecha_alta TEXT NOT NULL,
                    FOREIGN KEY(ciudad) REFERENCES ciudades(nombre_ciudad)
                )
            ''')
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

    def get_all(self) -> List[Tuple]:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute("SELECT * FROM clientes").fetchall()
            cursor.close()
            return data
    
    def get_by_id(self, id) -> Tuple:
        with self.conn as conn:
            cursor = conn.cursor()
            data = cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?',(id,)).fetchone()
            cursor.close()
            return data

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