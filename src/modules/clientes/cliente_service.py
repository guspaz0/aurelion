from datetime import datetime
from inspect import _void
from typing import Any, Dict, List, TYPE_CHECKING
from . import ClienteModel, ClientesRepository

if TYPE_CHECKING:
    from modules import DbConnection

class ClienteService:
    def __init__(self, db: 'DbConnection'):
        self.repository = ClientesRepository(db)

    def get_all(self) -> List[ClienteModel]:
        """
        Retorna todos los clientes en la base de datos.
        """
        return self.repository.get_all()
    
    def buscar_por_id(self, id_cliente: int) -> ClienteModel:
        """
        Retorna el cliente con el id especificado.

        :param id: El id del cliente a buscar.
        """
        return self.repository.buscar_por_id(id_cliente)
    
    def agregar(self, cliente: Dict[str, Any]) -> ClienteModel:
        """
        Agrega un nuevo cliente a la base de datos

        :param cliente: El diccionario con los datos del cliente.
        """
        cliente = ClienteModel(**cliente)
        self.repository.agregar(cliente)
        return cliente
    
    def total_ventas(self, desde: datetime | str = None, hasta: datetime | str = None) -> List[Dict[str, str | int | float]]:
        """
        Retorna una lista de clientes que han realizado compras en el rango de fechas especificado
        
        :param desde: La fecha inicial del rango. Si no se especifica, se considera la totalidad de los registros.
        :param hasta: La fecha final del rango. Si no se especifica, se considera la totalidad de los registros.
        """
        clientes = map(lambda x: {**x.to_dict(), **x.total_ventas(desde,hasta)}, self.get_all())
        clientes = list(filter(lambda x: x['importe'] != 0, clientes))
        
        for i in range(0, len(clientes)):
            del clientes[i]["ventas"]

        return sorted(clientes, key=lambda x: x["importe"], reverse=True)