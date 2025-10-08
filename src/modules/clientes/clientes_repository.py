from inspect import _void
from typing import Any, Dict, List
import os, csv
from modules.clientes.cliente_model import ClienteModel

class ClientesRepository:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "bd", "clientes.csv")
        self.clientes: List[ClienteModel] = []
        self.ciudades = set()
        self.departamentos = {
            "mendiolaza": "COLON",
            "cordoba": "CAPITAL",
            "villa maria": "GENERAL SAN MARTIN",
            "alta gracia": "SANTA MARIA",
            "carlos paz": "PUNILLA",
            "rio cuarto": "RIO CUARTO"
        }
        self._load()

    def _load(self):
        """
        Loads data from the csv file into the clientes list.
        """
        with open(self.db_path, mode='r',encoding='utf-8') as csvfile:
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
                cliente = ClienteModel(**dict)
                cliente.departamento = self.departamentos[cliente.ciudad.lower()]
                self.clientes.append(cliente)
                self.ciudades.add(dict['ciudad'] or '')
            csvfile.close()

    def get_all(self) -> List[ClienteModel]:
        """
        Returns all the clients from the database.
        """
        return self.clientes
    
    def buscar_por_id(self, id: int) -> ClienteModel:
        """
        Returns the client with the given id.

        :param id: int - The id of the client to search for.
        """
        return [cliente for cliente in self.clientes if cliente.id_cliente == id][0]
    
    def agregar(self, cliente: ClienteModel) -> _void:
        """
        Saves the given client to the database.

        :param cliente: ClienteModel - The client to save.
        """
        try:
            # chequeo que no haya repetidos, si no existe entra al except
            set = [i.to_dict() for i in self.clientes]
            set.index(cliente.to_dict())
        except:
            self.clientes.append(cliente)
            #escribo a la base de datos csv
            with open(self.db_path, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Assuming cliente has a method 'to_dict()' that returns its attributes as a dictionary
                writer.writerow(cliente.to_dict().values())