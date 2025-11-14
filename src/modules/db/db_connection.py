import sqlite3
import pathlib

db_path = (pathlib.Path(__file__).parents[3] / 'bd' / 'bd.sqlite').resolve()

class DbConnection:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        print(f"Database path: {db_path}")
        print("Connected to database")

    def get_connection(self):
        return self.conn

    def execute_query(self, query):
        self.cursor = self.conn.cursor()
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

db = DbConnection()