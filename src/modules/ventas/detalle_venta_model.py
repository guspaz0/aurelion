from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class DetalleVentaModel:
    id_venta: int
    id_producto: int
    nombre_producto: str
    cantidad: int
    precio_unitario: float
    importe: float
    fecha: datetime = field(default_factory=datetime)

    def __post_init__(self):
        if not self.fecha:
            self.fecha = None
        else:
            self.fecha = datetime.strptime(self.fecha, '%Y-%m-%d')

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
            "importe": self.importe,
            "fecha": self.fecha
        }
    
    def to_json(self):
        """
        Returns a JSON string representation of the object. This is useful for serialization and debugging.
        """
        return json.dumps(self.to_dict(), default=str, indent=4)
    