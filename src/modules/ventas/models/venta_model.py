from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from modules.ventas.models.detalle_venta_model import DetalleVentaModel

@dataclass
class VentaModel():
    id_venta: int
    fecha: datetime
    id_cliente: int
    nombre_cliente: str
    email: str
    medio_pago: str
    ciudad: str
    importe: float = field(default_factory=lambda value: datetime.strptime(value, '%Y-%m-%d'))
    detalle: List['DetalleVentaModel'] = field(default_factory=lambda value: list(map(lambda x: DetalleVentaModel(**x),value)))
    
    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, value: str):
        self._departamento = value


    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the object. This is useful for serialization and debugging.
        """
        return {
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "email": self.email,
            "medio_pago": self.medio_pago,
            "importe": self.importe,
            "detalle": self.detalle
        }

    def to_json(self) -> str:
        """
        Returns a JSON string representation of the object. This is useful for serialization and debugging.
        """
        return json.dumps({
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "email": self.email,
            "medio_pago": self.medio_pago,
            "importe": self.importe,
            "detalle": [det.to_dict() for det in self.detalle] if self.detalle else []
        }, default=str, indent=4)