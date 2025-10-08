from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class DetalleVentaModel():
    id_producto: int
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    id_venta: int
    cantidad: int
    importe: float

    def to_dict(self):
        """
        Returns a dictionary representation of the object. This is useful for serialization and debugging.
        """
        return {
            "id_venta": self.id_venta,
            "id_producto": self.id_producto,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "importe": self.importe
        }
    
    def to_json(self):
        """
        Returns a JSON string representation of the object. This is useful for serialization and debugging.
        """
        return json.dumps(self.to_dict(), default=str, indent=4)
    
    def get_fecha(self) -> datetime:
        """
        Returns the date of the venta as a datetime object.
        """
        from modules.ventas.service.ventas_service import VentasService
        fecha = VentasService().get_by_id_venta(self.id_venta).fecha
        return fecha if isinstance(fecha, datetime) else datetime.strptime(fecha, '%Y-%m-%d')