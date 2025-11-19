from dataclasses import dataclass
from datetime import datetime, date
import json, logging
from typing import Dict, List, TYPE_CHECKING

logger = logging.getLogger(__file__)

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
        return self._ventas
    
    @ventas.setter
    def ventas(self, value: List['VentaModel']):
        self._ventas = value

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
    
