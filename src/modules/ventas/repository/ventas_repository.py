from datetime import datetime, date
import os, csv
from typing import Any, Dict, List
from modules.ventas.models.venta_model import VentaModel


class VentasRepository:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "bd", "ventas.csv")
        self.ventas: List[VentaModel] = []
        self.medios_de_pago= set()
        self._load()

    def _load(self):
        """
        Loads the data from the CSV file into the repository.
        """
        with open(self.db_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            keys: List[str] = []
            for row in reader:
                dict: Dict[str, Any] = {}
                if len(keys) == 0:
                    keys = row
                    continue
                for i in range(0,len(keys)):
                    dict[keys[i]] = row[i] or ''
                dict['id_venta'] = int(dict['id_venta'])
                dict['id_cliente'] = int(dict['id_cliente'])
                dict['fecha'] = datetime.strptime(dict['fecha'], "%Y-%m-%d")
                self.ventas.append(VentaModel(**dict))
                self.medios_de_pago.add(dict['medio_pago'])
            csvfile.close()
    
    def get_all(self, desde: datetime | date | str = None, hasta: datetime | date | str = None) -> List[VentaModel]:
        """
        Returns all the ventas stored in the repository.
        """
        if not desde or not hasta:
            return self.ventas
        if all(isinstance(fecha, str) for fecha in (desde,hasta)):
            desde = datetime.strptime(desde, "%Y-%m-%d")
            hasta = datetime.strptime(hasta, "%Y-%m-%d")
        if all(isinstance(fecha, date) for fecha in (desde, hasta)):
            desde = datetime.strptime(desde.strftime("%Y-%m-%d"), "%Y-%m-%d")
            hasta = datetime.strptime(hasta.strftime("%Y-%m-%d"), "%Y-%m-%d")
        return [venta for venta in self.ventas if desde <= venta.fecha <= hasta]
    
    def get_by_id_venta(self, id_venta: int) -> VentaModel:
        """
        Returns the venta with the given id.

        :param id_venta: The id of the venta to retrieve
        """
        return [dv for dv in self.ventas if dv.id_venta == id_venta][0]
    
    def get_by_id_cliente(self, id_cliente: int) -> List[VentaModel]:
        """
        Returns all the ventas made by a given customer

        :param id_cliente: The id of the client to retrieve
        """
        return [dv for dv in self.ventas if dv.id_cliente == id_cliente]