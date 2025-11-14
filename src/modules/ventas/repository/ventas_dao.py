import pathlib
from modules.db.db_connection import db

class VentasDao:
    def __init__(self):
        self.conn = db.get_connection()
        self.csv_path = (pathlib.Path(__file__).parents[3] / "bd" / "ventas.csv").resolve()
    
    def initialize(self):
        with self.conn as conn:
            
