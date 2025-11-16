from datetime import datetime, date
import os, csv, logging
import pathlib
from typing import Any, Dict, List
from modules.ventas.models.venta_model import VentaModel
from modules.ventas.repository.ventas_dao import VentasDao

logger = logging.getLogger(__file__)

class VentasRepository:
    def __init__(self):
        self._dao = VentasDao()
        self.medios_de_pago = self._dao.get_medios_de_pago()
    
    def get_all(self, desde: datetime | date | str = None, hasta: datetime | date | str = None) -> List[VentaModel]:
        """
        Returns all the ventas stored in the repository.
        """
        if not desde or not hasta:
            return [VentaModel(*venta) for venta in self._dao.get_all()]
        if all(isinstance(fecha, str) for fecha in (desde,hasta)):
            desde = datetime.strptime(desde, "%Y-%m-%d")
            hasta = datetime.strptime(hasta, "%Y-%m-%d")
        if all(isinstance(fecha, date) for fecha in (desde, hasta)):
            desde = datetime.strptime(desde.strftime("%Y-%m-%d"), "%Y-%m-%d")
            hasta = datetime.strptime(hasta.strftime("%Y-%m-%d"), "%Y-%m-%d")
        return [VentaModel(*venta) for venta in self._dao.get_all(desde,hasta)]
    
    def get_by_id_venta(self, id_venta: int) -> VentaModel:
        """
        Returns the venta with the given id.

        :param id_venta: The id of the venta to retrieve
        """
        return VentaModel(*self._dao.get_by_id(id_venta))
    
    def get_by_id_cliente(self, id_cliente: int) -> List[VentaModel]:
        """
        Returns all the ventas made by a given customer

        :param id_cliente: The id of the client to retrieve
        """
        return [VentaModel(*dv) for dv in self._dao.get_by_cliente(id_cliente)]