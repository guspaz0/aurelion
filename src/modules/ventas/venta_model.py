from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, TYPE_CHECKING, Optional
import json

if TYPE_CHECKING:
    from src.modules.ventas.detalle_venta_model import DetalleVentaModel

@dataclass
class VentaModel:
    id_venta: int
    id_cliente: int
    nombre_cliente: str
    email: str
    medio_pago: str
    ciudad: str
    fecha: datetime
    importe: float
    detalle: List['DetalleVentaModel'] = field(default_factory=list)

    def __post_init__(self):
        # Normalizar `fecha` si viene como string
        if isinstance(self.fecha, str):
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y"):
                try:
                    self.fecha = datetime.strptime(self.fecha, fmt)
                    break
                except ValueError:
                    continue
        # Normalizar `importe` si viene como string
        if isinstance(self.importe, str):
            try:
                self.importe = float(self.importe)
            except ValueError:
                pass

        # Convertir `detalle` a lista de DetalleVentaModel
        if self.detalle is None:
            self.detalle = []
        
        else:
            # importar en tiempo de ejecución para evitar problemas de importación circular
            try:
                from src.modules.ventas.detalle_venta_model import DetalleVentaModel
            except Exception:
                from .detalle_venta_model import DetalleVentaModel

            raw = self.detalle
            if isinstance(raw, str):
                try:
                    raw = json.loads(raw)
                except Exception:
                    raw = []
            elif not isinstance(raw, list):
                # Puede ser un file-like o similar
                try:
                    raw = json.load(raw)
                except Exception:
                    raw = []

            normalized: List[DetalleVentaModel] = []
            for item in raw:
                if isinstance(item, DetalleVentaModel):
                    normalized.append(item)
                elif isinstance(item, dict):
                    normalized.append(DetalleVentaModel(**item))
                else:
                    # ignorar elementos no reconocidos
                    continue

            self.detalle = normalized

    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, value: str):
        self._departamento = value


    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the object for serialization and debugging."""
        return {
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "email": self.email,
            "medio_pago": self.medio_pago,
            "importe": self.importe,
            "detalle": [det.to_dict() if hasattr(det, 'to_dict') else det.__dict__ for det in self.detalle]
        }

    def to_json(self) -> str:
        """Returns a JSON string representation of the object for serialization and debugging."""
        return json.dumps({
            "id_venta": self.id_venta,
            "fecha": self.fecha,
            "id_cliente": self.id_cliente,
            "nombre_cliente": self.nombre_cliente,
            "email": self.email,
            "medio_pago": self.medio_pago,
            "importe": self.importe,
            "detalle": [det.to_dict() if hasattr(det, 'to_dict') else det.__dict__ for det in self.detalle]
        }, default=str, indent=4)