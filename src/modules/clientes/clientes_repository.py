from inspect import _void
from typing import Any, Dict, List, TYPE_CHECKING
from modules.clientes.cliente_model import ClienteModel

if TYPE_CHECKING:
    from modules.db.db_connection import DbConnection

class ClientesRepository:
    def __init__(self, db: 'DbConnection'):
        self._db = db
    
    @property
    def ciudades(self):
        self._ciudades = self._db.clientesDao.get_ciudades()
        return self._ciudades
    
    @ciudades.setter
    def ciudades(self, value):
        self._ciudades = value

    def get_all(self) -> List[ClienteModel]:
        """
        Returns all the clients from the database.
        """
        clientes = self._db.clientesDao.get_all()
        for cliente in clientes:
            cliente.ventas = self._db.ventasDao.get_by_cliente(cliente.id_cliente)
            #cliente.total_ventas = sum(venta.importe for venta in cliente.ventas)
        return clientes
    
    def buscar_por_id(self, id: int) -> ClienteModel:
        """
        Returns the client with the given id.

        :param id: int - The id of the client to search for.
        """
        cliente = self._db.clientesDao.get_by_id(id)
        cliente.ventas = self._db.ventasDao.get_by_cliente(cliente.id_cliente)
        #cliente.total_ventas = sum(venta.importe for venta in cliente.ventas)
        return cliente
    
    def agregar(self, cliente: ClienteModel) -> _void:
        """
        Saves the given client to the database.

        :param cliente: ClienteModel - The client to save.
        """
        # chequeo que no haya repetidos, si no existe entra al except
        self._db.clientesDao.insert_cliente(**cliente)