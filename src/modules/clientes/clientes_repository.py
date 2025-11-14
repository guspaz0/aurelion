from inspect import _void
from typing import Any, Dict, List
import pathlib
import os, csv
from modules.clientes.cliente_model import ClienteModel
from modules.clientes.clientes_dao import ClientesDao

class ClientesRepository:
    def __init__(self):
        self._dao = ClientesDao()
        self.ciudades = set()

    def get_all(self) -> List[ClienteModel]:
        """
        Returns all the clients from the database.
        """
        return [ClienteModel(*row) for row in self._dao.get_all()]
    
    def buscar_por_id(self, id: int) -> ClienteModel:
        """
        Returns the client with the given id.

        :param id: int - The id of the client to search for.
        """
        return ClienteModel(*self._dao.get_by_id(id))
    
    def agregar(self, cliente: ClienteModel) -> _void:
        """
        Saves the given client to the database.

        :param cliente: ClienteModel - The client to save.
        """
        # chequeo que no haya repetidos, si no existe entra al except
        self._dao.insert_cliente(**cliente)