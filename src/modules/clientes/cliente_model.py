from dataclasses import dataclass
from datetime import datetime, date
import json
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.ventas.models.venta_model import VentaModel

@dataclass
class ClienteModel:
    id_cliente: int
    nombre_cliente: str
    email: str
    ciudad: str
    fecha_alta: datetime
    departamento: str = None

    @property
    def ventas(self) -> List['VentaModel']:
        from modules.ventas.service.ventas_service import VentasService
        self._ventas = VentasService().get_by_id_cliente(self.id_cliente)
        return self._ventas
    
    @ventas.setter
    def ventas(self, value: List['VentaModel']):
        if isinstance(value, list) and all(isinstance(item, VentaModel) for item in value):
            self._ventas = value

    def total_ventas(self, desde: datetime | date | str = None, hasta: datetime | date | str = None) -> Dict[str,int | float]:
        """
        Retorna la sumatoria de los importes de las ventas realizadas por el cliente.
        
        :param desde: Fecha inicial para filtrar las ventas
        :param hasta: Fecha final para filtrar las ventas
        """
        from modules.ventas.repository.ventas_repository import VentasRepository
        medios_de_pago: dict = {}
        for medio in list(VentasRepository().medios_de_pago):
            medios_de_pago[medio] = 0
        importe: float = 0
        ventas: List['VentaModel'] = self.ventas
        if all(isinstance(fecha, str) for fecha in (desde, hasta)):
            desde = datetime.strptime(desde, "%Y-%m-%d")
            hasta = datetime.strptime(hasta, "%Y-%m-%d")
        if all(isinstance(fecha, date) for fecha in (desde, hasta)):
            desde = datetime.strptime(desde.strftime("%Y-%m-%d"), "%Y-%m-%d")
            hasta = datetime.strptime(hasta.strftime("%Y-%m-%d"), "%Y-%m-%d")
        if all(isinstance(fecha, datetime) for fecha in (desde, hasta)):
            ventas = [venta for venta in self.ventas if desde <= venta.fecha <= hasta]
        
        for venta in ventas:
            medios_de_pago[venta.medio_pago] += venta.importe
            importe += venta.importe
        return { "importe": importe, "cantidad_ventas": len(ventas), **medios_de_pago }

    def to_dict(self):
        """
        Retorna un diccionario con los datos del cliente.
        """
        return {
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "email": self.email,
            "ciudad": self.ciudad,
            "fecha_alta": self.fecha_alta,
            "ventas": [venta.to_dict() for venta in self.ventas] if self.ventas else []
        }

    def to_json(self):
        """
        Retorna un JSON con los datos del cliente.
        """
        return json.dumps({
            **self.to_dict(),
            "fecha_alta": self.fecha_alta if self.fecha_alta else None,
            "ventas": [
                {
                    **venta.to_dict(), "detalle": [dv.to_dict() for dv in venta.detalle]
                } for venta in self.ventas
            ] if self.ventas else []
        }, default=str, indent=4)
    
