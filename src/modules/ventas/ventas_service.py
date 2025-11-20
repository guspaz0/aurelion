from datetime import datetime, date
import os, csv, logging
from typing import Dict, List, TYPE_CHECKING

logger = logging.getLogger(__file__)

if TYPE_CHECKING:
    from modules.ventas.venta_model import VentaModel
    from modules.ventas.ventas_dao import VentasDao
    from modules import DbConnection

class VentasService:
    def __init__(self, db: 'DbConnection'):
        self._dao: 'VentasDao' = db.ventasDao
        self.ciudades: List[str] = db.clientesDao.get_ciudades()
    
    def get_all(self, f_desde: datetime | str = None, f_hasta: datetime | str = None) -> List['VentaModel']:
        """Retorna todos los registros de ventas en la base de datos. Ordenados por fecha en orden descendente."""
        if not f_desde or not f_hasta:
            return self._dao.get_all()
        if all(isinstance(fecha, str) for fecha in (f_desde,f_hasta)):
            f_desde = datetime.strptime(f_desde, "%Y-%m-%d")
            f_hasta = datetime.strptime(f_hasta, "%Y-%m-%d")
        if all(isinstance(fecha, date) for fecha in (f_desde, f_hasta)):
            f_desde = datetime.strptime(f_desde.strftime("%Y-%m-%d"), "%Y-%m-%d")
            f_hasta = datetime.strptime(f_hasta.strftime("%Y-%m-%d"), "%Y-%m-%d")
        
        ventas = self._dao.get_all(f_desde, f_hasta)
        ventas.sort(key=lambda x: x.fecha, reverse=True)
        return ventas
    
    def get_by_id_venta(self, id_venta: int) -> 'VentaModel':
        """
        Retorna el registro de venta con el id especificado

        :param id_venta: El id del registro de venta a buscar.
        """
        return self._dao.get_by_id(int(id_venta))
    
    def get_by_id_cliente(self, id_cliente: int) -> List['VentaModel']:
        """
        Retorna todos los registros de ventas asociados al cliente especificado

        :param id_cliente: El id del cliente a buscar
        """
        return self._dao.get_by_cliente(id_cliente)
    
    def get_ventas_por_ciudad(self, desde: datetime | str = None, hasta: datetime | str = None) -> List[Dict[str, float | str]]:
        """
        Retorna la sumatoria de los importes de las ventas realizadas discriminado por ciudad y filtrado por fecha, si se proporciona.
        
        :param desde: Fecha inicial para filtrar las ventas
        :param hasta: Fecha final para filtrar
        """

        departamentos: Dict[str, str] = self._dao.departamentos
        ventas_ciudades = dict()
        for ciudad in self.ciudades:
            ventas_ciudades[ciudad] = 0
        for venta in self.get_all(desde,hasta):
            ventas_ciudades[venta.ciudad] += venta.importe
        result = map(lambda x: { "ciudad": x.upper(), "departamento": departamentos[x.lower()] or x.upper(), "importe": ventas_ciudades[x] }, self.ciudades)

        return sorted(result, key=lambda x: x['importe'], reverse=True)
