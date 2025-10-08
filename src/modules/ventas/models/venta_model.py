from dataclasses import dataclass
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

    @property
    def detalle(self) -> List['DetalleVentaModel']:
        from modules.ventas.service.detalle_ventas_service import DetalleVentasService
        self._detalle = DetalleVentasService().get_by_id_venta(self.id_venta)
        return self._detalle
    
    @detalle.setter
    def detalle(self, value: List['DetalleVentaModel']):
        from modules.ventas.models.detalle_venta_model import DetalleVentaModel
        if isinstance(value, list) and all(isinstance(item, DetalleVentaModel) for item in value):
            self._detalle = value

    @property
    def importe(self) -> float:
        return sum(detalle.importe for detalle in self.detalle if detalle is not None)
    
    @importe.setter
    def importe(self, value: float):
        if value is not None and isinstance(value, (int, float)):
            self._importe = value
    
    @property
    def ciudad(self) -> str:
        from modules.clientes.cliente_service import ClienteService
        cliente = ClienteService().buscar_por_id(self.id_cliente)
        self.departamento = cliente.departamento
        return cliente.ciudad

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
            "detalle": self.detalle,
            "importe": self.importe
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
            "detalle": [det.to_dict() for det in self.detalle] if self.detalle else [],
            "importe": self.importe
        }, default=str, indent=4)