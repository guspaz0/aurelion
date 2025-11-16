from datetime import datetime
import os, csv, logging
from typing import Dict, List, TYPE_CHECKING
from modules.ventas.repository.ventas_repository import VentasRepository

logger = logging.getLogger(__file__)

if TYPE_CHECKING:
    from modules.ventas.models.venta_model import VentaModel

class VentasService:
    def __init__(self):
        self._repository = VentasRepository()
    
    def get_all(self, f_desde: datetime | str = None, f_hasta: datetime | str = None) -> List['VentaModel']:
        """Retorna todos los registros de ventas en la base de datos. Ordenados por fecha en orden descendente."""
        ventas = self._repository.get_all(f_desde, f_hasta)
        ventas.sort(key=lambda x: x.fecha, reverse=True)
        return ventas
    
    def get_by_id_venta(self, id_venta: int) -> 'VentaModel':
        """
        Retorna el registro de venta con el id especificado

        :param id_venta: El id del registro de venta a buscar.
        """
        return self._repository.get_by_id_venta(int(id_venta))
    
    def get_by_id_cliente(self, id_cliente: int) -> List['VentaModel']:
        """
        Retorna todos los registros de ventas asociados al cliente especificado

        :param id_cliente: El id del cliente a buscar
        """
        return self._repository.get_by_id_cliente(id_cliente)
    
    def get_ventas_por_ciudad(self, desde: datetime | str = None, hasta: datetime | str = None) -> List[Dict[str, float | str]]:
        """
        Retorna la sumatoria de los importes de las ventas realizadas discriminado por ciudad y filtrado por fecha, si se proporciona.
        
        :param desde: Fecha inicial para filtrar las ventas
        :param hasta: Fecha final para filtrar
        """
        from modules.clientes.clientes_repository import ClientesRepository
        clientes_repo = ClientesRepository()
        ciudades: List[str] = list(clientes_repo.ciudades)
        departamentos: Dict[str, str] = dict(clientes_repo._dao.departamentos)
        ventas_ciudades = dict()
        for ciudad in ciudades:
            ventas_ciudades[ciudad] = 0
        for venta in self.get_all(desde,hasta):
            ventas_ciudades[venta.ciudad] += venta.importe
        result = map(lambda x: { "ciudad": x.upper(), "departamento": departamentos[x.lower()] or x.upper(), "importe": ventas_ciudades[x] }, ciudades)

        return sorted(result, key=lambda x: x['importe'], reverse=True)
